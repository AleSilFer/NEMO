# GPT DevOps API 🔥

Uma API capaz de:
- 🔥 Gerar código com IA (GPT).
- 🐙 Criar repositórios no GitHub.
- 🐳 Buildar imagens Docker.
- ☁️ Fazer deploy no Google Cloud Run.
- 🔐 Gerenciar secrets e monitoramento.
- ♻️ Se auto-replicar, criar cópias dela mesma.

## Como rodar local
pip install -r requirements.txt
uvicorn app.main:app --reload

## Como fazer deploy
gcloud builds submit --config cloudbuild.yaml .

## Docs
Acesse:
http://localhost:8000/docs
