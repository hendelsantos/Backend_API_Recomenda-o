# Rotas da API
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import RecommendationRequest, RecommendationResponse, RecommendationMetadata
from ..recommendation_engine import RecommendationEngine

router = APIRouter()

@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint principal para obter recomendações de criadores
    """
    try:
        # Converter dados da campanha para dict
        campaign_data = {
            'goal': request.campaign.goal,
            'tags_required': request.campaign.tags_required,
            'audience_target': {
                'country': request.campaign.audience_target.country,
                'age_range': request.campaign.audience_target.age_range
            },
            'budget_cents': request.campaign.budget_cents,
            'deadline': request.campaign.deadline
        }
        
        # Inicializar engine de recomendação
        engine = RecommendationEngine(db)
        
        # Gerar recomendações
        recommendations = engine.get_recommendations(campaign_data, request.top_k)
        
        # Contar total de criadores
        from ..models import Creator
        total_creators = db.query(Creator).count()
        
        # Criar resposta
        response = RecommendationResponse(
            recommendations=recommendations,
            metadata=RecommendationMetadata(
                total_creators=total_creators,
                scoring_version="1.0"
            )
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/creators/count")
async def get_creators_count(db: Session = Depends(get_db)):
    """
    Endpoint para verificar quantos criadores estão cadastrados
    """
    from ..models import Creator
    count = db.query(Creator).count()
    return {"total_creators": count}