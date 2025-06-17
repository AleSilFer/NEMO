from google.cloud import run_v2
from google.cloud import logging_v2


def check_status(service_name: str):
    """
    Verifica o status de um serviço no Google Cloud Run.
    """
    client = run_v2.ServicesClient()

    project_id = "gpt-de-favela"
    location = "southamerica-east1"

    name = f"projects/{project_id}/locations/{location}/services/{service_name}"

    try:
        service = client.get_service(name=name)
        status = {
            "name": service.name,
            "url": service.uri,
            "status": "ACTIVE"
        }
        return status
    except Exception as e:
        return {"error": str(e)}


def get_logs(service_name: str):
    """
    Busca os últimos logs do serviço no Google Cloud Run.
    """
    client = logging_v2.LoggingServiceV2Client()

    project_id = "gpt-de-favela"

    resource_names = [f"projects/{project_id}"]

    filter_str = f'resource.type="cloud_run_revision" resource.labels.service_name="{service_name}"'

    try:
        response = client.list_log_entries(
            {
                "resource_names": resource_names,
                "filter": filter_str,
                "order_by": "timestamp desc",
                "page_size": 10,
            }
        )
        logs = []
        for entry in response:
            logs.append(entry.text_payload)

        return {"logs": logs}
    except Exception as e:
        return {"error": str(e)}
