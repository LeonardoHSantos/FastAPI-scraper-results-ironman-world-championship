from fastapi import FastAPI
from routers import scrapers

app = FastAPI(
    title="API para análise de resultados IRONMAN MAN/Woman - FastAPI",
    description="Scraper prático cobrindo a coleta de dados de resultados e estatísticas dos atletas nos IRONMANS.",
    version="1.0.0"
)

# Registrando o router importado
app.include_router(scrapers.router)

@app.get("/")
def root():
    return {"message": "API IRONMAN rodando!"}