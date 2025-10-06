#!/bin/bash
# Script de teste da API - Exemplo prático do desafio

echo "🚀 Testando API de Recomendações de Criadores"
echo "=============================================="

BASE_URL="http://localhost:8000"

echo ""
echo "1️⃣ Health Check"
curl -s "$BASE_URL/health" | jq .

echo ""
echo "2️⃣ Contagem de Criadores"
curl -s "$BASE_URL/api/v1/creators/count" | jq .

echo ""
echo "3️⃣ Recomendação para Campanha Fintech"
curl -s -X POST "$BASE_URL/api/v1/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign": {
      "goal": "installs",
      "tags_required": ["fintech", "investimentos"],
      "audience_target": {
        "country": "BR",
        "age_range": [25, 45]
      },
      "budget_cents": 1000000,
      "deadline": "2025-12-31"
    },
    "top_k": 5,
    "diversity": true
  }' | jq '.recommendations[:3] | .[] | {creator_id, score, why}'

echo ""
echo "4️⃣ Recomendação para Campanha Fitness"
curl -s -X POST "$BASE_URL/api/v1/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign": {
      "goal": "awareness", 
      "tags_required": ["fitness", "corrida"],
      "audience_target": {
        "country": "BR",
        "age_range": [18, 35]
      },
      "budget_cents": 2000000,
      "deadline": "2025-12-31"
    },
    "top_k": 3
  }' | jq '.recommendations[] | {creator_id, score, fit_breakdown: {tags: .fit_breakdown.tags, audience: .fit_breakdown.audience_overlap}}'

echo ""
echo "✅ Testes concluídos! Acesse http://localhost:8000/docs para mais opções."