# Desafio Conty – Hendel Santos / @hendelsantos

> **Local da submissão:** `submissions/hendelsantos/recommendations`

## Como rodar

- **Requisitos:** Python 3.12+ 
- **Comandos dentro desta pasta:**
  ```bash
  # 1. Criar e ativar ambiente virtual
  python -m venv .venv
  source .venv/bin/activate  # Linux/Mac
  # ou .venv\Scripts\activate  # Windows
  
  # 2. Instalar dependências
  pip install -r requirements.txt
  
  # 3. Popular banco com dados fictícios
  python seeds.py
  
  # 4. Executar servidor
  python run_server.py
  ```
- **Variáveis:** ver `.env.example` (opcional - defaults funcionam)

## Endpoints/CLI

### Teste Completo via Script
```bash
# Executar exemplos de todas as funcionalidades
./test_examples.sh
```

### POST /recommendations
Endpoint principal conforme especificação do desafio.

**Request:**
```bash
curl -X POST http://localhost:8000/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "campaign": {
      "goal": "installs",
      "tags_required": ["fintech"],
      "audience_target": {"country": "BR", "age_range": [20,34]},
      "budget_cents": 500000,
      "deadline": "2025-10-30"
    },
    "top_k": 5
  }'
```

### POST /api/v1/recommendations
Retorna ranking de criadores para uma campanha específica.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/recommendations \
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
    "top_k": 10,
    "diversity": true
  }'
```

**Response:**
```json
{
  "recommendations": [
    {
      "creator_id": "9",
      "score": 0.599,
      "fit_breakdown": {
        "tags": 0.25,
        "audience_overlap": 0.88,
        "performance": 0.66,
        "budget_fit": 1.0
      },
      "why": "Trabalha com investimentos; Audiência em BR 25-45 anos; 9/10 em confiabilidade"
    }
  ],
  "metadata": {
    "total_creators": 30,
    "scoring_version": "1.0"
  }
}
```

### GET /api/v1/creators/count
Verifica quantos criadores estão cadastrados.

### Documentação Interativa
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │ Recommendation  │    │   SQLite DB     │
│   (Routers)     │───▶│    Engine       │───▶│   (Models)      │
│                 │    │   (Scoring)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        │                       │                       │
   Pydantic              Algoritmo                SQLAlchemy
   Schemas             Determinístico               ORM
```

### Camadas:
1. **API Layer** (FastAPI + Pydantic): Validação de entrada e serialização
2. **Business Logic** (RecommendationEngine): Sistema de scoring determinístico  
3. **Data Layer** (SQLAlchemy + SQLite): Persistência de criadores, campanhas e deals

### Principais decisões:

**✅ Escolhas:**
- **SQLite**: Zero configuração, ideal para demo/desenvolvimento
- **Scoring determinístico**: Transparente, facilmente auditável e ajustável
- **FastAPI**: Auto-documentação, validação automática, performance
- **Pydantic**: Type safety e validação robusta de dados

**⚖️ Trade-offs:**
- **Simplicidade vs. Escalabilidade**: Priorizei clareza e facilidade de entendimento
- **Performance vs. Flexibilidade**: Algoritmo simples mas explicável
- **Memória vs. Disk**: SQLite carrega tudo em memória (bom para demo, limitado para produção)

### O que faria diferente com mais tempo:
- **Cache Redis** para otimização de queries repetidas
- **Sistema de ML** para otimização automática de pesos baseada em feedback
- **Postgres** para produção com índices otimizados
- **Métricas de diversidade** para evitar recomendações muito similares
- **Sistema de A/B testing** para validar melhorias no algoritmo

## Testes

```bash
# Executar testes unitários
python -m pytest test_api.py -v

# Coverage (6 testes cobrindo endpoints principais)
pytest --cov=app test_api.py
```

### O que cobre:
- ✅ Health checks e endpoints básicos
- ✅ Validação de schemas de entrada
- ✅ Sistema de scoring com dados fictícios
- ✅ Responses estruturadas corretamente
- ✅ Edge cases (tags vazias, requests inválidos)

## IA/Libraries

### Onde usei IA:
- **GitHub Copilot**: Geração inicial de boilerplate, schemas Pydantic e estrutura de testes, todo projeto estruturado
- **ChatGPT**: Brainstorming de nomes para criadores fictícios e definição de tags relevantes

### O que é meu vs. de terceiros:

**💡 Minha implementação:**
- **Sistema de scoring completo** (`recommendation_engine.py`): Lógica de negócio, pesos, normalizações
- **Algoritmo de matching**: Jaccard similarity, sobreposição de audiência, função sigmoid
- **Estrutura de dados**: Design das tabelas e relacionamentos
- **Seeds inteligentes**: Geração de dados fictícios realistas com distribuições coerentes
- **Justificativas legíveis**: Sistema de explicação do por que cada criador foi recomendado

**📚 Libraries de terceiros:**
- **FastAPI/Uvicorn**: Framework web e servidor ASGI
- **SQLAlchemy**: ORM para acesso ao banco
- **Pydantic**: Validação e serialização de dados
- **Pytest/httpx**: Framework de testes e client HTTP

### Detalhes do Sistema de Scoring:

**Pesos e Normalizações:**
```python
WEIGHTS = {
    'tags': 0.40,         # Jaccard similarity entre tags
    'audience': 0.25,     # Geo (50%) + Idade (50%) 
    'performance': 0.20,  # Views + CTR + CVR (sigmoid)
    'budget': 0.10,       # Fit dentro da faixa de preço
    'reliability': 0.05   # Score de confiabilidade direto
}
```

**Normalização Sigmoid para Performance:**
- Evita que outliers dominem o score
- `sigmoid(value, midpoint) = 1 / (1 + exp(-(value - midpoint) / (midpoint × 0.5)))`
- Midpoints: 100k views, 3% CTR, 2% CVR

**Explicabilidade:**
- Cada score é decomponível em fatores específicos
- Justificativas automáticas baseadas nos scores individuais
- Metadata incluindo versão do algoritmo para auditoria