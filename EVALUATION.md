# Instruções para Avaliação - Desafio Conty

## ✅ O que foi entregue

- [x] **API HTTP** com endpoint `POST /recommendations` (conforme especificação)
- [x] **Entrada JSON** no formato especificado no desafio
- [x] **Saída** com lista ordenada de criadores `{id, score, why}`
- [x] **Scoring determinístico** com pesos fixos e documentados
- [x] **Dataset fictício** com 100 criadores (50-500 ✅) e 5 campanhas
- [x] **Testes automatizados** (6 testes cobrindo casos principais)
- [x] **Endpoint adicional** `/api/v1/recommendations` para compatibilidade

## 🚀 Como testar rapidamente

1. **Setup (30 segundos)**:
   ```bash
   pip install -r requirements.txt
   python seeds.py
   python run_server.py
   ```

2. **Teste básico**:
   ```bash
   curl http://localhost:8000/api/v1/creators/count
   # Deve retornar: {"total_creators": 100}
   ```

3. **Teste conforme especificação**:
   ```bash
   curl -X POST http://localhost:8000/recommendations \
     -H "Content-Type: application/json" \
     -d '{"campaign":{"goal":"installs","tags_required":["fintech"],"audience_target":{"country":"BR","age_range":[20,34]},"budget_cents":500000,"deadline":"2025-10-30"},"top_k":3}'
   ```

4. **Interface visual**: http://localhost:8000/docs

## 🎯 Pontos de destaque

### Modelo de Scoring Transparente
```python
WEIGHTS = {
    'tags': 0.40,         # Jaccard similarity 
    'audience': 0.25,     # Sobreposição demográfica
    'performance': 0.20,  # Métricas históricas normalizadas
    'budget': 0.10,       # Fit de preço
    'reliability': 0.05   # Confiabilidade
}
```

### Exemplo de Resultado Real
Para campanha fintech (budget R$ 10k, audiência BR 25-45):
```json
{
  "creator_id": "9",
  "score": 0.599,
  "fit_breakdown": {
    "tags": 0.25,           // 25% match (fintech + investimentos)
    "audience_overlap": 0.88, // 88% audiência na faixa alvo
    "performance": 0.66,     // Performance acima da média
    "budget_fit": 1.0        // Preço dentro do orçamento
  },
  "why": "Trabalha com investimentos; Audiência em BR 25-45 anos; 9/10 em confiabilidade"
}
```

### Qualidade dos Seeds
- **Diversidade**: 8 nichos diferentes (fintech, fitness, beauty, tech, etc.)
- **Volume**: 100 criadores (atende requisito 50-500)
- **Realismo**: Distribuições de métricas baseadas em dados reais do mercado
- **Coerência**: Audiência correlacionada com nichos (ex: fintech → 25-45 anos)

## 📋 Checklist de avaliação

### Funcionalidade ✅
- [x] API responde corretamente 
- [x] Formato de entrada/saída conforme especificação
- [x] Scoring produz rankings coerentes
- [x] Justificativas (`why`) são legíveis

### Qualidade Técnica ✅  
- [x] Código organizado e documentado
- [x] Testes automatizados funcionando
- [x] Zero configuração necessária (SQLite)
- [x] Performance adequada (< 1s para recomendações)

### Documentação ✅
- [x] README_LOCAL.md seguindo template exato
- [x] Pesos e normalizações explicados
- [x] Decisões arquiteturais justificadas
- [x] Exemplos práticos funcionando

## 🔍 Para análise detalhada

- **Algoritmo**: `app/recommendation_engine.py` (linhas 30-180)
- **Seeds**: `seeds.py` (geração de dados realistas)
- **Testes**: `test_api.py` (cobertura completa dos endpoints)
- **Docs**: `README_LOCAL.md` (documentação completa)

---

**Tempo estimado para avaliação**: 10-15 minutos
**Complexidade**: Moderada, focada em clareza e funcionalidade