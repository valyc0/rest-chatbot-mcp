# API Gestione Memoria Conversazioni

Questo documento descrive le API per la gestione della memoria delle conversazioni nel server MCP REST.

## Panoramica

Il server mantiene in memoria le conversazioni per ogni utente, con un limite configurabile tramite la variabile d'ambiente `CONVERSATION_MEMORY_LIMIT` (default: 30 messaggi per utente).

Le API permettono di:
- Visualizzare statistiche sulla memoria utilizzata
- Pulire la memoria per un utente specifico
- Pulire tutta la memoria del sistema

## Configurazione

Nel file `.env`:

```env
# Limite massimo messaggi per utente (default: 30)
CONVERSATION_MEMORY_LIMIT=30

# User ID di default se non specificato nelle richieste
DEFAULT_USER_ID=default
```

## Endpoint API

### 1. Statistiche Memoria

**Endpoint:** `GET /api/v1/memory/stats`

**Descrizione:** Restituisce statistiche dettagliate sulla memoria delle conversazioni.

**Risposta:**
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

**Campi risposta:**
- `memory_limit`: Limite massimo messaggi per utente
- `default_user_id`: ID utente di default
- `active_users`: Numero di utenti con conversazioni attive
- `users`: Dettagli per ogni utente attivo

### 2. Pulire Memoria Utente Specifico

**Endpoint:** `DELETE /api/v1/memory/clear`

**Descrizione:** Pulisce la memoria delle conversazioni per un utente specifico.

**Body richiesta:**
```json
{
  "user_id": "user1"
}
```

**Risposta successo:**
```json
{
  "success": true,
  "message": "Memoria conversazione pulita per utente: user1",
  "cleared_user": "user1",
  "users_cleared": 1
}
```

**Risposta utente inesistente:**
```json
{
  "success": true,
  "message": "Memoria conversazione pulita per utente: utente_inesistente (utente non aveva conversazioni attive)",
  "cleared_user": "utente_inesistente",
  "users_cleared": 0
}
```

### 3. Pulire Tutta la Memoria

**Endpoint:** `DELETE /api/v1/memory/clear`

**Descrizione:** Pulisce la memoria di tutte le conversazioni.

**Body richiesta:**
```json
{}
```

**Risposta:**
```json
{
  "success": true,
  "message": "Memoria di tutte le conversazioni pulita. Utenti interessati: 3",
  "cleared_user": null,
  "users_cleared": 3
}
```

## Esempi d'uso

### Con curl

#### Visualizzare statistiche
```bash
curl -X GET "http://localhost:8000/api/v1/memory/stats" \
  -H "Content-Type: application/json"
```

#### Pulire utente specifico
```bash
curl -X DELETE "http://localhost:8000/api/v1/memory/clear" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1"}'
```

#### Pulire tutta la memoria
```bash
curl -X DELETE "http://localhost:8000/api/v1/memory/clear" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Con Python (requests)

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Statistiche memoria
response = requests.get(f"{BASE_URL}/api/v1/memory/stats")
stats = response.json()
print(f"Utenti attivi: {stats['active_users']}")

# Pulire utente specifico  
clear_data = {"user_id": "user1"}
response = requests.delete(
    f"{BASE_URL}/api/v1/memory/clear",
    json=clear_data
)
result = response.json()
print(f"Operazione riuscita: {result['success']}")

# Pulire tutta la memoria
response = requests.delete(
    f"{BASE_URL}/api/v1/memory/clear",
    json={}
)
result = response.json()
print(f"Utenti puliti: {result['users_cleared']}")
```

### Con JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000";

// Statistiche memoria
async function getMemoryStats() {
  const response = await fetch(`${BASE_URL}/api/v1/memory/stats`);
  const stats = await response.json();
  console.log('Utenti attivi:', stats.active_users);
  return stats;
}

// Pulire utente specifico
async function clearUserMemory(userId) {
  const response = await fetch(`${BASE_URL}/api/v1/memory/clear`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ user_id: userId })
  });
  const result = await response.json();
  console.log('Memoria pulita:', result.message);
  return result;
}

// Pulire tutta la memoria
async function clearAllMemory() {
  const response = await fetch(`${BASE_URL}/api/v1/memory/clear`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({})
  });
  const result = await response.json();
  console.log('Memoria totale pulita:', result.users_cleared, 'utenti');
  return result;
}
```

## Test Automatici

Sono disponibili script di test per verificare il funzionamento delle API:

### Test Python
```bash
python test_memory_api.py
```

### Test Bash/curl
```bash
./test_memory_curl.sh
```

## Gestione Errori

### Errori comuni

#### 500 - Errore interno
Se il server restituisce un errore 500, controlla i log per dettagli:
```json
{
  "detail": "Errore nella pulizia della memoria: <dettagli errore>"
}
```

#### 404 - Endpoint non trovato
Verifica che l'URL sia corretto e che il server sia aggiornato con le nuove API.

## Integrazione con UI

Le API possono essere integrate nell'interfaccia web del chatbot per fornire controlli di amministrazione:

```javascript
// Componente React per controlli memoria
function MemoryControls() {
  const [stats, setStats] = useState(null);
  
  const loadStats = async () => {
    const response = await fetch('/api/v1/memory/stats');
    const data = await response.json();
    setStats(data);
  };
  
  const clearAllMemory = async () => {
    const response = await fetch('/api/v1/memory/clear', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const result = await response.json();
    alert(result.message);
    loadStats(); // Ricarica statistiche
  };
  
  return (
    <div>
      <button onClick={loadStats}>Aggiorna Statistiche</button>
      <button onClick={clearAllMemory}>Pulisci Tutta la Memoria</button>
      {stats && (
        <div>
          <p>Utenti attivi: {stats.active_users}</p>
          <p>Limite memoria: {stats.memory_limit}</p>
        </div>
      )}
    </div>
  );
}
```

## Note di Sicurezza

- Le API di pulizia memoria sono operazioni distruttive
- Non c'è modo di recuperare conversazioni pulite
- Considera l'implementazione di autenticazione per ambienti di produzione
- I log del server registrano tutte le operazioni di pulizia memoria

## Logging

Le operazioni sulla memoria vengono registrate nei log del server:

```
INFO - Memoria cancellata per utente: user1
INFO - Memoria di tutte le conversazioni cancellata  
INFO - Richiesta statistiche memoria conversazioni
```

Livello log configurabile tramite `LOG_LEVEL` nel file `.env`.
