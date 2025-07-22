#!/usr/bin/env python3
"""
MCP Server con supporto per Gemini e OpenRouter
Server HTTP che espone API per interagire con MCP usando diversi provider AI
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import traceback
from collections import defaultdict, deque

# FastAPI imports
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Environment and utilities
from dotenv import load_dotenv
import requests

# Environment and utilities
from dotenv import load_dotenv
import requests

# Caricate le variabili d'ambiente
load_dotenv()

# Configurazione logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importazioni MCP e LangChain
try:
    from mcp_use import MCPAgent, MCPClient
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
    from langchain_core.outputs import ChatGeneration, ChatResult
    from langchain_core.callbacks.manager import CallbackManagerForLLMRun
    MCP_AVAILABLE = True
    logger.info("MCP e LangChain disponibili")
except ImportError as e:
    logger.error(f"MCP o LangChain non disponibili: {e}")
    MCP_AVAILABLE = False

# Importazioni aggiuntive per connessioni HTTP/SSE
import aiohttp
from urllib.parse import urljoin, urlparse

# Configurazione logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importazioni MCP e LangChain
try:
    from mcp_use import MCPAgent, MCPClient
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
    from langchain_core.outputs import ChatGeneration, ChatResult
    from langchain_core.callbacks.manager import CallbackManagerForLLMRun
    MCP_AVAILABLE = True
    logger.info("MCP e LangChain disponibili")
except ImportError as e:
    logger.error(f"MCP o LangChain non disponibili: {e}")
    MCP_AVAILABLE = False

# Modelli Pydantic per API
class ConversationMessage(BaseModel):
    """Messaggio in una conversazione"""
    id: str = Field(..., description="ID univoco del messaggio")
    content: str = Field(..., description="Contenuto del messaggio")
    role: str = Field(..., description="Ruolo del messaggio (user, assistant)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp del messaggio")

class MCPQueryRequest(BaseModel):
    prompt: str = Field(..., description="Prompt da inviare al modello AI")
    user_id: Optional[str] = Field("default", description="ID dell'utente per il tracking della conversazione")
    provider: Optional[str] = Field(None, description="Provider AI (gemini, openrouter)")
    model: Optional[str] = Field(None, description="Modello specifico da usare")
    max_steps: Optional[int] = Field(3, description="Numero massimo di passi MCP")
    temperature: Optional[float] = Field(None, description="Temperatura per la generazione")
    max_tokens: Optional[int] = Field(None, description="Numero massimo di token")
    system_prompt: Optional[str] = Field(None, description="Prompt di sistema opzionale")
    prompt_file: Optional[str] = Field(None, description="Nome del file di prompt da usare (senza estensione)")
    use_context: Optional[bool] = Field(True, description="Se includere il contesto delle conversazioni precedenti")

class MCPQueryResponse(BaseModel):
    response: str = Field(..., description="Risposta del modello AI")
    provider: str = Field(..., description="Provider utilizzato")
    model: str = Field(..., description="Modello utilizzato")
    steps: int = Field(..., description="Numero di passi eseguiti")
    timestamp: str = Field(..., description="Timestamp della risposta")
    execution_time: float = Field(..., description="Tempo di esecuzione in secondi")
    conversation_id: str = Field(..., description="ID della conversazione")
    context_used: bool = Field(..., description="Se è stato utilizzato il contesto precedente")
    context_messages_count: int = Field(..., description="Numero di messaggi del contesto utilizzati")

class ProviderInfo(BaseModel):
    name: str
    models: List[str]
    default_model: str
    available: bool

class ServerStatus(BaseModel):
    status: str
    version: str
    mcp_available: bool
    providers: List[ProviderInfo]
    uptime: str

# Modelli per la gestione della memoria delle conversazioni
class MemoryStatsResponse(BaseModel):
    memory_limit: int = Field(..., description="Limite massimo di messaggi per utente")
    default_user_id: str = Field(..., description="ID utente di default")
    active_users: int = Field(..., description="Numero di utenti attivi con conversazioni")
    users: Dict[str, Dict[str, Any]] = Field(..., description="Statistiche per ogni utente")

class ClearMemoryRequest(BaseModel):
    user_id: Optional[str] = Field(None, description="ID utente specifico da pulire. Se non fornito, pulisce tutte le conversazioni")

class ClearMemoryResponse(BaseModel):
    success: bool = Field(..., description="Se l'operazione è riuscita")
    message: str = Field(..., description="Messaggio descrittivo dell'operazione")
    cleared_user: Optional[str] = Field(None, description="ID dell'utente pulito")
    users_cleared: int = Field(..., description="Numero di utenti le cui conversazioni sono state pulite")

# Implementazione OpenRouter LLM personalizzata
class OpenRouterLLM(BaseChatModel):
    """Wrapper per OpenRouter API compatibile con LangChain"""
    
    model: str = Field(description="Nome del modello OpenRouter")
    api_key: str = Field(description="Chiave API OpenRouter")
    base_url: str = Field(default="https://openrouter.ai/api/v1", description="URL base API")
    temperature: float = Field(default=0.7, description="Temperatura per la generazione")
    max_tokens: int = Field(default=4000, description="Numero massimo di token")
    
    class Config:
        arbitrary_types_allowed = True
    
    @property
    def model_name(self) -> str:
        """Proprietà per compatibilità con LangChain"""
        return self.model
    
    @property
    def _llm_type(self) -> str:
        return "openrouter"
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Genera una risposta usando OpenRouter API"""
        
        # Converte i messaggi in formato OpenRouter
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                formatted_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                formatted_messages.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, SystemMessage):
                formatted_messages.append({"role": "system", "content": msg.content})
            else:
                # Fallback per altri tipi di messaggio
                role = getattr(msg, 'type', 'user')
                if role == 'human':
                    role = 'user'
                elif role == 'ai':
                    role = 'assistant'
                formatted_messages.append({"role": role, "content": msg.content})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "MCP Server with OpenRouter"
        }
        
        payload = {
            "model": self.model,
            "messages": formatted_messages,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature)
        }
        
        if stop:
            payload["stop"] = stop
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=int(os.getenv('REQUEST_TIMEOUT', 30))
            )
            response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            # Crea il risultato nel formato LangChain
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            return ChatResult(generations=[generation])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API error: {e}")
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    def bind_tools(self, tools, **kwargs):
        """Implementa bind_tools per compatibilità MCP"""
        return self
    
    @property
    def _identifying_params(self) -> dict:
        """Parametri identificativi per il modello"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "base_url": self.base_url
        }

# Servizio MCP principale

# Servizio MCP principale
class MCPService:
    """Servizio per gestire operazioni MCP con supporto multi-provider"""
    
    def __init__(self, config_file: str = "mcp_config.json"):
        self.client = None
        self.agent = None
        self.llm = None
        self.initialized = False
        self.config_file = config_file
        self.config = self._load_config()
        self.start_time = datetime.now()
        
        # Sistema di memoria per conversazioni per utente
        # Struttura: {user_id: deque([{role, content, timestamp}], maxlen=limit)}
        self.conversation_memory = defaultdict(lambda: deque(
            maxlen=int(os.getenv('CONVERSATION_MEMORY_LIMIT', 30))
        ))
        self.memory_limit = int(os.getenv('CONVERSATION_MEMORY_LIMIT', 30))
        self.default_user_id = os.getenv('DEFAULT_USER_ID', 'default')
        
        logger.info(f"Sistema memoria conversazioni inizializzato - Limite: {self.memory_limit} messaggi per utente")
        
    def _load_config(self) -> Dict[str, Any]:
        """Carica la configurazione dal file JSON"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {self.config_file} not found")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file: {e}")
            return {}
    
    def _load_prompt_from_file(self, prompt_name: str) -> Optional[str]:
        """Carica un prompt da file nella directory prompts/"""
        prompt_file = f"prompts/{prompt_name}.txt"
        try:
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    logger.info(f"Prompt caricato da file: {prompt_file}")
                    return content
            else:
                logger.debug(f"File prompt non trovato: {prompt_file}")
                return None
        except Exception as e:
            logger.error(f"Errore nel caricamento del prompt da {prompt_file}: {e}")
            return None
    
    def _add_message_to_memory(self, user_id: str, role: str, content: str):
        """Aggiunge un messaggio alla memoria dell'utente"""
        if not user_id:
            user_id = self.default_user_id
            
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        # Aggiunge alla deque che automaticamente mantiene il limite
        self.conversation_memory[user_id].append(message)
        
        logger.debug(f"Messaggio aggiunto alla memoria per utente {user_id}. "
                    f"Messaggi totali: {len(self.conversation_memory[user_id])}")
    
    def _get_conversation_context(self, user_id: str) -> List[Dict[str, str]]:
        """Recupera il contesto delle conversazioni per un utente"""
        if not user_id:
            user_id = self.default_user_id
            
        messages = list(self.conversation_memory.get(user_id, []))
        
        logger.debug(f"Recuperati {len(messages)} messaggi dal contesto per utente {user_id}")
        return messages
    
    def _build_context_prompt(self, user_id: str, current_prompt: str) -> str:
        """Costruisce un prompt includendo il contesto delle conversazioni precedenti"""
        context_messages = self._get_conversation_context(user_id)
        
        if not context_messages:
            logger.debug("Nessun contesto precedente trovato")
            return current_prompt
        
        # Costruisce il contesto
        context_parts = ["=== CONTESTO CONVERSAZIONE PRECEDENTE ==="]
        
        for msg in context_messages:
            role_label = "UTENTE" if msg["role"] == "user" else "ASSISTENTE"
            context_parts.append(f"{role_label}: {msg['content']}")
        
        context_parts.extend([
            "=== FINE CONTESTO ===",
            "",
            f"DOMANDA CORRENTE: {current_prompt}"
        ])
        
        context_prompt = "\n".join(context_parts)
        
        logger.debug(f"Contesto costruito con {len(context_messages)} messaggi precedenti")
        return context_prompt
    
    def clear_user_memory(self, user_id: str = None):
        """Pulisce la memoria delle conversazioni per un utente specifico o tutti"""
        if user_id:
            if user_id in self.conversation_memory:
                self.conversation_memory[user_id].clear()
                logger.info(f"Memoria cancellata per utente: {user_id}")
            else:
                logger.info(f"Nessuna memoria trovata per utente: {user_id}")
        else:
            self.conversation_memory.clear()
            logger.info("Memoria di tutte le conversazioni cancellata")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Restituisce statistiche sulla memoria delle conversazioni"""
        stats = {
            "memory_limit": self.memory_limit,
            "default_user_id": self.default_user_id,
            "active_users": len(self.conversation_memory),
            "users": {}
        }
        
        for user_id, messages in self.conversation_memory.items():
            stats["users"][user_id] = {
                "message_count": len(messages),
                "last_message_time": messages[-1]["timestamp"] if messages else None
            }
        
        return stats
    
    def get_available_providers(self) -> List[ProviderInfo]:
        """Restituisce la lista dei provider disponibili"""
        providers = []
        
        for provider_name, provider_config in self.config.get("providers", {}).items():
            # Verifica se il provider è disponibile
            available = False
            
            if provider_name == "gemini":
                api_key = os.getenv('GOOGLE_API_KEY') or provider_config.get('api_key')
                available = bool(api_key and MCP_AVAILABLE)
            elif provider_name == "openrouter":
                api_key = os.getenv('OPENROUTER_API_KEY') or provider_config.get('api_key')
                available = bool(api_key and MCP_AVAILABLE)
            
            providers.append(ProviderInfo(
                name=provider_name,
                models=provider_config.get('models', []),
                default_model=provider_config.get('model', ''),
                available=available
            ))
        
        return providers
    
    def _create_mcp_client(self):
        """Crea il client MCP appropriato basato sulla configurazione"""
        try:
            # Controlla se ci sono server con URL (per 1MCP Agent)
            mcp_servers = self.config.get("mcpServers", {})
            
            # Cerca server con URL (connessioni HTTP/SSE)
            for server_name, server_config in mcp_servers.items():
                if server_config.get("disabled", False):
                    continue
                    
                if "url" in server_config:
                    url = server_config["url"]
                    
                    logger.info(f"Configurando client HTTP per server: {server_name} -> {url}")
                    
                    # Usa il formato corretto per mcp-use con HTTP/SSE
                    config_dict = {
                        "mcpServers": {
                            server_name: {
                                "url": url
                            }
                        }
                    }
                    
                    # Aggiungi headers se presenti
                    if "headers" in server_config:
                        config_dict["mcpServers"][server_name]["headers"] = server_config["headers"]
                    
                    logger.info(f"Creando client MCP con configurazione: {config_dict}")
                    return MCPClient.from_dict(config_dict)
            
            # Se non ci sono server con URL, usa il client tradizionale
            if not os.path.exists(self.config_file):
                logger.warning(f"File di configurazione MCP non trovato: {self.config_file}")
                return MCPClient()
            else:
                logger.info("Usando client MCP tradizionale")
                return MCPClient.from_config_file(self.config_file)
                
        except Exception as e:
            logger.error(f"Errore nella creazione del client MCP: {e}")
            return MCPClient()  # Fallback a client vuoto
    
    async def initialize(self, provider: str = None, model: str = None):
        """Inizializza il servizio MCP con provider e modello specificati"""
        if not MCP_AVAILABLE:
            logger.error("MCP non disponibile. Installare con: pip install mcp-use langchain-openai langchain-google-genai")
            return False
            
        try:
            # Usa provider e modello dalla configurazione o dai parametri
            provider = provider or self.config.get("default_provider", "gemini")
            
            if provider not in self.config.get("providers", {}):
                logger.error(f"Provider {provider} non configurato")
                return False
                
            provider_config = self.config["providers"][provider]
            model = model or provider_config.get("model")
            
            # Inizializza il client MCP
            self.client = self._create_mcp_client()
            
            # Configura il modello LLM in base al provider
            logger.debug(f"Configurazione LLM per provider: {provider}")
            
            if provider == "openrouter":
                api_key = os.getenv('OPENROUTER_API_KEY') or provider_config.get('api_key')
                if not api_key:
                    logger.error("OPENROUTER_API_KEY richiesta per OpenRouter")
                    return False
                
                logger.debug(f"Creazione OpenRouterLLM con modello: {model}")
                self.llm = OpenRouterLLM(
                    model=model,
                    api_key=api_key,
                    base_url=provider_config.get('base_url', 'https://openrouter.ai/api/v1'),
                    temperature=float(os.getenv('DEFAULT_TEMPERATURE', 0.7)),
                    max_tokens=int(os.getenv('MAX_TOKENS', 4000))
                )
                logger.debug(f"OpenRouterLLM creato. Modello configurato: {self.llm.model}")
                
            elif provider == "gemini":
                api_key = os.getenv('GOOGLE_API_KEY') or provider_config.get('api_key')
                if not api_key:
                    logger.error("GOOGLE_API_KEY richiesta per Gemini")
                    return False
                
                logger.debug(f"Creazione ChatGoogleGenerativeAI con modello: {model}")
                self.llm = ChatGoogleGenerativeAI(
                    model=model,
                    google_api_key=api_key,
                    temperature=float(os.getenv('DEFAULT_TEMPERATURE', 0.7)),
                    max_tokens=int(os.getenv('MAX_TOKENS', 4000))
                )
                logger.debug(f"ChatGoogleGenerativeAI creato. Modello configurato: {model}")
            else:
                logger.error(f"Provider {provider} non supportato")
                return False
            
            # Inizializza l'agent MCP
            logger.debug("Creazione MCPAgent con LLM configurato")
            self.agent = MCPAgent(llm=self.llm, client=self.client)
            self.initialized = True
            
            logger.info(f"MCP Service inizializzato con provider: {provider}, model: {model}")
            logger.debug(f"Tipo LLM finale: {type(self.llm).__name__}")
            return True
            
        except Exception as e:
            logger.error(f"Errore durante l'inizializzazione: {e}")
            logger.error(traceback.format_exc())
            return False
    
    async def query(self, request: MCPQueryRequest) -> MCPQueryResponse:
        """Esegue una query usando MCP"""
        start_time = datetime.now()
        
        # Determina user_id (usa default se non specificato)
        user_id = request.user_id or self.default_user_id
        
        # Log della richiesta in debug
        logger.debug("=== INIZIO RICHIESTA MCP ===")
        logger.debug(f"Request ID: {id(request)}")
        logger.debug(f"User ID: {user_id}")
        logger.debug(f"Prompt: {request.prompt[:200]}{'...' if len(request.prompt) > 200 else ''}")
        logger.debug(f"Provider richiesto: {request.provider}")
        logger.debug(f"Modello richiesto: {request.model}")
        logger.debug(f"Max steps: {request.max_steps}")
        logger.debug(f"Temperature: {request.temperature}")
        logger.debug(f"Max tokens: {request.max_tokens}")
        logger.debug(f"Use context: {request.use_context}")
        logger.debug(f"System prompt: {request.system_prompt[:100] + '...' if request.system_prompt and len(request.system_prompt) > 100 else request.system_prompt}")
        
        # Determina provider e modello che verranno utilizzati
        target_provider = request.provider or self.config.get("default_provider", "unknown")
        target_model = request.model or self.config.get("providers", {}).get(target_provider, {}).get("model", "unknown")
        
        logger.debug(f"Provider target: {target_provider}")
        logger.debug(f"Modello target: {target_model}")
        logger.debug(f"Servizio già inizializzato: {self.initialized}")
        
        # Reinizializza se necessario con il provider richiesto
        if not self.initialized or request.provider:
            logger.debug(f"Reinizializzazione richiesta per provider: {target_provider}, modello: {target_model}")
            success = await self.initialize(request.provider, request.model)
            if not success:
                logger.error("Fallita l'inizializzazione del servizio MCP")
                raise HTTPException(status_code=500, detail="Impossibile inizializzare il servizio MCP")
        
        # Log del modello LLM attualmente configurato
        if hasattr(self.llm, 'model'):
            logger.debug(f"Modello LLM configurato: {self.llm.model}")
        elif hasattr(self.llm, 'model_name'):
            logger.debug(f"Modello LLM configurato: {self.llm.model_name}")
        else:
            logger.debug(f"Tipo LLM configurato: {type(self.llm).__name__}")
        
        try:
            # Prepara il prompt di sistema
            system_prompt = request.system_prompt
            
            # Se è specificato un file di prompt, caricalo
            if request.prompt_file:
                file_prompt = self._load_prompt_from_file(request.prompt_file)
                if file_prompt:
                    system_prompt = file_prompt
                    logger.info(f"Utilizzando prompt da file: {request.prompt_file}.txt")
                else:
                    logger.warning(f"File prompt {request.prompt_file}.txt non trovato, uso prompt di default")
            
            # Se non c'è un prompt di sistema specificato, prova a caricare il prompt di default
            elif not system_prompt:
                default_prompt = self._load_prompt_from_file("default")
                if default_prompt:
                    system_prompt = default_prompt
                    logger.info("Utilizzando prompt di default da file")
            
            # Gestione del contesto delle conversazioni
            context_used = False
            context_messages_count = 0
            query_text = request.prompt
            
            if request.use_context:
                # Costruisce il prompt con il contesto delle conversazioni precedenti
                context_messages = self._get_conversation_context(user_id)
                if context_messages:
                    query_text = self._build_context_prompt(user_id, request.prompt)
                    context_used = True
                    context_messages_count = len(context_messages)
                    logger.info(f"Utilizzando contesto conversazione con {context_messages_count} messaggi precedenti per utente {user_id}")
            
            # Aggiungi il system prompt se specificato
            if system_prompt:
                query_text = f"System: {system_prompt}\n\nUser: {query_text}"
                logger.debug("System prompt aggiunto alla query")
            
            logger.debug(f"Query finale preparata (lunghezza: {len(query_text)} caratteri)")
            
            # Salva la domanda dell'utente nella memoria
            self._add_message_to_memory(user_id, "user", request.prompt)
            
            # Esegue la query
            logger.debug("Invio query al modello AI...")
            result = await self.agent.run(
                query=query_text,
                max_steps=request.max_steps or self.config.get("max_steps", 3)
            )
            
            # Salva la risposta dell'assistente nella memoria
            self._add_message_to_memory(user_id, "assistant", result)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.debug(f"Query completata in {execution_time:.2f} secondi")
            logger.debug(f"Risposta ricevuta (lunghezza: {len(result)} caratteri)")
            
            # Determina provider e modello utilizzati
            used_provider = request.provider or self.config.get("default_provider", "unknown")
            used_model = request.model or self.config.get("providers", {}).get(used_provider, {}).get("model", "unknown")
            
            logger.debug(f"Provider utilizzato: {used_provider}")
            logger.debug(f"Modello utilizzato: {used_model}")
            logger.debug("=== FINE RICHIESTA MCP ===")
            
            return MCPQueryResponse(
                response=result,
                provider=used_provider,
                model=used_model,
                steps=request.max_steps or self.config.get("max_steps", 3),
                timestamp=datetime.now().isoformat(),
                execution_time=execution_time,
                conversation_id=user_id,
                context_used=context_used,
                context_messages_count=context_messages_count
            )
            
        except Exception as e:
            logger.error(f"Errore durante l'esecuzione della query: {e}")
            logger.error(f"Request ID: {id(request)}")
            logger.error(traceback.format_exc())
            logger.debug("=== FINE RICHIESTA MCP (CON ERRORE) ===")
            raise HTTPException(status_code=500, detail=f"Errore durante l'esecuzione: {str(e)}")

# Inizializza il servizio MCP
mcp_service = MCPService()

# Crea l'app FastAPI
app = FastAPI(
    title="MCP Server",
    description="Server HTTP per interagire con MCP usando Gemini e OpenRouter",
    version="1.0.0"
)

# Aggiungi CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency per verificare lo stato del servizio
async def get_mcp_service():
    return mcp_service

# Endpoint per lo stato di salute
@app.get("/health", response_model=ServerStatus)
async def health_check(service: MCPService = Depends(get_mcp_service)):
    """Controlla lo stato del server"""
    uptime = datetime.now() - service.start_time
    
    return ServerStatus(
        status="healthy",
        version="1.0.0",
        mcp_available=MCP_AVAILABLE,
        providers=service.get_available_providers(),
        uptime=str(uptime)
    )

# Endpoint per i provider disponibili
@app.get("/api/v1/providers", response_model=List[ProviderInfo])
async def list_providers(service: MCPService = Depends(get_mcp_service)):
    """Lista i provider AI disponibili"""
    return service.get_available_providers()

# Endpoint per i modelli di un provider
@app.get("/api/v1/providers/{provider}/models")
async def list_models(provider: str, service: MCPService = Depends(get_mcp_service)):
    """Lista i modelli disponibili per un provider"""
    providers = service.config.get("providers", {})
    
    if provider not in providers:
        raise HTTPException(status_code=404, detail=f"Provider {provider} non trovato")
    
    return {
        "provider": provider,
        "models": providers[provider].get("models", []),
        "default_model": providers[provider].get("model", "")
    }

# Endpoint principale per le query MCP
@app.post("/api/v1/query", response_model=MCPQueryResponse)
async def mcp_query(request: MCPQueryRequest, service: MCPService = Depends(get_mcp_service)):
    """Esegue una query usando MCP"""
    logger.info(f"Ricevuta query: {request.prompt[:100]}...")
    return await service.query(request)

# Endpoint per test rapido
@app.get("/api/v1/test")
async def test_endpoint():
    """Endpoint di test per verificare che il server funzioni"""
    return {
        "message": "MCP Server is running!",
        "timestamp": datetime.now().isoformat(),
        "mcp_available": MCP_AVAILABLE
    }

# Endpoint per la configurazione
@app.get("/api/v1/config")
async def get_config(service: MCPService = Depends(get_mcp_service)):
    """Restituisce la configurazione attuale (senza chiavi API)"""
    config = service.config.copy()
    
    # Rimuovi le chiavi API per sicurezza
    if "providers" in config:
        for provider in config["providers"]:
            if "api_key" in config["providers"][provider]:
                config["providers"][provider]["api_key"] = "***"
    
    return config

# Endpoint per le statistiche della memoria delle conversazioni
@app.get("/api/v1/memory/stats", response_model=MemoryStatsResponse)
async def get_memory_stats(service: MCPService = Depends(get_mcp_service)):
    """Restituisce le statistiche della memoria delle conversazioni"""
    logger.info("Richiesta statistiche memoria conversazioni")
    stats = service.get_memory_stats()
    return MemoryStatsResponse(**stats)

# Endpoint per pulire la memoria delle conversazioni
@app.delete("/api/v1/memory/clear", response_model=ClearMemoryResponse)
async def clear_conversation_memory(
    request: ClearMemoryRequest, 
    service: MCPService = Depends(get_mcp_service)
):
    """Pulisce la memoria delle conversazioni per un utente specifico o tutti gli utenti"""
    try:
        user_id = request.user_id
        users_before = len(service.conversation_memory)
        
        if user_id:
            # Pulisci memoria per utente specifico
            user_existed = user_id in service.conversation_memory
            service.clear_user_memory(user_id)
            users_cleared = 1 if user_existed else 0
            
            message = f"Memoria conversazione pulita per utente: {user_id}"
            if not user_existed:
                message += " (utente non aveva conversazioni attive)"
                
            logger.info(f"Memoria pulita per utente: {user_id}")
            
            return ClearMemoryResponse(
                success=True,
                message=message,
                cleared_user=user_id,
                users_cleared=users_cleared
            )
        else:
            # Pulisci memoria per tutti gli utenti
            service.clear_user_memory()  # Senza parametri pulisce tutto
            users_cleared = users_before
            
            message = f"Memoria di tutte le conversazioni pulita. Utenti interessati: {users_cleared}"
            logger.info("Memoria di tutte le conversazioni pulita")
            
            return ClearMemoryResponse(
                success=True,
                message=message,
                cleared_user=None,
                users_cleared=users_cleared
            )
            
    except Exception as e:
        logger.error(f"Errore nella pulizia della memoria: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Errore nella pulizia della memoria: {str(e)}"
        )

if __name__ == "__main__":
    # Configurazione del server
    host = os.getenv('MCP_SERVER_HOST', '0.0.0.0')
    port = int(os.getenv('MCP_SERVER_PORT', 8000))
    debug = os.getenv('MCP_SERVER_DEBUG', 'true').lower() == 'true'
    
    logger.info(f"Avvio MCP Server su {host}:{port}")
    logger.info(f"MCP disponibile: {MCP_AVAILABLE}")
    
    # Avvia il server
    uvicorn.run(
        "mcp_server:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "warning"
    )
