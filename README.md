# Backend API Recomendação - Desafio Conty

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3+-orange.svg)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-6%20passed-brightgreen.svg)](./test_api.py)

Sistema de recomendação de criadores para campanhas desenvolvido para o **Desafio Conty**. Implementa algoritmo de scoring determinístico para recomendar os melhores criadores de conteúdo para campanhas específicas.

## 🚀 Quick Start

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Popular banco com dados fictícios  
python seeds.py

# 3. Executar servidor
python run_server.py
```

Servidor disponível em: **http://localhost:8000**

## � Documentação Completa

Ver **[README_LOCAL.md](./README_LOCAL.md)** para documentação completa seguindo o template do desafio Conty.

## 🔗 Links Úteis

- **API Docs**: http://localhost:8000/docs
- **Teste rápido**: `curl http://localhost:8000/api/v1/creators/count`
- **Exemplo completo**: Ver README_LOCAL.md

## 📊 Dados Ficticios

- ✅ 30 criadores com perfis variados (fintech, fitness, beauty, tech, etc.)
- ✅ 5 campanhas de exemplo (NuBank, Nike, Natura, Apple, Netflix)  
- ✅ 40+ deals históricos para contexto de performance

## 🧪 Testes

```bash
python -m pytest test_api.py -v
```

**6 testes** cobrindo endpoints principais, validação de schemas e sistema de scoring.# Backend_API_Recomendação
