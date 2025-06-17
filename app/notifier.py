import requests


def send_notification(message: str):
    """
    Envia uma notificação simples via webhook (exemplo Discord, Slack, etc.)
    """
    webhook_url = "https://seu-webhook-aqui.com"

    payload = {"content": message}

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204 or response.status_code == 200:
            return {"status": "Notificação enviada com sucesso"}
        else:
            return {
                "status": "Falha ao enviar notificação",
                "details": response.text
            }
    except Exception as e:
        return {"error": str(e)}
