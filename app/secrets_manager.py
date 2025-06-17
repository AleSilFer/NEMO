from google.cloud import secretmanager
from app import config

client = secretmanager.SecretManagerServiceClient()
parent = f"projects/{config.PROJECT_ID}"

def create_secret(name, value):
    secret = client.create_secret(
        request={"parent": parent, "secret_id": name, "secret": {"replication": {"automatic": {}}}}
    )
    client.add_secret_version(
        request={"parent": secret.name, "payload": {"data": value.encode()}}
    )
    return {"message": f"Secret {name} criado com sucesso."}

def get_secret(name):
    name = f"{parent}/secrets/{name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return {"value": response.payload.data.decode('UTF-8')}

def delete_secret(name):
    client.delete_secret(request={"name": f"{parent}/secrets/{name}"})
    return {"message": f"Secret {name} deletado."}
