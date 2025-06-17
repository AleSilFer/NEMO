from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from google.cloud import workflows_v1, firestore
from google.cloud.workflows.executions_v1.types import Execution
from .tools import sptrans_client, Maps_client # Importa as novas ferramentas
import os
import json

# --- Configuração e Modelos ---
app = FastAPI(title="GPT DE FAVELA API", version="2.0.0")
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "gpt-de-favela")
REGION = os.getenv("GCP_REGION", "southamerica-east1")
WORKFLOW_NAME = os.getenv("WORKFLOW_NAME", "gpt-de-favela-workflow")

class ProjectRequest(BaseModel):
    prompt: str
    github_repo_name: str

# --- Endpoints Principais (sem alteração) ---
@app.post("/projects", ...)
async def create_project(project_request: ProjectRequest):
    # (código para iniciar o workflow, como na resposta anterior)
    # ...

@app.get("/projects/{project_id}/status", ...)
async def get_project_status(project_id: str):
    # (código para buscar o status no firestore, como na resposta anterior)
    # ...

# --- NOVOS ENDPOINTS DE ASSISTENTE ---

@app.get("/assistant/bus-location", summary="Localiza ônibus de uma linha em SP")
async def get_bus_location(line_number: str = Query(..., description="O número da linha, ex: '8000-10'")):
    if not sptrans_client.authenticate():
        raise HTTPException(status_code=503, detail="Falha na comunicação com a API da SPTrans.")
    
    lines = sptrans_client.search_line(line_number)
    if not lines:
        raise HTTPException(status_code=404, detail=f"Linha '{line_number}' não encontrada.")
        
    line_code = lines[0]['cl'] # Pega o código da primeira linha encontrada
    positions = sptrans_client.get_bus_positions(line_code)
    
    if not positions or 'vs' not in positions:
        return {"message": "Nenhum ônibus encontrado para esta linha no momento."}
    return {"onibus_encontrados": len(positions['vs']), "veiculos": positions['vs']}

@app.get("/assistant/directions", summary="Busca rotas com transporte público")
async def get_gmaps_directions(origin: str, destination: str):
    directions = Maps_client.get_directions(origin, destination)
    if not directions:
        raise HTTPException(status_code=404, detail="Não foi possível encontrar uma rota.")
    return directions

@app.get("/assistant/places-nearby", summary="Encontra locais de interesse próximos")
async def find_gmaps_places(location: str, keyword: str):
    places = Maps_client.find_nearby_places(location, keyword)
    if not places or 'results' not in places:
        raise HTTPException(status_code=404, detail=f"Não foi possível encontrar locais para '{keyword}' perto de '{location}'.")
    return places['results']