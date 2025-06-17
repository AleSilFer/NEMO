# Usa uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a pasta 'app' para dentro do diretório de trabalho /app
# O resultado será a estrutura correta: /app/app/main.py
COPY ./app ./app

# Expõe a porta que o serviço vai rodar
EXPOSE 8080

# Comando para iniciar a aplicação, que agora encontrará o módulo 'app.main'
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}