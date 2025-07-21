# Chatbot UI Generica

Questa è una versione generica dell'interfaccia chatbot che può essere configurata per comunicare con diversi server API.

## Configurazione

L'interfaccia include un pannello di configurazione accessibile tramite il pulsante "⚙️ Configurazione" nell'header. Puoi configurare i seguenti parametri:

### Parametri di Configurazione

1. **URL Server**: L'endpoint dell'API del server (esempio: `http://localhost:8000/api/v1/query`)
2. **Campo Risposta**: Il campo JSON della risposta da cui estrarre il messaggio (esempio: `response`)
3. **Provider**: Il provider dell'AI da utilizzare (esempio: `gemini`)
4. **Modello**: Il modello specifico da utilizzare (esempio: `gemini-2.5-flash`)
5. **Max Steps**: Numero massimo di passaggi per l'elaborazione (esempio: `15`)
6. **Temperature**: Controllo della creatività delle risposte (0.0-2.0, esempio: `0.1`)

### Configurazione Predefinita

L'interfaccia è preconfigurata per funzionare con il server MCP che accetta richieste nel formato:

```json
{
  "prompt": "tua domanda",
  "provider": "gemini",
  "model": "gemini-2.5-flash",
  "max_steps": 15,
  "temperature": 0.1
}
```

E restituisce risposte nel formato:

```json
{
  "response": "risposta del bot",
  "provider": "gemini",
  "model": "gemini-2.5-flash",
  "steps": 15,
  "timestamp": "2025-07-21T06:42:47.408247",
  "execution_time": 3.179445
}
```

## Utilizzo

1. **Avvio dell'applicazione**:
   ```bash
   cd /workspace/db-ready/webhook-postgres-chat/chatbot-ui
   npm start
   ```

2. **Configurazione**:
   - Clicca sul pulsante "⚙️ Configurazione"
   - Modifica i parametri secondo le tue esigenze
   - Clicca "💾 Salva" per salvare la configurazione

3. **Test della connessione**:
   - Usa il pulsante "🔧 Test Connessione" per verificare che il server sia raggiungibile

4. **Messaggi rapidi**:
   - Usa i pulsanti di messaggio rapido per testare rapidamente la funzionalità
   - Personalizza i messaggi modificando il codice sorgente

## Personalizzazione

### Aggiungere nuovi messaggi rapidi

Modifica la sezione `quick-buttons` in `src/App.js`:

```javascript
<button 
  onClick={() => sendQuickMessage("Il tuo messaggio personalizzato")}
  className="quick-button"
>
  🔄 Tuo Messaggio
</button>
```

### Modificare il formato della richiesta

Se il tuo server API accetta un formato diverso, modifica la sezione `requestBody` nella funzione `sendMessage`:

```javascript
const requestBody = {
  // Personalizza questo oggetto secondo le API del tuo server
  prompt: inputMessage,
  provider: config.provider,
  model: config.model,
  max_steps: config.maxSteps,
  temperature: config.temperature
};
```

### Gestire diversi formati di risposta

L'interfaccia cerca automaticamente il campo specificato in "Campo Risposta" nella configurazione, con fallback ai campi comuni:
- `output`
- `response` 
- `message`
- `result`
- `data`

## Salvataggio Configurazione

La configurazione viene salvata automaticamente nel localStorage del browser e ricaricata ad ogni avvio dell'applicazione.

## Esempi di Configurazione

### Server MCP Standard
- **URL Server**: `http://localhost:8000/api/v1/query`
- **Campo Risposta**: `response`

### Server Webhook N8N
- **URL Server**: `http://localhost:5678/webhook/aa`
- **Campo Risposta**: `output`

### Server OpenAI-compatible
- **URL Server**: `http://localhost:1234/v1/chat/completions`
- **Campo Risposta**: `choices[0].message.content`

## Risoluzione Problemi

1. **Errore di connessione**: Verifica che l'URL del server sia corretto e che il server sia in esecuzione
2. **Risposta vuota**: Controlla che il "Campo Risposta" sia configurato correttamente
3. **Errori CORS**: Assicurati che il server permetta le richieste dall'origine del frontend

## Sviluppo

L'applicazione è basata su React e può essere estesa facilmente per supportare nuove funzionalità:

- Autenticazione
- Storia delle conversazioni
- Export/Import delle configurazioni
- Temi personalizzati
- Supporto per file upload
- Integrazione con altri servizi
