from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import recommendations
from .database import init_db

app = FastAPI(
    title="Sistema de Recomendação de Criadores",
    description="API para recomendar criadores para campanhas",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(recommendations.router, prefix="/api/v1")
app.include_router(recommendations.router)  # Endpoint /recommendations sem prefixo

@app.get("/")
async def root():
    return {"message": "Sistema de Recomendação de Criadores - API ativa"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}