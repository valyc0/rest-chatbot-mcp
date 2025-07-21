#!/bin/bash

# Test del Sistema di Prompt Configurabili
# Questo script dimostra come utilizzare i prompt da file

echo "🧪 Test del Sistema di Prompt Configurabili"
echo "=========================================="

BASE_URL="http://localhost:8000"

echo ""
echo "📋 1. Test con prompt di default (automatico)"
echo "----------------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Ciao, presentati brevemente"
  }' | jq -r '.response' | head -3

echo ""
echo "💻 2. Test con prompt coding specializzato"
echo "-------------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Come implemento una funzione di Fibonacci in Python?",
    "prompt_file": "coding"
  }' | jq -r '.response' | head -3

echo ""
echo "🗄️ 3. Test con prompt database specializzato"
echo "----------------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Come ottimizzare una query SELECT lenta?",
    "prompt_file": "database"
  }' | jq -r '.response' | head -3

echo ""
echo "❓ 4. Test con prompt inesistente (fallback a default)"
echo "------------------------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test fallback",
    "prompt_file": "inesistente"
  }' | jq -r '.response' | head -3

echo ""
echo "✋ 5. Test con prompt manuale (sovrascrive tutto)"
echo "-------------------------------------------------"
curl -s -X POST "$BASE_URL/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Spiegami brevemente cosa è Python",
    "system_prompt": "Sei un professore universitario di informatica molto formale"
  }' | jq -r '.response' | head -3

echo ""
echo "✅ Test completati!"
