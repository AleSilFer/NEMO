import functions_framework
from google.cloud import containeranalysis_v1

@functions_framework.http
def scan_image_vulnerabilities(request):
    """
    Cloud Function acionada por HTTP que verifica vulnerabilidades
    de uma imagem no Artifact Registry.
    Exemplo de corpo da requisição: {"image_uri": "gcr.io/meu-projeto/minha-imagem:latest"}
    """
    request_json = request.get_json(silent=True)
    if not request_json or "image_uri" not in request_json:
        return "Erro: 'image_uri' não fornecido no corpo da requisição.", 400

    image_uri = request_json["image_uri"]
    project_id = os.getenv("GCP_PROJECT_ID")
    
    client = containeranalysis_v1.ContainerAnalysisClient()
    resource_url = f"https://{image_uri}"
    filter_str = f'resourceUrl="{resource_url}" AND note_kind="VULNERABILITY"'

    try:
        results = client.get_grafeas_client().list_occurrences(parent=f"projects/{project_id}", filter=filter_str)
        vulnerabilities = []
        for occ in results:
            vulnerabilities.append({
                "severidade": occ.vulnerability.severity.name,
                "descricao": occ.vulnerability.short_description
            })

        if not vulnerabilities:
            return {"status": "SUCESSO", "message": "Nenhuma vulnerabilidade encontrada."}, 200
        else:
            return {"status": "FALHA", "vulnerabilities_found": len(vulnerabilities), "details": vulnerabilities}, 200

    except Exception as e:
        return f"Erro ao escanear a imagem: {e}", 500