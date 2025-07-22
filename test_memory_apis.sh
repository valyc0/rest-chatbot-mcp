#!/bin/bash

# Script per testare le nuove API di gestione memoria

echo "🚀 Test delle API di gestione memoria conversazioni"
echo "=================================================="

# Controlla se il server è già in esecuzione
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Server già in esecuzione"
else
    echo "⚠️  Server non in esecuzione. Avviandolo..."
    cd /workspace/db-ready/rest-chatbot-mcp
    
    # Avvia il server in background
    python mcp_server.py &
    SERVER_PID=$!
    
    echo "🔄 Aspettando che il server si avvii..."
    sleep 5
    
    # Verifica che il server sia attivo
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Server avviato con successo (PID: $SERVER_PID)"
    else
        echo "❌ Errore nell'avvio del server"
        kill $SERVER_PID 2>/dev/null
        exit 1
    fi
fi

echo ""
echo "🧪 Esecuzione test delle API memoria..."
echo ""

# Esegui i test
cd /workspace/db-ready/rest-chatbot-mcp

if [ -f "test_memory_curl.sh" ]; then
    echo "📋 Esecuzione test con curl..."
    ./test_memory_curl.sh
else
    echo "❌ File test_memory_curl.sh non trovato"
fi

echo ""
echo "📋 Puoi anche eseguire i test Python:"
echo "python test_memory_api.py"

echo ""
echo "🔗 Endpoint disponibili:"
echo "- GET http://localhost:8000/api/v1/memory/stats"
echo "- DELETE http://localhost:8000/api/v1/memory/clear"
echo ""
echo "📚 Vedi MEMORY_API.md per la documentazione completa"

if [ ! -z "$SERVER_PID" ]; then
    echo ""
    echo "⚠️  Server avviato in background con PID: $SERVER_PID"
    echo "Per fermarlo: kill $SERVER_PID"
fi
