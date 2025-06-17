import os
from app import config

def build_image():
    command = f"docker build -t {config.IMAGE} ."
    os.system(command)
    return {"message": f"Imagem {config.IMAGE} construída com sucesso."}

def push_image():
    full_path = f"southamerica-east1-docker.pkg.dev/{config.PROJECT_ID}/{config.REPOSITORY}/{config.IMAGE}"
    os.system(f"docker tag {config.IMAGE} {full_path}")
    os.system(f"docker push {full_path}")
    return {"message": f"Imagem {full_path} enviada para o Artifact Registry."}
