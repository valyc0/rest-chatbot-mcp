# Sistema di Prompt Configurabili

Il server MCP ora supporta un sistema di prompt configurabili che permette di caricare automaticamente prompt di sistema da file, migliorando la precisione e la specializzazione delle risposte AI.

## 🎯 Come Funziona

Il sistema legge automaticamente i prompt da file nella directory `prompts/` e li applica alle richieste in base a diverse modalità:

### 1. Prompt di Default Automatico
Se non viene specificato nessun prompt di sistema, il server carica automaticamente il prompt da `prompts/default.txt`

### 2. Prompt Specializzati
Puoi specificare un prompt specializzato usando il parametro `prompt_file`

### 3. Prompt Manuale
Puoi sempre sovrascrivere tutto specificando direttamente `system_prompt`

## 📁 File di Prompt Disponibili

### `default.txt`
Prompt generale per conversazioni di base:
```
Sei un assistente AI intelligente e utile. Rispondi sempre in modo preciso, cortese e dettagliato...
```

### `coding.txt`
Prompt specializzato per sviluppo software:
```
Sei un esperto sviluppatore di software con decenni di esperienza...
```

### `database.txt`
Prompt specializzato per database e SQL:
```
Sei un esperto Database Administrator (DBA) con ampia esperienza...
```

## 🚀 Esempi di Utilizzo

### 1. Usando il Prompt di Default (Automatico)
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Ciao, come stai?"
  }'
```
→ Usa automaticamente `prompts/default.txt`

### 2. Usando un Prompt Specializzato
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Come implemento una funzione di ordinamento in Python?",
    "prompt_file": "coding"
  }'
```
→ Usa `prompts/coding.txt`

### 3. Per Database e SQL
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Come ottimizzare questa query SQL?",
    "prompt_file": "database"
  }'
```
→ Usa `prompts/database.txt`

### 4. Prompt Manuale (Sovrascrive tutto)
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Spiegami la fisica quantistica",
    "system_prompt": "Sei un professore di fisica con dottorato in meccanica quantistica"
  }'
```
→ Usa il prompt specificato direttamente

## ➕ Aggiungere Nuovi Prompt

Per aggiungere un nuovo prompt specializzato:

1. Crea un file nella directory `prompts/` con estensione `.txt`
2. Scrivi il prompt di sistema desiderato
3. Usa il nome del file (senza estensione) nel parametro `prompt_file`

Esempio:
```bash
# Crea prompts/matematica.txt
echo "Sei un professore di matematica esperto in algebra e calcolo..." > prompts/matematica.txt

# Usalo nelle richieste
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Risolvi questa equazione differenziale",
    "prompt_file": "matematica"
  }'
```

## 🔧 Struttura del Request

Il nuovo parametro `prompt_file` è stato aggiunto al modello `MCPQueryRequest`:

```json
{
  "prompt": "string",              // Richiesto: La domanda/richiesta dell'utente
  "provider": "string",            // Opzionale: Provider AI (gemini, openrouter)
  "model": "string",               // Opzionale: Modello specifico
  "max_steps": 3,                  // Opzionale: Numero massimo di passi MCP
  "temperature": 0.7,              // Opzionale: Temperatura per la generazione
  "max_tokens": 4000,              // Opzionale: Numero massimo di token
  "system_prompt": "string",       // Opzionale: Prompt di sistema manuale
  "prompt_file": "string"          // Opzionale: Nome del file di prompt (senza .txt)
}
```

## 📋 Priorità dei Prompt

Il sistema applica i prompt in questo ordine di priorità:

1. **`system_prompt`** - Se specificato, sovrascrive tutto
2. **`prompt_file`** - Se specificato, carica il prompt dal file
3. **`default.txt`** - Se nessuno dei precedenti, usa il prompt di default
4. **Nessun prompt** - Se nemmeno default.txt esiste

## 🔍 Logging

Il server registra automaticamente quale prompt viene utilizzato:

```
INFO:mcp_server:Utilizzando prompt da file: coding.txt
INFO:mcp_server:Utilizzando prompt di default da file
WARNING:mcp_server:File prompt matematica.txt non trovato, uso prompt di default
```

Questo permette di monitorare facilmente quale prompt viene applicato a ogni richiesta.
