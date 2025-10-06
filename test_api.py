# Testes para o sistema de recomendação
import pytest
import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base, Creator, Campaign
import tempfile
import os

# Criar banco de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    """Setup e teardown do banco de teste"""
    Base.metadata.create_all(bind=engine)
    
    # Criar dados de teste
    db = TestingSessionLocal()
    
    # Criador de teste
    test_creator = Creator(
        name="Criador Teste",
        tags=["fintech", "investimentos"],
        audience_age=[25, 30, 35, 40],
        audience_location=["BR"],
        avg_views=100000,
        ctr=0.03,
        cvr=0.02,
        price_min=500000,  # R$ 5.000
        price_max=1500000,  # R$ 15.000
        reliability_score=0.9
    )
    
    db.add(test_creator)
    db.commit()
    db.close()
    
    yield
    
    Base.metadata.drop_all(bind=engine)

def test_health_endpoint():
    """Testa endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Testa endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Sistema de Recomendação" in response.json()["message"]

def test_creators_count_endpoint(setup_database):
    """Testa endpoint de contagem de criadores"""
    response = client.get("/api/v1/creators/count")
    assert response.status_code == 200
    assert response.json()["total_creators"] == 1

def test_recommendations_endpoint(setup_database):
    """Testa endpoint principal de recomendações"""
    request_data = {
        "campaign": {
            "goal": "installs",
            "tags_required": ["fintech"],
            "audience_target": {
                "country": "BR",
                "age_range": [25, 45]
            },
            "budget_cents": 1000000,
            "deadline": "2025-12-31"
        },
        "top_k": 5,
        "diversity": True
    }
    
    response = client.post("/api/v1/recommendations", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "recommendations" in data
    assert "metadata" in data
    assert len(data["recommendations"]) <= 5
    assert data["metadata"]["total_creators"] == 1
    
    # Verificar estrutura da recomendação
    if data["recommendations"]:
        rec = data["recommendations"][0]
        assert "creator_id" in rec
        assert "score" in rec
        assert "fit_breakdown" in rec
        assert "why" in rec
        
        # Verificar fit_breakdown
        breakdown = rec["fit_breakdown"]
        assert "tags" in breakdown
        assert "audience_overlap" in breakdown
        assert "performance" in breakdown
        assert "budget_fit" in breakdown

def test_recommendations_invalid_request():
    """Testa request inválido"""
    invalid_request = {
        "campaign": {
            "goal": "installs",
            # Faltando campos obrigatórios
        }
    }
    
    response = client.post("/api/v1/recommendations", json=invalid_request)
    assert response.status_code == 422  # Validation error

def test_recommendations_empty_tags(setup_database):
    """Testa recomendação com tags vazias"""
    request_data = {
        "campaign": {
            "goal": "awareness",
            "tags_required": [],
            "audience_target": {
                "country": "BR", 
                "age_range": [18, 65]
            },
            "budget_cents": 1000000,
            "deadline": "2025-12-31"
        },
        "top_k": 10
    }
    
    response = client.post("/api/v1/recommendations", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["recommendations"]) == 1  # Deve retornar o criador mesmo sem tags

if __name__ == "__main__":
    pytest.main([__file__, "-v"])