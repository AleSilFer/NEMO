import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Google Cloud
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION")
REPOSITORY = os.getenv("REPOSITORY")
IMAGE = os.getenv("IMAGE")
SERVICE = os.getenv("SERVICE")
