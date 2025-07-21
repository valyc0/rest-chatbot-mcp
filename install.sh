#!/bin/bash

# Script di installazione per MCP Server
echo "🚀 Installazione MCP Server"
echo "=========================="

# Controlla se Python 3 è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trovato. Installarlo prima di continuare."
    exit 1
fi

echo "✅ Python 3 trovato: $(python3 --version)"

# Controlla se pip è installato
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 non trovato. Installarlo prima di continuare."
    exit 1
fi

echo "✅ pip3 trovato: $(pip3 --version)"

# Installa le dipendenze
echo "📦 Installazione dipendenze..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dipendenze installate con successo"
else
    echo "❌ Errore durante l'installazione delle dipendenze"
    exit 1
fi

# Crea il file .env se non esiste
if [ ! -f ".env" ]; then
    echo "📝 Creazione file .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Modifica il file .env con le tue chiavi API"
else
    echo "✅ File .env già esistente"
fi

# Verifica che Node.js sia installato per i server MCP
if command -v node &> /dev/null; then
    echo "✅ Node.js trovato: $(node --version)"
    
    # Installa i server MCP se non già presenti
    echo "📦 Installazione server MCP..."
    npm install -g @modelcontextprotocol/server-postgres @modelcontextprotocol/server-filesystem
    
    if [ $? -eq 0 ]; then
        echo "✅ Server MCP installati con successo"
    else
        echo "⚠️  Errore durante l'installazione dei server MCP (opzionale)"
    fi
else
    echo "⚠️  Node.js non trovato - alcuni server MCP potrebbero non funzionare"
fi

echo ""
echo "🎉 Installazione completata!"
echo ""
echo "📋 Prossimi passi:"
echo "1. Modifica il file .env con le tue chiavi API:"
echo "   - OPENROUTER_API_KEY=your_openrouter_key"
echo "   - GOOGLE_API_KEY=your_google_key"
echo ""
echo "2. Avvia il server:"
echo "   python3 mcp_server.py"
echo ""
echo "3. Testa il server:"
echo "   curl http://localhost:8000/health"
echo ""
echo "📚 Documentazione API disponibile su:"
echo "   http://localhost:8000/docs"
