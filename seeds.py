# Script para popular o banco com dados fictícios
import json
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import Creator, Campaign, PastDeal

# Dados fictícios para seeds
TAGS_POOL = [
    "fintech", "investimentos", "crypto", "bolsa", "poupança",
    "fitness", "musculação", "yoga", "corrida", "nutrição",
    "skincare", "beleza", "maquiagem", "cuidados", "cosmético",
    "tech", "gadgets", "smartphones", "programação", "ai",
    "games", "streaming", "entretenimento", "música", "filme",
    "lifestyle", "viagem", "culinária", "diy", "decoração",
    "educação", "idiomas", "cursos", "livros", "produtividade",
    "sustentabilidade", "meio-ambiente", "vegano", "organic"
]

BRANDS = [
    "NuBank", "Inter", "C6 Bank", "PicPay", "Mercado Pago",
    "Nike", "Adidas", "Under Armour", "Raia Drogasil", "Natura",
    "Boticário", "Apple", "Samsung", "Xiaomi", "Netflix",
    "Spotify", "Uber", "iFood", "Magazine Luiza", "Amazon"
]

CREATOR_BASE_NAMES = [
    "Ana", "Bruno", "Carla", "Diego", "Elena", "Felipe", "Gabriela", "Henrique", 
    "Isabela", "João", "Kamila", "Lucas", "Mariana", "Nicolas", "Olivia", "Pedro",
    "Rafaela", "Samuel", "Tatiana", "Victor", "Amanda", "Bernardo", "Camila", "Daniel",
    "Eduardo", "Fernanda", "Gustavo", "Helena", "Igor", "Julia", "Kevin", "Larissa",
    "Marcelo", "Natalia", "Otavio", "Patricia", "Ricardo", "Sophia", "Thiago", "Vanessa"
]

CREATOR_SURNAMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira",
    "Lima", "Gomes", "Ribeiro", "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes",
    "Vieira", "Barbosa", "Rocha", "Dias", "Nascimento", "Monteiro", "Mendes", "Freitas",
    "Cardoso", "Ramos", "Teixeira", "Reis", "Campos", "Fonseca", "Pinto", "Moreira",
    "Correia", "Martins", "Araújo", "Costa", "Nunes", "Castro", "Machado", "Torres"
]

def generate_creator_data():
    """Gera dados fictícios para criadores"""
    creators = []
    
    # Gerar 100 criadores combinando nomes e sobrenomes
    num_creators = 100
    for i in range(num_creators):
        # Gerar nome único combinando primeiro nome + sobrenome
        first_name = random.choice(CREATOR_BASE_NAMES)
        surname = random.choice(CREATOR_SURNAMES)
        name = f"{first_name} {surname}"
        
        # Se já existe, adicionar número
        base_name = name
        counter = 1
        while any(creator.name == name for creator in creators):
            name = f"{base_name} {counter}"
            counter += 1
            
        # Tags (2-5 tags aleatórias)
        num_tags = random.randint(2, 5)
        creator_tags = random.sample(TAGS_POOL, num_tags)
        
        # Audiência por idade (distribuição normal centrada)
        base_age = random.randint(18, 45)
        audience_age = []
        for _ in range(random.randint(100, 1000)):  # Simular amostra de audiência
            age = max(16, min(65, int(random.normalvariate(base_age, 8))))
            audience_age.append(age)
        
        # Localização (priorizando BR, mas pode ter outros)
        locations = ["BR"]
        if random.random() < 0.3:  # 30% chance de ter audiência internacional
            extra_locations = random.sample(["US", "PT", "ES", "AR", "MX"], random.randint(1, 2))
            locations.extend(extra_locations)
        
        # Métricas de performance
        avg_views = random.randint(5000, 500000)
        ctr = random.uniform(0.005, 0.08)  # 0.5% a 8%
        cvr = random.uniform(0.001, 0.05)  # 0.1% a 5%
        
        # Preços (em centavos)
        base_price = random.randint(50000, 2000000)  # R$ 500 a R$ 20.000
        price_min = base_price
        price_max = int(base_price * random.uniform(1.2, 3.0))
        
        # Score de confiabilidade
        reliability = random.uniform(0.6, 1.0)
        
        creator = Creator(
            name=name,
            tags=creator_tags,
            audience_age=audience_age,
            audience_location=locations,
            avg_views=avg_views,
            ctr=ctr,
            cvr=cvr,
            price_min=price_min,
            price_max=price_max,
            reliability_score=reliability
        )
        creators.append(creator)
    
    return creators

def generate_campaign_data():
    """Gera dados fictícios para campanhas"""
    campaigns = []
    
    campaign_configs = [
        {
            "brand": "NuBank",
            "goal": "installs",
            "tags": ["fintech", "investimentos"],
            "country": "BR",
            "age_range": [25, 45],
            "budget": 1000000  # R$ 10.000
        },
        {
            "brand": "Nike",
            "goal": "awareness",
            "tags": ["fitness", "corrida"],
            "country": "BR", 
            "age_range": [18, 35],
            "budget": 2000000  # R$ 20.000
        },
        {
            "brand": "Natura",
            "goal": "sales",
            "tags": ["skincare", "beleza"],
            "country": "BR",
            "age_range": [20, 40],
            "budget": 800000  # R$ 8.000
        },
        {
            "brand": "Apple",
            "goal": "awareness",
            "tags": ["tech", "smartphones"],
            "country": "BR",
            "age_range": [22, 50],
            "budget": 5000000  # R$ 50.000
        },
        {
            "brand": "Netflix", 
            "goal": "subscriptions",
            "tags": ["entretenimento", "streaming"],
            "country": "BR",
            "age_range": [16, 45],
            "budget": 1500000  # R$ 15.000
        }
    ]
    
    for config in campaign_configs:
        deadline = datetime.now() + timedelta(days=random.randint(30, 90))
        
        campaign = Campaign(
            brand=config["brand"],
            goal=config["goal"],
            tags_required=config["tags"],
            audience_target={
                "country": config["country"],
                "age_range": config["age_range"]
            },
            budget_cents=config["budget"],
            deadline=deadline
        )
        campaigns.append(campaign)
    
    return campaigns

def generate_past_deals(creators, campaigns):
    """Gera histórico fictício de deals"""
    deals = []
    
    # Criar alguns deals históricos para dar contexto
    for _ in range(random.randint(20, 50)):
        creator = random.choice(creators)
        campaign = random.choice(campaigns)
        
        # 80% chance de entrega no prazo
        delivered_on_time = random.random() < 0.8
        
        # Performance score correlacionado com métricas do criador
        base_performance = (creator.ctr * 10 + creator.cvr * 20) / 2
        performance_score = max(0.0, min(1.0, base_performance + random.uniform(-0.2, 0.2)))
        
        deal = PastDeal(
            creator_id=creator.id,
            campaign_id=campaign.id,
            delivered_on_time=delivered_on_time,
            performance_score=performance_score
        )
        deals.append(deal)
    
    return deals

def seed_database():
    """Popula o banco de dados com dados fictícios"""
    print("Inicializando banco de dados...")
    init_db()
    
    db = SessionLocal()
    try:
        # Verificar se já existem dados
        existing_creators = db.query(Creator).count()
        if existing_creators > 0:
            print(f"Banco já possui {existing_creators} criadores. Limpando dados existentes...")
            db.query(PastDeal).delete()
            db.query(Campaign).delete()
            db.query(Creator).delete()
            db.commit()
        
        print("Gerando criadores fictícios...")
        creators = generate_creator_data()
        db.add_all(creators)
        db.commit()
        
        # Refresh para obter IDs
        for creator in creators:
            db.refresh(creator)
        
        print("Gerando campanhas fictícias...")
        campaigns = generate_campaign_data()
        db.add_all(campaigns)
        db.commit()
        
        # Refresh para obter IDs
        for campaign in campaigns:
            db.refresh(campaign)
        
        print("Gerando histórico de deals...")
        deals = generate_past_deals(creators, campaigns)
        db.add_all(deals)
        db.commit()
        
        print(f"✅ Banco populado com sucesso!")
        print(f"   - {len(creators)} criadores")
        print(f"   - {len(campaigns)} campanhas") 
        print(f"   - {len(deals)} deals históricos")
        
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()