# REST Chatbot MCP Server

Un server HTTP REST che espone API per interagire con il Model Context Protocol (MCP) utilizzando diversi provider AI come Gemini e OpenRouter.

## 🚀 Caratteristiche

- **Multi-Provider AI**: Supporto per Google Gemini e OpenRouter
- **Sistema di Prompt Configurabili**: Prompt specializzati caricati automaticamente da file
- **API REST**: Interfaccia HTTP semplice per integrazioni
- **1MCP Agent Integration**: Supporto per connessioni HTTP/SSE al 1MCP Agent
- **Backward Compatibility**: Piena compatibilità con server MCP tradizionali ### 6. Test Manuali

```bash
# Test semplice
curl -X GET "http://localhost:8000/api/v1/test"

# Test query di base (usa provider e modello di default)
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Ciao, come stai?"}'
```

## 🎯 Esempi Specifici per Provider

### Google Gemini

#### Query Semplice con Gemini Flash
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Qual è la capitale dell'\''Italia?",
    "provider": "gemini",
    "model": "gemini-1.5-flash"
  }'
```

#### Query Complessa con Gemini Pro
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Scrivi un algoritmo Python per ordinare una lista usando quicksort",
    "provider": "gemini",
    "model": "gemini-1.5-pro",
    "max_steps": 5,
    "temperature": 0.2,
    "system_prompt": "Sei un esperto programmatore Python. Fornisci codice ben commentato."
  }'
```

#### Analisi di Testo con Gemini
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analizza il sentiment di questo testo: '\''Oggi è stata una giornata fantastica, sono molto felice!'\''",
    "provider": "gemini",
    "model": "gemini-1.5-flash",
    "max_steps": 2,
    "temperature": 0.1
  }'
```

### DeepSeek (OpenRouter - Gratuito)

#### Query Semplice con DeepSeek
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Spiegami in termini semplici cosa è l'\''intelligenza artificiale",
    "provider": "openrouter",
    "model": "deepseek/deepseek-chat-v3-0324:free"
  }'
```

#### Coding con DeepSeek
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea una funzione JavaScript che validi un indirizzo email",
    "provider": "openrouter",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_steps": 3,
    "temperature": 0.3,
    "system_prompt": "Scrivi codice JavaScript pulito e ben documentato con esempi di utilizzo."
  }'
```

#### Riassunto di Testo con DeepSeek
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Riassumi in 3 punti chiave: Il machine learning è una branca dell'\''intelligenza artificiale che permette ai computer di apprendere senza essere esplicitamente programmati per ogni compito specifico.",
    "provider": "openrouter",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_steps": 2,
    "temperature": 0.5
  }'
```

### Confronto Provider

#### Stessa Domanda a Entrambi i Provider

**Con Gemini:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Qual è la differenza tra machine learning e deep learning?",
    "provider": "gemini",
    "model": "gemini-1.5-flash",
    "temperature": 0.7
  }'
```

**Con DeepSeek:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Qual è la differenza tra machine learning e deep learning?",
    "provider": "openrouter",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "temperature": 0.7
  }'
```

### Esempi con Casi d'Uso Specifici

#### 📝 Scrittura Creativa
```bash
# Con Gemini (migliore per creatività)
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Scrivi una breve storia di fantascienza ambientata nel 2100",
    "provider": "gemini",
    "model": "gemini-1.5-pro",
    "max_steps": 4,
    "temperature": 0.9,
    "max_tokens": 1000
  }'
```

#### 🔧 Problem Solving Tecnico
```bash
# Con DeepSeek (ottimo per programmazione)
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Debug questo codice Python che non funziona: def calcola_media(numeri): return sum(numeri) / len(numeri); print(calcola_media([]))",
    "provider": "openrouter",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_steps": 3,
    "temperature": 0.2,
    "system_prompt": "Analizza il codice, identifica il problema e fornisci la soluzione corretta."
  }'
```

#### 📊 Analisi Dati
```bash
# Con Gemini (buono per analisi)
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analizza questi dati di vendita e suggerisci azioni: Gen: 1000€, Feb: 800€, Mar: 1200€, Apr: 900€, Mag: 1400€",
    "provider": "gemini",
    "model": "gemini-1.5-flash",
    "max_steps": 4,
    "temperature": 0.4,
    "system_prompt": "Sei un analista di business. Fornisci insights pratici e actionable."
  }'
```ioni MCP
- **Configurazione Flessibile**: File di configurazione JSON per provider e modelli
- **Logging Avanzato**: Sistema di logging configurabile
- **Documentazione API**: Swagger/OpenAPI integrato
- **CORS**: Supporto completo per richieste cross-origin

## 📁 Struttura del Progetto

```
rest-chatbot-mcp/
├── mcp_server.py          # Server principale FastAPI
├── mcp_config.json        # Configurazione provider e modelli
├── requirements.txt       # Dipendenze Python
├── .env                   # Variabili d'ambiente
├── install.sh            # Script di installazione
├── start.sh              # Script di avvio
├── test_server.sh        # Script di test
├── interactive_client.py  # Client interattivo Python
├── interactive_client.sh  # Client interattivo Bash
└── README.md             # Questo file
```

## 🛠️ Installazione

### Prerequisiti

- Python 3.8+
- Node.js (per server MCP esterni)
- pip3

### Installazione Rapida

```bash
# Clona il repository
git clone <repository-url>
cd rest-chatbot-mcp

# Esegui lo script di installazione
chmod +x install.sh
./install.sh

# Configura le variabili d'ambiente
cp .env.example .env
# Modifica .env con le tue chiavi API
```

### Installazione Manuale

```bash
# Installa le dipendenze Python
pip3 install -r requirements.txt

# Installa server MCP esterni
npm install -g @modelcontextprotocol/server-postgres
```

## ⚙️ Configurazione

### Variabili d'Ambiente (.env)

```properties
# API Keys
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key
GOOGLE_API_KEY=your-google-api-key

# Configurazioni Server
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
MCP_SERVER_DEBUG=true

# Logging
LOG_LEVEL=INFO

# AI Settings
REQUEST_TIMEOUT=30
MAX_TOKENS=4000
DEFAULT_TEMPERATURE=0.7
```

### Configurazione Provider (mcp_config.json)

```json
{
  "providers": {
    "gemini": {
      "model": "gemini-1.5-flash",
      "models": [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro"
      ]
    },
    "openrouter": {
      "model": "deepseek/deepseek-chat-v3-0324:free",
      "base_url": "https://openrouter.ai/api/v1",
      "models": [
        "deepseek/deepseek-chat-v3-0324:free",
        "anthropic/claude-3-sonnet",
        "openai/gpt-4"
      ]
    }
  },
  "default_provider": "openrouter",
  "max_steps": 10
}
```

## � Integrazione con 1MCP Agent

Il server supporta ora la connessione al 1MCP Agent tramite HTTP/SSE. Questa integrazione permette di accedere a tutti gli strumenti e risorse disponibili nel 1MCP Agent.

### Configurazione per 1MCP Agent

Aggiungi questa sezione al tuo `mcp_config.json`:

```json
{
  "mcpServers": {
    "1mcp-agent": {
      "url": "http://localhost:3051/sse",
      "headers": {},
      "description": "1MCP Agent via HTTP/SSE",
      "disabled": false
    }
  },
  "providers": {
    // ... configurazione provider esistente
  }
}
```

### Avvio con 1MCP Agent

1. **Avvia il 1MCP Agent:**
```bash
cd /workspace/db-ready/1MCP-proxy
./start-sse.sh
```

2. **Avvia il Rest-Chatbot:**
```bash
cd /workspace/db-ready/rest-chatbot-mcp
./start.sh
```

3. **Testa l'integrazione:**
```bash
python3 test_1mcp_integration.py
```

### Configurazione con Proxy NGINX

Se stai usando il proxy NGINX del 1MCP Agent:

```json
{
  "mcpServers": {
    "1mcp-agent": {
      "url": "http://localhost:4080/sse",
      "headers": {
        "Authorization": "Bearer mcp-token-secret-2025"
      },
      "disabled": false
    }
  }
}
```

### Esempi di Query con 1MCP Agent

```bash
# Query che utilizza gli strumenti del 1MCP Agent
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Lista i file nella directory corrente e dimmi quanti sono",
    "provider": "gemini",
    "max_steps": 5
  }'
```

Per maggiori dettagli, consulta [1MCP_INTEGRATION.md](1MCP_INTEGRATION.md).

## �🚀 Avvio del Server

### Avvio Rapido

```bash
chmod +x start.sh
./start.sh
```

### Avvio Manuale

```bash
python3 mcp_server.py
```

Il server sarà disponibile su:
- **API**: http://localhost:8000
- **Documentazione**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📚 API Reference

### Endpoints Principali

#### Health Check
```http
GET /health
```

#### Lista Provider
```http
GET /api/v1/providers
```

#### Modelli di un Provider
```http
GET /api/v1/providers/{provider}/models
```

#### Query MCP
```http
POST /api/v1/query
```

### Modello di Richiesta

```json
{
  "prompt": "string",
  "provider": "gemini|openrouter",
  "model": "string",
  "max_steps": 3,
  "temperature": 0.7,
  "max_tokens": 4000,
  "system_prompt": "string"
}
```

### Modello di Risposta

```json
{
  "response": "string",
  "provider": "string",
  "model": "string",
  "steps": 3,
  "timestamp": "2025-07-16T10:30:00",
  "execution_time": 1.23
}
```

## 💡 Esempi di Utilizzo

### 1. Health Check

```bash
curl -X GET "http://localhost:8000/health" \
  -H "Accept: application/json"
```

**Risposta:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "mcp_available": true,
  "providers": [
    {
      "name": "gemini",
      "models": ["gemini-1.5-flash", "gemini-1.5-pro"],
      "default_model": "gemini-1.5-flash",
      "available": true
    }
  ],
  "uptime": "0:15:30.123456"
}
```

### 2. Query con Gemini

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Spiega cosa è il Model Context Protocol",
    "provider": "gemini",
    "model": "gemini-1.5-flash",
    "max_steps": 2
  }'
```

### 3. Query con OpenRouter (DeepSeek Gratuito)

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Crea una lista di 5 vantaggi del cloud computing",
    "provider": "openrouter",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_steps": 3,
    "temperature": 0.5
  }'
```

### 4. Query con Sistema Prompt

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analizza questo codice Python",
    "provider": "gemini",
    "model": "gemini-1.5-pro",
    "system_prompt": "Sei un esperto sviluppatore Python. Analizza il codice per bug e miglioramenti.",
    "max_steps": 3,
    "temperature": 0.3,
    "max_tokens": 1000
  }'
```

### 5. Lista Provider Disponibili

```bash
curl -X GET "http://localhost:8000/api/v1/providers" \
  -H "Accept: application/json"
```

### 6. Modelli di un Provider

```bash
curl -X GET "http://localhost:8000/api/v1/providers/gemini/models" \
  -H "Accept: application/json"
```

## 🧪 Testing

### Client Interattivo

Per un'esperienza più user-friendly, usa i client interattivi:

#### Client Python (Raccomandato)
```bash
# Avvia il client interattivo Python
python3 interactive_client.py
```

#### Client Bash (Alternativa leggera)
```bash
# Avvia il client interattivo Bash
./interactive_client.sh
```

**Caratteristiche dei client interattivi:**
- 🎯 **Selezione guidata** di provider e modelli
- 📝 **Input interattivo** per prompt e parametri
- 🎨 **Output colorato** e ben formattato
- ⚡ **Gestione automatica** delle chiamate curl
- 🔄 **Sessioni multiple** senza riavvio
- ❌ **Gestione errori** user-friendly

### Test Automatici

```bash
chmod +x test_server.sh
./test_server.sh
```

### Test Manuali

```bash
# Test semplice
curl -X GET "http://localhost:8000/api/v1/test"

# Test query di base
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Ciao, come stai?"}'
```

## 🔧 Provider Supportati

### Google Gemini
- **Modelli**: gemini-1.5-flash, gemini-1.5-pro, gemini-pro
- **Requisiti**: GOOGLE_API_KEY
- **Caratteristiche**: Veloce, efficiente, multimodale

### OpenRouter
- **Modelli**: DeepSeek (gratuito), Claude, GPT-4, Llama, Mistral
- **Requisiti**: OPENROUTER_API_KEY
- **Caratteristiche**: Accesso a molti modelli, alcuni gratuiti

## 📊 Monitoring e Logging

Il server include logging dettagliato configurabile:

```python
# Livelli di log disponibili
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR

# I log includono:
# - Timestamp delle richieste
# - Parametri delle query
# - Tempo di esecuzione
# - Errori dettagliati
# - Stato dei provider
```

## 🛡️ Sicurezza

- **API Keys**: Mai esposte nei log o risposte
- **CORS**: Configurabile per ambiente di produzione
- **Rate Limiting**: Implementabile tramite middleware
- **Timeout**: Configurabile per evitare richieste bloccate

## 🐛 Troubleshooting

### Errori Comuni

1. **"MCP non disponibile"**
   ```bash
   pip install mcp-use langchain-openai langchain-google-genai
   ```

2. **"API Key mancante"**
   - Verifica che .env contenga le chiavi corrette
   - Controlla che le variabili siano caricate

3. **"Server non raggiungibile"**
   ```bash
   python3 mcp_server.py
   curl http://localhost:8000/health
   ```

4. **"Timeout nelle richieste"**
   - Aumenta REQUEST_TIMEOUT in .env
   - Verifica la connessione internet

### Debug Mode

```bash
# Avvia in modalità debug
MCP_SERVER_DEBUG=true python3 mcp_server.py

# Oppure modifica .env
MCP_SERVER_DEBUG=true
LOG_LEVEL=DEBUG
```

### Logging delle Richieste

Il server include logging dettagliato per debugging. In modalità DEBUG, ogni richiesta include:

- **Request ID**: Identificativo univoco della richiesta
- **Parametri di input**: Prompt, provider, modello, temperature, ecc.
- **Modello target**: Provider e modello che verranno utilizzati
- **Stato inizializzazione**: Se il servizio deve essere reinizializzato
- **Modello LLM configurato**: Conferma del modello attualmente in uso
- **Tempo di esecuzione**: Durata della richiesta
- **Dimensione risposta**: Lunghezza del testo di risposta

Esempio di log di debug:
```
=== INIZIO RICHIESTA MCP ===
Request ID: 140234567890123
Prompt: Spiega cosa è il Model Context Protocol...
Provider richiesto: gemini
Modello richiesto: gemini-1.5-flash
Provider target: gemini
Modello target: gemini-1.5-flash
Modello LLM configurato: gemini-1.5-flash
Query completata in 2.34 secondi
Provider utilizzato: gemini
Modello utilizzato: gemini-1.5-flash
=== FINE RICHIESTA MCP ===
```

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT.

## 🤝 Contributi

I contributi sono benvenuti! Per favore:

1. Fork del repository
2. Crea un branch per la feature
3. Commit delle modifiche
4. Push del branch
5. Apri una Pull Request

## 📞 Supporto

Per supporto e segnalazione bug:
- Apri una Issue su GitHub
- Controlla la documentazione API su `/docs`
- Verifica i log del server per errori dettagliati

---

**Nota**: Questo server è progettato per sviluppo e testing. Per produzione, considera l'aggiunta di autenticazione, rate limiting e monitoring avanzato.
