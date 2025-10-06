# 🏆 Desafio Conty - Sistema de Recomendação

> **Repositório:** https://github.com/hendelsantos/Backend_API_Recomenda-o

## ⚡ Teste Rápido (2 minutos)

```bash
# 1. Clonar e entrar no diretório
git clone https://github.com/hendelsantos/Backend_API_Recomenda-o.git
cd Backend_API_Recomenda-o

# 2. Setup (30 segundos)
pip install -r requirements.txt
python seeds.py
python run_server.py

# 3. Testar endpoint principal (em outro terminal)
curl -X POST http://localhost:8000/recommendations \
  -H "Content-Type: application/json" \
  -d '{"campaign":{"goal":"installs","tags_required":["fintech"],"audience_target":{"country":"BR","age_range":[20,34]},"budget_cents":500000,"deadline":"2025-10-30"},"top_k":3}'
```

## 🎯 Critérios Atendidos

| Requisito | Status | Detalhes |
|-----------|---------|----------|
| **Endpoint HTTP** | ✅ | `POST /recommendations` |
| **Entrada JSON** | ✅ | Formato exato da especificação |
| **Saída ordenada** | ✅ | Lista com `{id, score, why}` |
| **50-500 criadores** | ✅ | 100 criadores gerados |
| **Scoring determinístico** | ✅ | Pesos fixos documentados |
| **Justificativas** | ✅ | Explicações automáticas |
| **README_LOCAL.md** | ✅ | Template seguido exatamente |

## 📊 Dados Gerados

- **100 criadores** com 8 nichos diferentes
- **5 campanhas** (fintech, fitness, beauty, tech, streaming)
- **49 deals históricos** para contexto
- **Métricas realistas** baseadas no mercado

## 🧮 Sistema de Scoring

```python
WEIGHTS = {
    'tags': 0.40,         # Jaccard similarity
    'audience': 0.25,     # Sobreposição demográfica  
    'performance': 0.20,  # Views, CTR, CVR (sigmoid)
    'budget': 0.10,       # Adequação de preço
    'reliability': 0.05   # Confiabilidade
}
```

## 🔗 Links Importantes

- **📚 Documentação Completa**: [README_LOCAL.md](./README_LOCAL.md)
- **🔬 API Docs**: http://localhost:8000/docs
- **🧪 Testes**: `python -m pytest test_api.py -v`
- **📋 Avaliação**: [EVALUATION.md](./EVALUATION.md)

## 💡 Destaques Técnicos

- **Transparência**: Sistema explicável com breakdown de scores
- **Qualidade**: 6 testes automatizados, 100% funcionais
- **Performance**: ~500ms para processar 100 criadores
- **Documentação**: Template do desafio seguido rigorosamente

---

**Desenvolvido por:** Hendel Santos (@hendelsantos)  
**Tempo de desenvolvimento:** ~3 horas  
**Status:** ✅ Todos os critérios atendidos