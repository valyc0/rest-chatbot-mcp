# 🤖 Chatbot React UI

Una moderna interfaccia web React per interagire con il server MCP (Model Context Protocol) via webhook REST API. Questo progetto fornisce un'interfaccia utente intuitiva per comunicare con un chatbot che può gestire operazioni su database, in particolare per la gestione di una rubrica telefonica.

## 🎯 Cosa fa il progetto

Il **Chatbot React UI** è un'applicazione frontend che:

- 🌐 **Interfaccia Web Moderna**: Fornisce una chat interface pulita e responsive
- 🔗 **Connessione MCP**: Si connette al server MCP tramite webhook HTTP POST
- � **Gestione Rubrica**: Specializzato per operazioni CRUD su una rubrica telefonica
- 💬 **Chat Interattiva**: Permette conversazioni naturali con il bot
- 🚀 **Messaggi Rapidi**: Bottoni predefiniti per operazioni comuni
- 🔄 **Sessione Persistente**: Mantiene il contesto della conversazione
- ⚡ **Real-time**: Indicatori di stato e risposte immediate

## 🏗️ Architettura

```
Frontend (React) → HTTP POST → Server MCP → Database Operations
     ↓                           ↓
localhost:3000              localhost:5678/webhook/aa
```

## 🚀 Compilazione e Avvio

### Prerequisiti

- **Node.js** (versione 16 o superiore)
- **npm** (incluso con Node.js)
- **Server MCP** attivo su localhost:5678

### Installazione Node.js (se necessario)

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verifica installazione
node --version
npm --version
```

### Metodo 1: Avvio Automatico (Raccomandato)

```bash
# Dalla directory principale del progetto
cd /workspace/db-ready/rest-chatbot-mcp
./start_chatbot_ui.sh
```

### Metodo 2: Avvio Manuale

```bash
# Naviga nella directory del progetto
cd /workspace/db-ready/rest-chatbot-mcp/chatbot-ui

# Installa le dipendenze
npm install

# Avvia l'applicazione in modalità sviluppo
npm start
```

### Metodo 3: Build di Produzione

```bash
cd /workspace/db-ready/rest-chatbot-mcp/chatbot-ui

# Installa dipendenze
npm install

# Crea build ottimizzato per produzione
npm run build

# Serve i file statici (richiede server web)
npx serve -s build -l 3000
```

## 🌐 Accesso all'Applicazione

Dopo l'avvio, apri il browser su: **http://localhost:3000**

## 📋 Funzionalità

- **Interfaccia moderna**: Design responsive con gradiente blu-viola e animazioni
- **Messaggi rapidi**: Bottoni per query comuni alla rubrica
- **Sessione persistente**: Mantiene la sessione con ID fisso
- **Indicatori di stato**: Mostra quando il bot sta "digitando"
- **Gestione errori**: Messaggi di errore chiari se il server non è disponibile
- **Chat pulita**: Possibilità di cancellare la cronologia
- **Test connessione**: Verifica automatica della connessione al server MCP

## 🔧 Configurazione

### Endpoint API
### Endpoint API
L'applicazione è configurata per chiamare:
```
POST http://localhost:5678/webhook/aa
```

### Payload di esempio
```json
{
  "message": "Ciao! elenca i record sulla tabella rubrica",
  "sessionId": "1"
}
```

### Modificare l'endpoint

Per cambiare l'endpoint del server MCP, modifica il file `src/App.js` alla riga 34:

```javascript
const response = await fetch('http://localhost:5678/webhook/aa', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: inputMessage,
    sessionId: sessionId
  })
});
```

## 🛠️ Sviluppo

### Struttura del progetto
```
chatbot-ui/
├── public/
│   └── index.html          # Template HTML principale
├── src/
│   ├── App.js              # Componente principale con logica chat
│   ├── App.css             # Stili dell'applicazione
│   ├── index.js            # Entry point React
│   └── index.css           # Stili globali
├── package.json            # Dipendenze e script
└── README.md               # Documentazione
```

### Dipendenze principali
- **React 18.2.0** - Libreria UI principale
- **React DOM 18.2.0** - Rendering DOM
- **React Scripts 5.0.1** - Strumenti di build e sviluppo
- **Testing Library** - Framework per testing

### Comandi disponibili
```bash
# Installa dipendenze
npm install

# Avvia in modalità sviluppo (auto-reload)
npm start

# Crea build di produzione ottimizzato
npm run build

# Esegui test unitari
npm test

# Espone configurazione webpack (irreversibile)
npm run eject
```

## 🔗 Integrazione con MCP

Il chatbot invia richieste HTTP POST al webhook MCP configurato e gestisce automaticamente diversi tipi di risposta.

### Esempi di messaggi supportati

#### Gestione Rubrica
- "Ciao! elenca i record sulla tabella rubrica"
- "Mostrami tutti i contatti"
- "Crea un nuovo contatto"
- "Cerca contatto per nome Mario"
- "Elimina contatto con ID 123"
- "Modifica contatto Mario Rossi"

#### Comandi di Sistema
- "Test di connessione"
- "Stato del server"
- "Aiuto"

### Formato Risposta del Server

Il server MCP può rispondere in diversi formati:

#### Risposta JSON
```json
{
  "output": "Testo della risposta",
  "status": "success"
}
```

#### Risposta Testo Semplice
```
Elenco contatti:
1. Mario Rossi - 123456789
2. Luigi Bianchi - 987654321
```

### Gestione Errori

L'applicazione gestisce automaticamente:
- **Errori di connessione**: Server non raggiungibile
- **Errori HTTP**: Status code 4xx/5xx
- **Timeout**: Richieste che impiegano troppo tempo
- **Errori di parsing**: Risposte malformate

## 🚨 Troubleshooting

### Server non raggiungibile
Se vedi errori di connessione:
1. **Verifica server MCP**: Assicurati che sia attivo su porta 5678
   ```bash
   cd /workspace/db-ready/rest-chatbot-mcp
   ./start.sh
   ```
2. **Controlla webhook**: Verifica che `/webhook/aa` sia configurato
3. **Problemi CORS**: Il server deve accettare richieste da localhost:3000
4. **Test manuale**: Usa il pulsante "🔧 Test Connessione" nell'interfaccia

### Problemi di installazione
Se `npm install` fallisce:
```bash
# Aggiorna npm alla versione più recente
npm install -g npm@latest

# Pulisci cache npm
npm cache clean --force

# Reinstalla completamente
rm -rf node_modules package-lock.json
npm install
```

### Problemi di avvio
Se l'applicazione non si avvia:
```bash
# Controlla se la porta 3000 è già in uso
lsof -i :3000

# Usa una porta diversa
PORT=3001 npm start
```

### Debugging
Per abilitare il debugging:
```bash
# Avvia con logging dettagliato
REACT_APP_DEBUG=true npm start

# Controlla console del browser (F12)
```

## 🎨 Personalizzazione

### Aggiungere nuovi messaggi rapidi
Modifica la sezione `quick-buttons` in `src/App.js`:

```javascript
<button 
  onClick={() => sendQuickMessage("Il tuo messaggio personalizzato")}
  className="quick-button"
>
  🔧 Tuo Bottone
</button>
```

### Modificare i colori
Edita `src/App.css` per cambiare il tema:

```css
/* Gradiente principale */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Colori dei messaggi */
.message.user {
  background: #007bff;
}

.message.bot {
  background: #f8f9fa;
}
```

### Personalizzare l'interfaccia
- **Header**: Modifica `chat-header` in `App.css`
- **Messaggi**: Personalizza `.message` styles
- **Input**: Modifica `.input-container` styles
- **Animazioni**: Aggiungi transizioni CSS custom

## 🔍 Monitoraggio

### Logs del Frontend
- **Console Browser**: Apri F12 per vedere i log
- **Network Tab**: Monitora le richieste HTTP
- **React DevTools**: Installa l'estensione per debugging

### Metriche di Performance
```bash
# Analizza bundle size
npm run build
npx bundlesize

# Lighthouse audit
npx lighthouse http://localhost:3000
```

## 🚀 Deployment

### Build di Produzione
```bash
npm run build
```

### Serve Statico
```bash
# Con serve
npx serve -s build -l 3000

# Con nginx
sudo cp -r build/* /var/www/html/
```

### Docker (Opzionale)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
```

## 📖 Documentazione API

### Endpoint principale
- **URL**: `http://localhost:5678/webhook/aa`
- **Metodo**: POST
- **Content-Type**: application/json

### Payload richiesta
```json
{
  "message": "string",      // Messaggio dell'utente
  "sessionId": "string"     // ID sessione (fisso a "1")
}
```

### Risposta attesa
```json
{
  "output": "string",       // Risposta del bot
  "status": "success|error" // Stato operazione
}
```

## 🤝 Contribuire

1. **Fork** il repository
2. **Crea** un branch per la tua feature
3. **Commit** le tue modifiche
4. **Push** al branch
5. **Apri** una Pull Request

## 📝 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file LICENSE per maggiori dettagli.

## 🆘 Supporto

Per supporto e domande:
- Apri un issue nel repository
- Controlla la documentazione del server MCP
- Verifica i log del browser (F12 → Console)

---

**Nota**: Assicurati sempre che il server MCP sia attivo prima di avviare l'interfaccia chatbot!
