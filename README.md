# Rest Chatbot MCP

Un server REST basato su FastAPI che integra il Model Context Protocol (MCP) con provider AI multipli per l'interazione con database e sistemi esterni.

## Descrizione del Progetto

Questo progetto fornisce un'API REST per interagire con database e sistemi attraverso MCP (Model Context Protocol) utilizzando diversi provider AI come Gemini e OpenRouter. Il server può eseguire query su database, analizzare dati e fornire risposte intelligenti attraverso modelli di linguaggio avanzati.

### Caratteristiche principali:

- **API REST** con FastAPI per interazioni programmatiche
- **Supporto Multi-provider**: Gemini, OpenRouter e altri provider AI
- **Integrazione MCP**: Connessione con server MCP per database e filesystem
- **UI Web**: Interfaccia utente React per interazioni facili
- **Configurazione flessibile**: Gestione semplice di chiavi API e configurazioni

## Configurazione

### 1. Installazione

Esegui lo script di installazione per installare tutte le dipendenze:

```bash
./install.sh
```

Questo script:
- Verifica Python 3 e pip
- Installa le dipendenze Python da `requirements.txt`
- Crea il file `.env` da template
- Installa server MCP globali se Node.js è disponibile

### 2. Configurazione Chiavi API

Dopo l'installazione, modifica il file `.env` con le tue chiavi API:

```env
# Gemini API Key (da Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# OpenRouter API Key (da openrouter.ai)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Configurazione Server
MCP_SERVER_PORT=8000
LOG_LEVEL=INFO
```

#### Dove ottenere le chiavi API:

**Gemini API Key:**
1. Vai su [Google AI Studio](https://aistudio.google.com)
2. Accedi con il tuo account Google
3. Vai su "Get API Key" nel menu
4. Crea una nuova chiave API
5. Copia la chiave nel file `.env`

**OpenRouter API Key:**
1. Registrati su [OpenRouter](https://openrouter.ai)
2. Vai su "Keys" nel dashboard
3. Crea una nuova chiave API
4. Copia la chiave nel file `.env`

### 3. Configurazione MCP

Il file `mcp_config.json` contiene le configurazioni per i provider AI e i server MCP:

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
    "gemini": {
      "api_key": "",
      "model": "gemini-2.5-flash",
      "base_url": "https://generativelanguage.googleapis.com"
    },
    "openrouter": {
      "api_key": "",
      "model": "deepseek/deepseek-chat-v3-0324:free",
      "base_url": "https://openrouter.ai/api/v1"
    }
  }
}
```

## Avvio del Server

Per avviare il server MCP:

```bash
./start.sh
```

Il server sarà disponibile su:
- **API**: http://localhost:8000
- **Documentazione**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Principale Endpoint Query

#### POST /api/v1/query

Endpoint principale per inviare query al sistema MCP.

**Parametri:**
- `prompt` (string): Il prompt o query da processare
- `provider` (string): Provider AI da utilizzare ("gemini" o "openrouter")
- `model` (string): Modello specifico da utilizzare
- `max_steps` (integer, optional): Numero massimo di passi per il reasoning (default: 10)
- `temperature` (float, optional): Temperatura per la generazione (default: 0.1)

### Altri Endpoints

- `GET /health` - Stato del server
- `GET /api/v1/providers` - Lista provider disponibili
- `GET /api/v1/providers/{provider}/models` - Modelli per un provider
- `GET /api/v1/config` - Configurazione attuale

## Esempi di Chiamate cURL

### 1. Query Database con Gemini

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "elenca i record nella tabella rubrica",
    "provider": "gemini",
    "model": "gemini-2.5-flash",
    "max_steps": 15,
    "temperature": 0.1
  }'
```

### 2. Analisi Dati con OpenRouter

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "analizza le vendite dell'\''ultimo mese e mostra un riassunto",
    "provider": "openrouter",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_steps": 20,
    "temperature": 0.2
  }'
```

### 3. Query con Modello Anthropic Claude

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "crea una query SQL per trovare i clienti più attivi",
    "provider": "openrouter",
    "model": "anthropic/claude-3-sonnet",
    "max_steps": 10,
    "temperature": 0.0
  }'
```

### 4. Operazioni sui File

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "leggi il contenuto del file config.json e spiega la sua struttura",
    "provider": "gemini",
    "model": "gemini-1.5-pro",
    "max_steps": 5,
    "temperature": 0.1
  }'
```

### 5. Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

### 6. Lista Provider Disponibili

```bash
curl -X GET "http://localhost:8000/api/v1/providers"
```

### 7. Modelli per un Provider

```bash
curl -X GET "http://localhost:8000/api/v1/providers/gemini/models"
```

### 8. Gestione Memoria Conversazioni

#### 8.1. Visualizzare Statistiche Memoria

```bash
curl -X GET "http://localhost:8000/api/v1/memory/stats"
```

Risposta:
```json
{
  "memory_limit": 30,
  "default_user_id": "default",
  "active_users": 2,
  "users": {
    "user1": {
      "message_count": 4,
      "last_message_time": "2025-01-22T10:30:45"
    },
    "user2": {
      "message_count": 2,
      "last_message_time": "2025-01-22T10:25:30"
    }
  }
}
```

#### 8.2. Pulire Memoria Utente Specifico

```bash
curl -X DELETE "http://localhost:8000/api/v1/memory/clear" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1"}'
```

Risposta:
```json
{
  "success": true,
  "message": "Memoria conversazione pulita per utente: user1",
  "cleared_user": "user1",
  "users_cleared": 1
}
```

#### 8.3. Pulire Memoria di Tutti gli Utenti

```bash
curl -X DELETE "http://localhost:8000/api/v1/memory/clear" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Risposta:
```json
{
  "success": true,
  "message": "Memoria di tutte le conversazioni pulita. Utenti interessati: 3",
  "cleared_user": null,
  "users_cleared": 3
}
```

## Chatbot UI

Il progetto include una interfaccia web React per interagire facilmente con il server MCP.

### Configurazione e Avvio UI

1. **Installazione dipendenze UI:**
   ```bash
   cd chatbot-ui
   npm install
   ```

2. **Avvio dell'interfaccia web:**
   ```bash
   cd chatbot-ui
   ./start.sh
   ```
   
   Oppure direttamente:
   ```bash
   cd chatbot-ui
   npm start
   ```

3. **Accesso all'UI:**
   - L'interfaccia sarà disponibile su http://localhost:3000
   - Assicurati che il server MCP sia in esecuzione su http://localhost:8000

### Utilizzo dell'Interfaccia Web

L'interfaccia chatbot UI permette di:

- **Chat Interattiva**: Invia messaggi e ricevi risposte dal sistema MCP
- **Selezione Provider**: Scegli tra Gemini, OpenRouter e altri provider
- **Configurazione Modelli**: Seleziona modelli specifici per ogni provider
- **Parametri Avanzati**: Configura temperatura, max_steps e altri parametri
- **Storico Conversazioni**: Visualizza e gestisci le conversazioni precedenti
- **Preview Risposte**: Visualizzazione formattata delle risposte del sistema

### Struttura dell'UI

```
chatbot-ui/
├── public/          # File statici
├── src/             # Codice sorgente React
│   ├── components/  # Componenti React
│   ├── services/    # Servizi per API calls
│   └── App.js       # Componente principale
├── package.json     # Dipendenze Node.js
└── start.sh         # Script di avvio
```

## Risoluzione Problemi

### Server non si avvia

1. Verifica che le dipendenze siano installate:
   ```bash
   ./install.sh
   ```

2. Controlla il file `.env` e le chiavi API

3. Verifica che la porta 8000 non sia occupata:
   ```bash
   lsof -i :8000
   ```

### UI non si connette al server

1. Assicurati che il server MCP sia in esecuzione su localhost:8000
2. Controlla che non ci siano problemi CORS
3. Verifica i log del browser per errori di rete

### Errori API

- Controlla i log del server per errori dettagliati
- Verifica che le chiavi API siano corrette e valide
- Assicurati che il server MCP di destinazione sia raggiungibile

## Server MCP Supportati

Il sistema supporta diversi tipi di server MCP:

- **Database**: PostgreSQL, MySQL, SQLite
- **Filesystem**: Accesso a file e directory
- **1MCP Agent**: Server MCP avanzato con capacità multiple
- **Servizi Web**: API REST e servizi esterni

## Contributi

Per contribuire al progetto:

1. Fai fork del repository
2. Crea un branch per la tua feature
3. Implementa le modifiche
4. Aggiungi test se necessario
5. Invia una pull request

## Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file LICENSE per dettagli.