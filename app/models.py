# Modelos de dados usando SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Optional
import json

Base = declarative_base()

# Tabela de associação para tags de criadores (many-to-many)
creator_tags = Table(
    'creator_tags',
    Base.metadata,
    Column('creator_id', Integer, ForeignKey('creators.id')),
    Column('tag', String(50))
)

# Tabela de associação para tags de campanhas
campaign_tags = Table(
    'campaign_tags', 
    Base.metadata,
    Column('campaign_id', Integer, ForeignKey('campaigns.id')),
    Column('tag', String(50))
)

class Creator(Base):
    __tablename__ = "creators"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    tags = Column(JSON)  # Lista de tags como JSON
    audience_age = Column(JSON)  # Lista de idades como JSON [18, 25, 30, ...]
    audience_location = Column(JSON)  # Lista de países como JSON ["BR", "US", ...]
    avg_views = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)  # Click Through Rate
    cvr = Column(Float, default=0.0)  # Conversion Rate
    price_min = Column(Integer, default=0)  # Preço mínimo em centavos
    price_max = Column(Integer, default=0)  # Preço máximo em centavos
    reliability_score = Column(Float, default=0.0)  # Score de confiabilidade (0-1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    deals = relationship("PastDeal", back_populates="creator")

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False)
    goal = Column(String(50), nullable=False)  # "installs", "awareness", "sales", etc.
    tags_required = Column(JSON)  # Tags obrigatórias como JSON
    audience_target = Column(JSON)  # Audiência alvo como JSON {"country": "BR", "age_range": [20,34]}
    budget_cents = Column(Integer, nullable=False)  # Orçamento em centavos
    deadline = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    deals = relationship("PastDeal", back_populates="campaign")

class PastDeal(Base):
    __tablename__ = "past_deals"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creators.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    delivered_on_time = Column(Boolean, default=True)
    performance_score = Column(Float, default=0.0)  # Score de performance (0-1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    creator = relationship("Creator", back_populates="deals")
    campaign = relationship("Campaign", back_populates="deals")