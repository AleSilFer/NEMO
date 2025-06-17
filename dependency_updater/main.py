import functions_framework
import os
import requests
from packaging import version
from github import Github
from google.cloud import firestore, secretmanager

# --- Configuração Inicial ---
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "gpt-de-favela")

# Clientes para os serviços do Google Cloud
firestore_client = firestore.Client(project=PROJECT_ID)
secret_client = secretmanager.SecretManagerServiceClient()

# --- Funções Auxiliares ---

def get_secret(secret_id, version_id="latest"):
    """Busca um segredo do Google Secret Manager."""
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = secret_client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def get_latest_pypi_version(package_name):
    """Verifica a versão mais recente de um pacote no PyPI."""
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["info"]["version"]
    except requests.exceptions.RequestException:
        # Retorna None se o pacote não for encontrado ou houver erro
        return None

# --- Função Principal ---

@functions_framework.http
def check_dependencies(request):
    """
    Função principal acionada pelo Cloud Scheduler.
    Verifica as dependências de todos os projetos gerenciados.
    """
    print("--- AGENTE DE MANUTENÇÃO INICIADO ---")
    
    try:
        # Busca o token do GitHub que está guardado de forma segura
        github_token = get_secret("GITHUB_TOKEN")
        github_client = Github(github_token)
        github_user = github_client.get_user()

        # Busca todos os projetos no Firestore
        projects_ref = firestore_client.collection("projects").stream()
        
        for project in projects_ref:
            project_data = project.to_dict()
            repo_name = project_data.get("github_repo_name")

            if not repo_name:
                continue

            print(f"Verificando repositório: {repo_name}")
            
            try:
                # Acessa o repositório no GitHub
                repo = github_user.get_repo(repo_name)
                contents = repo.get_contents("requirements.txt", ref="main")
                requirements_text = contents.decoded_content.decode("utf-8")
                
                current_deps = requirements_text.strip().split("\n")
                updates_found = []
                new_requirements = []

                # Verifica cada dependência
                for dep in current_deps:
                    if "==" in dep:
                        package, current_ver_str = dep.split("==")
                        latest_ver_str = get_latest_pypi_version(package)
                        
                        if latest_ver_str and version.parse(latest_ver_str) > version.parse(current_ver_str):
                            print(f"  -> Atualização encontrada para {package}: {current_ver_str} -> {latest_ver_str}")
                            updates_found.append(f"Atualiza {package} de {current_ver_str} para {latest_ver_str}")
                            new_requirements.append(f"{package}=={latest_ver_str}")
                        else:
                            new_requirements.append(dep)
                    else:
                        new_requirements.append(dep)

                # Se houver atualizações, cria um Pull Request
                if updates_found:
                    print(f"  Abrindo Pull Request para {repo_name}...")
                    
                    new_branch_name = f"dependabot/updates-{firestore.SERVER_TIMESTAMP.now().strftime('%Y-%m-%d')}"
                    main_branch = repo.get_branch("main")
                    
                    # Cria uma nova branch a partir da main
                    repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=main_branch.commit.sha)
                    
                    # Faz o commit do novo requirements.txt na nova branch
                    commit_message = "chore: Atualiza dependências"
                    repo.update_file(
                        "requirements.txt",
                        commit_message,
                        "\n".join(new_requirements),
                        contents.sha,
                        branch=new_branch_name
                    )
                    
                    # Cria o Pull Request
                    pr_title = "Atualização automática de dependências"
                    pr_body = "Olá! Encontrei algumas atualizações para as dependências do projeto:\n\n- " + "\n- ".join(updates_found)
                    repo.create_pull(title=pr_title, body=pr_body, head=new_branch_name, base="main")
                    print(f"  Pull Request aberto com sucesso!")
                else:
                    print("  Nenhuma atualização de dependência encontrada.")

            except Exception as e:
                print(f"  ERRO ao processar o repositório {repo_name}: {e}")

    except Exception as e:
        print(f"ERRO CRÍTICO no agente de manutenção: {e}")
        return "Erro no agente", 500

    print("--- AGENTE DE MANUTENÇÃO FINALIZADO ---")
    return "Verificação concluída", 200