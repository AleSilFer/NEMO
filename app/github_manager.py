from github import Github
import os
from app import config

g = Github(config.GITHUB_TOKEN)

def create_repo(repo_name: str):
    user = g.get_user()
    repo = user.create_repo(repo_name)
    return {"repo_url": repo.html_url}

def push_to_repo(repo_name: str):
    # Simulação de push - aqui você faria git init, add, commit, push via subprocess
    return {"message": f"Código enviado para o repositório {repo_name}"}

def generate_project_files(repo_name: str):
    files = {
        "Dockerfile": "FROM python:3.11-slim\n...",
        "cloudbuild.yaml": "steps:\n- name: ...",
        ".github/workflows/deploy.yaml": "name: Deploy to Google Cloud Run\n..."
    }
    return {"files": list(files.keys())}
