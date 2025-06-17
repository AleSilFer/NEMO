import os
import shutil


def generate_project_files(repo_name: str):
    """
    Gera arquivos básicos do projeto como Dockerfile, cloudbuild.yaml e README.
    """
    repo_path = os.path.join(os.getcwd(), repo_name)
    os.makedirs(repo_path, exist_ok=True)

    # Cria Dockerfile
    dockerfile_content = f"""
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
"""
    with open(os.path.join(repo_path, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)

    # Cria requirements.txt
    requirements = """
fastapi
uvicorn
openai
requests
python-dotenv
pydantic
PyGithub
google-cloud-run
google-cloud-build
google-cloud-artifact-registry
google-cloud-storage
google-cloud-secret-manager
"""
    with open(os.path.join(repo_path, "requirements.txt"), "w") as f:
        f.write(requirements)

    # Cria cloudbuild.yaml
    cloudbuild = f"""
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/{repo_name}', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/{repo_name}']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - '{repo_name}'
      - '--image'
      - 'gcr.io/$PROJECT_ID/{repo_name}'
      - '--region'
      - 'southamerica-east1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--set-env-vars'
      - 'GCP_PROJECT_ID=$PROJECT_ID'
"""
    with open(os.path.join(repo_path, "cloudbuild.yaml"), "w") as f:
        f.write(cloudbuild)

    # Cria README.md
    readme = f"# {repo_name}\n\nProjeto gerado automaticamente pela GPT DevOps API."
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write(readme)

    return {"status": "Arquivos do projeto gerados com sucesso", "repo_path": repo_path}


def replicate_system():
    """
    Função simulada para auto-replicação do sistema.
    """
    return {"status": "Sistema replicado com sucesso (simulado)"}
