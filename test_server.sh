#!/bin/bash

# Script per testare il MCP Server
echo "🧪 Test MCP Server"
echo "================="

SERVER_URL="http://localhost:8000"

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzione per test HTTP
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -e "\n${BLUE}📡 Test: $description${NC}"
    echo "   $method $endpoint"
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$SERVER_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$SERVER_URL$endpoint")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "   ${GREEN}✅ Successo ($http_code)${NC}"
        echo "   Risposta: $(echo "$body" | head -c 200)..."
    else
        echo -e "   ${RED}❌ Errore ($http_code)${NC}"
        echo "   Errore: $body"
    fi
}

echo -e "\n${YELLOW}⏳ Verifico che il server sia in esecuzione...${NC}"
if ! curl -s "$SERVER_URL/health" > /dev/null 2>&1; then
    echo -e "${RED}❌ Server non raggiungibile su $SERVER_URL${NC}"
    echo "   Assicurati che il server sia in esecuzione:"
    echo "   python3 mcp_server.py"
    exit 1
fi
echo -e "${GREEN}✅ Server attivo${NC}"

# Test 1: Stato di salute
test_endpoint "GET" "/health" "" "Controllo stato server"

# Test 2: Lista provider disponibili
test_endpoint "GET" "/api/v1/providers" "" "Lista provider disponibili"

# Test 3: Modelli OpenRouter
test_endpoint "GET" "/api/v1/providers/openrouter/models" "" "Modelli OpenRouter"

# Test 4: Modelli Gemini
test_endpoint "GET" "/api/v1/providers/gemini/models" "" "Modelli Gemini"

# Test 5: Configurazione
test_endpoint "GET" "/api/v1/config" "" "Configurazione server"

# Test 6: Test endpoint
test_endpoint "GET" "/api/v1/test" "" "Endpoint di test"

# Test 7: Query con provider predefinito
test_data_default='{
    "prompt": "Saluta e presenta brevemente le tue capacità MCP",
    "max_steps": 2
}'
test_endpoint "POST" "/api/v1/query" "$test_data_default" "Query con provider predefinito"

# Test 8: Query con OpenRouter (DeepSeek - GRATUITO)
test_data_deepseek='{
    "prompt": "Che cosa è MCP (Model Context Protocol)?",
    "provider": "openrouter",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_steps": 2
}'
test_endpoint "POST" "/api/v1/query" "$test_data_deepseek" "Query con OpenRouter (DeepSeek)"

# Test 9: Query con Gemini
test_data_gemini='{
    "prompt": "Spiega brevemente cosa puoi fare con MCP",
    "provider": "gemini",
    "model": "gemini-1.5-flash",
    "max_steps": 2
}'
test_endpoint "POST" "/api/v1/query" "$test_data_gemini" "Query con Gemini"

# Test 10: Query con parametri personalizzati
test_data_custom='{
    "prompt": "Crea una lista di 3 vantaggi di MCP",
    "provider": "openrouter",
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "max_steps": 3,
    "temperature": 0.3,
    "max_tokens": 500,
    "system_prompt": "Sei un esperto di protocolli di comunicazione AI. Rispondi in modo conciso e tecnico."
}'
test_endpoint "POST" "/api/v1/query" "$test_data_custom" "Query con parametri personalizzati"

# Test 11: Query con provider non valido
test_data_invalid='{
    "prompt": "Test con provider inesistente",
    "provider": "invalid-provider",
    "model": "non-existent-model",
    "max_steps": 1
}'
test_endpoint "POST" "/api/v1/query" "$test_data_invalid" "Test gestione errore provider invalido"

echo -e "\n${BLUE}📊 Riepilogo Test${NC}"
echo "========================="
echo "✅ Test endpoint di stato completati"
echo "✅ Test endpoint provider completati"
echo "✅ Test query multi-provider completati"
echo "✅ Test gestione errori completati"

echo -e "\n${YELLOW}💡 Suggerimenti:${NC}"
echo "1. Verifica che le API keys siano configurate nel file .env"
echo "2. Controlla i log del server per eventuali errori dettagliati"
echo "3. Consulta la documentazione API su http://localhost:8000/docs"
echo "4. Per test interattivi usa: curl -X POST -H 'Content-Type: application/json' -d '{\"prompt\":\"test\"}' $SERVER_URL/api/v1/query"

echo -e "\n${GREEN}🎉 Test completati!${NC}"
