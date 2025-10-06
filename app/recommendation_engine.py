# Sistema de scoring e recomendação
import math
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from .models import Creator, Campaign, PastDeal
from .schemas import CreatorRecommendation, FitBreakdown, RecommendationMetadata
import json

class RecommendationEngine:
    """
    Sistema de scoring determinístico para recomendação de criadores
    
    Pesos do modelo:
    - Tags: 40% (compatibilidade de nicho/temas)
    - Audiência: 25% (sobreposição demográfica)
    - Performance: 20% (métricas históricas)
    - Orçamento: 10% (adequação de preço)
    - Confiabilidade: 5% (histórico de entregas)
    """
    
    WEIGHTS = {
        'tags': 0.40,
        'audience': 0.25,
        'performance': 0.20,
        'budget': 0.10,
        'reliability': 0.05
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_tags_score(self, creator_tags: List[str], required_tags: List[str]) -> float:
        """
        Calcula score de compatibilidade de tags usando Jaccard similarity
        Score = |intersection| / |union|
        """
        if not required_tags:
            return 1.0
        
        creator_set = set(creator_tags or [])
        required_set = set(required_tags)
        
        intersection = len(creator_set.intersection(required_set))
        union = len(creator_set.union(required_set))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def calculate_audience_score(self, creator_age: List[int], creator_location: List[str],
                               target_country: str, target_age_range: List[int]) -> float:
        """
        Calcula score de sobreposição de audiência
        Combina compatibilidade geográfica e etária
        """
        # Score geográfico (50% do score de audiência)
        geo_score = 1.0 if target_country in (creator_location or []) else 0.0
        
        # Score etário (50% do score de audiência)
        age_score = 0.0
        if creator_age and target_age_range and len(target_age_range) >= 2:
            target_min, target_max = target_age_range[0], target_age_range[1]
            
            # Calcula quantos % da audiência do criador estão na faixa alvo
            overlap_count = sum(1 for age in creator_age if target_min <= age <= target_max)
            age_score = overlap_count / len(creator_age) if creator_age else 0.0
        
        return (geo_score + age_score) / 2
    
    def calculate_performance_score(self, creator: Creator) -> float:
        """
        Calcula score de performance histórica
        Normaliza métricas usando função sigmoid para evitar outliers
        """
        # Normalização das métricas (usando valores típicos do mercado)
        avg_views_norm = self._sigmoid(creator.avg_views, 100000)  # 100k views = 0.5
        ctr_norm = self._sigmoid(creator.ctr, 0.03)  # 3% CTR = 0.5
        cvr_norm = self._sigmoid(creator.cvr, 0.02)  # 2% CVR = 0.5
        
        # Média ponderada das métricas
        return (avg_views_norm * 0.4 + ctr_norm * 0.3 + cvr_norm * 0.3)
    
    def calculate_budget_score(self, creator_min: int, creator_max: int, budget: int) -> float:
        """
        Calcula adequação ao orçamento
        Score máximo quando o orçamento está dentro da faixa do criador
        """
        if creator_min <= budget <= creator_max:
            return 1.0
        elif budget < creator_min:
            # Penaliza se orçamento for muito baixo
            return max(0.0, budget / creator_min)
        else:
            # Bonifica levemente se orçamento for maior (mais flexibilidade)
            return min(1.0, creator_max / budget + 0.2)
    
    def calculate_reliability_score(self, creator: Creator) -> float:
        """
        Score de confiabilidade baseado no histórico de entregas
        """
        return creator.reliability_score
    
    def _sigmoid(self, value: float, midpoint: float) -> float:
        """Função sigmoid para normalização suave"""
        return 1 / (1 + math.exp(-(value - midpoint) / (midpoint * 0.5)))
    
    def score_creator(self, creator: Creator, campaign_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcula score total de um criador para uma campanha específica
        """
        # Extrair dados da campanha
        required_tags = campaign_data.get('tags_required', [])
        audience_target = campaign_data.get('audience_target', {})
        target_country = audience_target.get('country', '')
        target_age_range = audience_target.get('age_range', [])
        budget = campaign_data.get('budget_cents', 0)
        
        # Calcular scores individuais
        tags_score = self.calculate_tags_score(creator.tags or [], required_tags)
        audience_score = self.calculate_audience_score(
            creator.audience_age or [], 
            creator.audience_location or [],
            target_country, 
            target_age_range
        )
        performance_score = self.calculate_performance_score(creator)
        budget_score = self.calculate_budget_score(creator.price_min, creator.price_max, budget)
        reliability_score = self.calculate_reliability_score(creator)
        
        # Score total ponderado
        total_score = (
            tags_score * self.WEIGHTS['tags'] +
            audience_score * self.WEIGHTS['audience'] +
            performance_score * self.WEIGHTS['performance'] +
            budget_score * self.WEIGHTS['budget'] +
            reliability_score * self.WEIGHTS['reliability']
        )
        
        return {
            'tags': tags_score,
            'audience_overlap': audience_score,
            'performance': performance_score,
            'budget_fit': budget_score,
            'reliability': reliability_score,
            'total': total_score
        }
    
    def generate_explanation(self, creator: Creator, scores: Dict[str, float], 
                           campaign_data: Dict[str, Any]) -> str:
        """
        Gera explicação legível do score
        """
        explanations = []
        
        # Tags
        required_tags = campaign_data.get('tags_required', [])
        creator_tags = creator.tags or []
        matching_tags = set(creator_tags).intersection(set(required_tags))
        if matching_tags:
            explanations.append(f"Trabalha com {', '.join(matching_tags)}")
        
        # Audiência
        audience_target = campaign_data.get('audience_target', {})
        target_country = audience_target.get('country', '')
        if target_country in (creator.audience_location or []):
            target_age_range = audience_target.get('age_range', [])
            if target_age_range and len(target_age_range) >= 2:
                explanations.append(f"Audiência em {target_country} {target_age_range[0]}-{target_age_range[1]} anos")
        
        # Performance
        if scores['performance'] > 0.7:
            explanations.append(f"{creator.avg_views//1000}k views médias")
        
        # Confiabilidade
        reliability_pct = int(creator.reliability_score * 10)
        explanations.append(f"{reliability_pct}/10 em confiabilidade")
        
        return "; ".join(explanations) if explanations else "Criador adequado para a campanha"
    
    def get_recommendations(self, campaign_data: Dict[str, Any], top_k: int = 10) -> List[CreatorRecommendation]:
        """
        Gera lista de recomendações ordenada por score
        """
        # Buscar todos os criadores
        creators = self.db.query(Creator).all()
        
        recommendations = []
        for creator in creators:
            scores = self.score_creator(creator, campaign_data)
            
            # Criar recomendação
            recommendation = CreatorRecommendation(
                creator_id=str(creator.id),
                score=round(scores['total'], 3),
                fit_breakdown=FitBreakdown(
                    tags=round(scores['tags'], 3),
                    audience_overlap=round(scores['audience_overlap'], 3),
                    performance=round(scores['performance'], 3),
                    budget_fit=round(scores['budget_fit'], 3)
                ),
                why=self.generate_explanation(creator, scores, campaign_data)
            )
            recommendations.append(recommendation)
        
        # Ordenar por score decrescente e limitar
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:top_k]