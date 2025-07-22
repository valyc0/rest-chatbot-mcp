#!/bin/bash

# Script con esempi di utilizzo delle API di gestione memoria conversazioni
# Usare con il server MCP in esecuzione su localhost:8000

BASE_URL="http://localhost:8000"

echo "🧪 Esempi di utilizzo API Memoria Conversazioni"
echo "=============================================="

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzione per stampare titoli
print_title() {
    echo -e "\n${BLUE}$1${NC}"
    echo "----------------------------------------"
}

# Funzione per controllare se il server è attivo
check_server() {
    if ! curl -s "$BASE_URL/health" > /dev/null; then
        echo -e "${RED}❌ Server non raggiungibile su $BASE_URL${NC}"
        echo "Assicurati che il server MCP sia in esecuzione"
        exit 1
    fi
    echo -e "${GREEN}✅ Server MCP attivo${NC}"
}

print_title "1. 🔍 Controllo stato server"
check_server

print_title "2. 📊 Ottenere statistiche memoria conversazioni"
echo "GET /api/v1/memory/stats"
echo ""
curl -X GET "$BASE_URL/api/v1/memory/stats" \
  -H "Content-Type: application/json" | jq '.'

print_title "3. 💬 Creare alcune conversazioni di test"
echo "Creazione conversazioni per user1..."
curl -X POST "$BASE_URL/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Ciao, come stai?", "user_id": "user1"}' | jq -r '.response'

curl -X POST "$BASE_URL/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Dimmi qualcosa sui database", "user_id": "user1"}' | jq -r '.response'

echo ""
echo "Creazione conversazioni per user2..."
curl -X POST "$BASE_URL/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Che tempo fa oggi?", "user_id": "user2"}' | jq -r '.response'

print_title "4. 📈 Statistiche dopo le conversazioni"
echo "GET /api/v1/memory/stats"
echo ""
curl -X GET "$BASE_URL/api/v1/memory/stats" \
  -H "Content-Type: application/json" | jq '.'

print_title "5. 🧹 Pulire memoria per utente specifico"
echo "DELETE /api/v1/memory/clear (per user1)"
echo ""
curl -X DELETE "$BASE_URL/api/v1/memory/clear" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1"}' | jq '.'

print_title "6. 📊 Statistiche dopo pulizia parziale"
echo "GET /api/v1/memory/stats"
echo ""
curl -X GET "$BASE_URL/api/v1/memory/stats" \
  -H "Content-Type: application/json" | jq '.'

print_title "7. 🧹 Pulire memoria per tutti gli utenti"
echo "DELETE /api/v1/memory/clear (tutti gli utenti)"
echo ""
curl -X DELETE "$BASE_URL/api/v1/memory/clear" \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.'

print_title "8. 📊 Statistiche finali"
echo "GET /api/v1/memory/stats"
echo ""
curl -X GET "$BASE_URL/api/v1/memory/stats" \
  -H "Content-Type: application/json" | jq '.'

print_title "9. 🧹 Test pulizia utente inesistente"
echo "DELETE /api/v1/memory/clear (utente inesistente)"
echo ""
curl -X DELETE "$BASE_URL/api/v1/memory/clear" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "utente_che_non_esiste"}' | jq '.'

echo ""
echo -e "${GREEN}✅ Test completato!${NC}"
echo ""
echo "📝 Comandi utili:"
echo ""
echo "# Statistiche memoria:"
echo "curl -X GET $BASE_URL/api/v1/memory/stats"
echo ""
echo "# Pulire memoria utente specifico:"
echo "curl -X DELETE $BASE_URL/api/v1/memory/clear -H 'Content-Type: application/json' -d '{\"user_id\": \"user1\"}'"
echo ""
echo "# Pulire tutta la memoria:"
echo "curl -X DELETE $BASE_URL/api/v1/memory/clear -H 'Content-Type: application/json' -d '{}'"
echo ""
