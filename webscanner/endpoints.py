import requests
from urllib.parse import urljoin, urlparse
from collections import Counter
import re

# Colors for the console
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
WHITE = "\033[37m"

def find_endpoints(content):
    """
    Searches for potential endpoints in a JavaScript file.

    Args:
        content (str): Content of the JavaScript file.

    Returns:
        list: List of endpoints found.
    """
    patterns = [
        # URLs completas
        r"https?://[^\s\"']+",  # URLs completas com http:// ou https://
        r"https?://[a-zA-Z0-9.-]+:\d+/[^\s\"']*",  # URLs com portas

        # Caminhos de APIs genéricos
        r"/api/[^\s\"']*",  # Caminhos genéricos que começam com /api/
        r"/v\d+/[^\s\"']*",  # Versões como /v1/, /v2/, etc.

        # Combinações baseadas em verbos e substantivos
        r"/(get|create|update|delete)/[a-zA-Z0-9_-]+",  # Ações com recursos
        r"/[a-zA-Z0-9_-]+/(get|create|update|delete)",  # Recursos seguidos de ações
        r"/(get|post|put|patch|delete)/[^\s\"']+",  # Métodos HTTP comuns em APIs
        r"/[a-zA-Z0-9_-]+/(list|detail|info|summary)",  # Recursos seguidos por operações descritivas
        r"/(list|detail|info|summary)/[a-zA-Z0-9_-]+",  # Operações descritivas seguidas de recursos

        # Endpoints com IDs ou chaves dinâmicas
        r"/[a-zA-Z0-9_-]+/\d+",  # Caminhos com IDs numéricos (e.g., /user/123)
        r"/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+",  # Caminhos com IDs alfanuméricos (e.g., /user/john_doe)
        r"/[a-zA-Z0-9_-]+/\{[a-zA-Z0-9_-]+\}",  # IDs dinâmicos (e.g., /user/{userId})
        r"/[a-zA-Z0-9_-]+/\:[a-zA-Z0-9_-]+",  # IDs dinâmicos com ":" (e.g., /user/:userId)

        # Padrões baseados em categorias
        r"/(auth|oauth|token|login|logout|signup|register|verify)/[^\s\"']*",  # Autenticação e tokens
        r"/(user|account|profile|settings|preferences)/[^\s\"']*",  # Usuários e configurações
        r"/(product|order|cart|checkout|payment|invoice)/[^\s\"']*",  # E-commerce
        r"/(admin|dashboard|config|analytics|reports|logs)/[^\s\"']*",  # Administrativo e relatórios
        r"/(notification|message|chat|feed|media)/[^\s\"']*",  # Comunicação e mídia

        # Padrões para uploads e downloads
        r"/(upload|download|file|image|video|media)/[^\s\"']*",  # Arquivos e mídia

        # Padrões para buscas e consultas
        r"/(search|query|filter|find)/[^\s\"']*",  # Busca e filtros

        # Health checks e status
        r"/(health|status|metrics|info)/[^\s\"']*",  # Health checks e métricas

        # Recursos estáticos e assets
        r"/(static|assets|css|js|images|videos|fonts|files)/[^\s\"']*",  # Recursos estáticos
        r"/(favicon\.ico|robots\.txt|sitemap\.xml)",  # Arquivos padrões

        # Endpoints com parâmetros opcionais ou query strings
        r"/[a-zA-Z0-9_-]+(\?.+)?",  # Caminhos com query strings opcionais
        r"/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+(\?.+)?",  # Caminhos com sub-recursos e query strings

    ]

    endpoints = []
    for pattern in patterns:
        matches = re.findall(pattern, content)
        endpoints.extend(matches)

    return list(set(endpoints))

def check_endpoints(base_url, endpoints):
    """
    Checks the HTTP response codes of the found endpoints.

    Args:
        base_url (str): Base URL of the website.
        endpoints (list): List of endpoints.

    Returns:
        tuple: Counter of status codes and detailed results list.
    """
    print(f"\n{BOLD}{CYAN}Checking Found Endpoints:{RESET}")
    status_counter = Counter()
    results = []

    for endpoint in endpoints:
        parsed_url = urlparse(endpoint)
        full_url = endpoint if parsed_url.scheme else urljoin(base_url, endpoint)

        try:
            response = requests.get(full_url, timeout=5)
            status_code = response.status_code
            print(f"{WHITE}[{CYAN}{full_url}{WHITE}] -> {GREEN if status_code == 200 else RED}{status_code}{RESET}")
            results.append({"url": full_url, "status": status_code})
            status_counter[status_code] += 1
        except Exception as e:
            print(f"{WHITE}[{CYAN}{full_url}{WHITE}] -> {RED}Error: {e}{RESET}")
            results.append({"url": full_url, "status": "Error"})
            status_counter["Error"] += 1

    return status_counter, results
