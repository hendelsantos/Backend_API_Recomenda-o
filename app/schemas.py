# Schemas Pydantic para validação de dados
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class AudienceTarget(BaseModel):
    country: str = Field(..., description="País alvo da audiência")
    age_range: List[int] = Field(..., description="Faixa etária [min, max]")

class CampaignRequest(BaseModel):
    goal: str = Field(..., description="Objetivo da campanha")
    tags_required: List[str] = Field(..., description="Tags obrigatórias")
    audience_target: AudienceTarget = Field(..., description="Audiência alvo")
    budget_cents: int = Field(..., description="Orçamento em centavos")
    deadline: str = Field(..., description="Prazo no formato YYYY-MM-DD")

class RecommendationRequest(BaseModel):
    campaign: CampaignRequest
    top_k: int = Field(default=10, description="Número máximo de recomendações")
    diversity: bool = Field(default=True, description="Aplicar filtro de diversidade")

class FitBreakdown(BaseModel):
    tags: float = Field(..., description="Score de compatibilidade de tags")
    audience_overlap: float = Field(..., description="Score de sobreposição de audiência")
    performance: float = Field(..., description="Score de performance histórica")
    budget_fit: float = Field(..., description="Score de adequação ao orçamento")

class CreatorRecommendation(BaseModel):
    creator_id: str = Field(..., description="ID do criador")
    score: float = Field(..., description="Score total de compatibilidade")
    fit_breakdown: FitBreakdown = Field(..., description="Detalhamento do score")
    why: str = Field(..., description="Justificativa legível")

class RecommendationMetadata(BaseModel):
    total_creators: int = Field(..., description="Total de criadores avaliados")
    scoring_version: str = Field(default="1.0", description="Versão do sistema de scoring")

class RecommendationResponse(BaseModel):
    recommendations: List[CreatorRecommendation]
    metadata: RecommendationMetadata

# Schemas para criadores
class CreatorBase(BaseModel):
    name: str
    tags: List[str]
    audience_age: List[int]
    audience_location: List[str]
    avg_views: int
    ctr: float
    cvr: float
    price_min: int
    price_max: int
    reliability_score: float

class CreatorCreate(CreatorBase):
    pass

class Creator(CreatorBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas para campanhas
class CampaignBase(BaseModel):
    brand: str
    goal: str
    tags_required: List[str]
    audience_target: Dict[str, Any]
    budget_cents: int
    deadline: datetime

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True