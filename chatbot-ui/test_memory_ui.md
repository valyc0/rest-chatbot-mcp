# Test Plan per Chatbot UI con Gestione Memoria

## Modifiche Implementate

### 1. **Nuovi Stati e Configurazioni**
- Aggiunto `showMemoryPanel` per mostrare/nascondere il pannello memoria
- Aggiunto `memoryStats` per memorizzare le statistiche della memoria
- Aggiunto `memoryUrl` alla configurazione (default: http://localhost:8000/api/v1/memory)
- Aggiunto `userId` alla configurazione (default: 'default')

### 2. **Nuove Funzioni di Gestione Memoria**
- `getMemoryStats()`: Recupera statistiche memoria dal server
- `clearUserMemory(userId)`: Cancella memoria per utente specifico
- `clearAllMemory()`: Cancella tutta la memoria (con conferma)

### 3. **Nuovi Componenti UI**
- Pulsante "🧠 Memoria" nell'header
- Pannello memoria con:
  - Pulsante "📊 Mostra Statistiche"
  - Pulsante "🧹 Pulisci Memoria Utente"
  - Pulsante "🗑️ Pulisci Tutta la Memoria"
  - Visualizzazione statistiche dettagliate
  - Lista utenti con pulsanti individuali di cancellazione

### 4. **Pulsanti Rapidi Aggiuntivi**
- "📊 Statistiche Memoria" nei messaggi rapidi
- "🧹 Pulisci Memoria" nei messaggi rapidi

### 5. **Miglioramenti**
- Aggiunto `user_id` nelle richieste al server
- Aggiornamento automatico statistiche dopo operazioni di memoria
- Stili CSS dedicati per il pannello memoria

## Come Testare

### Prerequisiti
1. Server MCP REST attivo su http://localhost:8000
2. API memoria implementate sul server (/api/v1/memory/stats e /api/v1/memory/clear)

### Test Procedure

1. **Avvio dell'interfaccia**
   ```bash
   cd /workspace/db-ready/rest-chatbot-mcp/chatbot-ui
   npm start
   ```

2. **Test Configurazione Memoria**
   - Cliccare su "⚙️ Configurazione"
   - Verificare campi "URL Memoria" e "User ID"
   - Modificare se necessario

3. **Test Pannello Memoria**
   - Cliccare su "🧠 Memoria" nell'header
   - Cliccare su "📊 Mostra Statistiche"
   - Verificare visualizzazione statistiche

4. **Test Cancellazione Memoria**
   - Cliccare su "🧹 Pulisci Memoria Utente"
   - Verificare messaggio di conferma
   - Cliccare su "🗑️ Pulisci Tutta la Memoria"
   - Verificare richiesta di conferma

5. **Test Pulsanti Rapidi**
   - Testare "📊 Statistiche Memoria"
   - Testare "🧹 Pulisci Memoria"

## Endpoint API Utilizzati

### GET /api/v1/memory/stats
Recupera statistiche memoria:
```json
{
  "memory_limit": 30,
  "default_user_id": "default",
  "active_users": 2,
  "users": {
    "user1": {
      "message_count": 4,
      "last_message_time": "2025-01-22T10:30:45"
    }
  }
}
```

### DELETE /api/v1/memory/clear
Cancella memoria (con user_id per utente specifico, senza per tutti):
```json
// Utente specifico
{ "user_id": "user1" }

// Tutti gli utenti
{}
```

## Possibili Miglioramenti Futuri

1. **Filtri avanzati** per statistiche memoria
2. **Export/Import** memoria conversazioni
3. **Backup automatico** prima della cancellazione
4. **Notifiche real-time** per cambi memoria
5. **Grafici** per visualizzazione statistiche temporali
