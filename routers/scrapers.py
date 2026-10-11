from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
import asyncio

# prefix="/scrapers" agrupamento de todas as rotas de scraper com esse prefixo
# tags=["Scrapers"] para manter organizado o Swagger UI visualmente
router = APIRouter(
    prefix="/scrapers",
    tags=["Scrapers"]
)

# --- Modelo Pydantic (Validação de dados) ---
class ScraperTask(BaseModel):
    url: str = Field(..., description="URL Alvo para scraping")
    selectors: list[str] = Field(default=[], description="Elementos CSS para extrair")
    timeout_seconds: int = Field(default=10, ge=1, le=60)

# --- Dependência Auth -> por enquanto simulada (Autenticação ou Conexão) ---
def verify_api_key(api_key: str = "no-auth"):
    if api_key == "no-auth":
        return True
    else:
        raise HTTPException( # Apenas para referência! Se nessário será criado motor de autenticação
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida"
        )

# --- Rotas e Endpoints ---

@router.get("/races")
def read_root():
    """Endpoint síncrono para coleta de eventos."""
    return {"status": "races", "message": "em breve listagem de Eventos, Categorias e Países."}

@router.get("/sync-results")
def sync_endpoint():
    """
    Fluxo SINCRONO para coletar resultados das provas.
    Ideal se preferir dados brutos de todos os atletas de um evento específico.
    """
    return {"modo": "sync", "thread_pool": "Gerenciado automaticamente pelo FastAPI."}

@router.get("/async-results")
async def async_endpoint():
    """
    Fluxo ASSINCRONO.
    Ideal para otimizar fluxo de I/O não bloqueante (ex: requisições HTTP que processarão coleta e tratamento dos dados).
    """
    await asyncio.sleep(1) # esperar alguns segundos para garantir fim do evento de Rede ou I/O, ainda será validado essa necessidade.
    return {"modo": "async", "event_loop": "Async para não travar o servidor principal durante a Pipeline pesada de dados."}

@router.post("/scrapers/run")
def run_scraper_task(task: ScraperTask, autorized: bool = Depends(verify_api_key)):
    """
    Fluxo POST com validação Pydantic e Injeção de Dependência.
    Redebe os dados tipados e validados automaticamente.
    """
    # Aqui será a lógica do scraper (Playwright)
    return {
        "status": "sucesso",
        "mensagem": f"Tarefa iniciada para a URL: {task.url}",
        "itens_configurados": len(task.selectors),
        "timeout": task.timeout_seconds
    }