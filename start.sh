#!/bin/bash

# Script per avviare il MCP Server
echo "🚀 Avvio MCP Server"
echo "=================="

# Controlla se il file .env esiste
if [ ! -f ".env" ]; then
    echo "⚠️  File .env non trovato. Creazione da template..."
    cp .env.example .env
    echo "📝 Modifica il file .env con le tue chiavi API prima di continuare."
    exit 1
fi

# Controlla se Python 3 è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Esegui ./install.sh per installare le dipendenze."
    exit 1
fi

# Controlla se le dipendenze sono installate
echo "🔍 Verifica dipendenze..."
python3 -c "import mcp_use, fastapi, uvicorn" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Dipendenze mancanti. Esegui ./install.sh per installarle."
    exit 1
fi

echo "✅ Dipendenze verificate"

# Carica le variabili d'ambiente
source .env

# Avvia il server
echo "🌟 Avvio del server MCP..."
echo "📡 Server disponibile su: http://localhost:${MCP_SERVER_PORT:-8000}"
echo "📚 Documentazione API su: http://localhost:${MCP_SERVER_PORT:-8000}/docs"
echo "🛑 Premi Ctrl+C per fermare il server"
echo ""

python3 mcp_server.py
