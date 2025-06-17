import os
from app import config

def deploy_service():
    command = f"""
    gcloud run deploy {config.SERVICE} \
    --image=southamerica-east1-docker.pkg.dev/{config.PROJECT_ID}/{config.REPOSITORY}/{config.IMAGE} \
    --platform=managed \
    --region={config.REGION} \
    --allow-unauthenticated
    """
    os.system(command)
    return {"message": f"Deploy do serviço {config.SERVICE} iniciado."}
