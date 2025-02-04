import argparse
import os
import json
from webscanner.banner import print_banner
from webscanner.utils import create_site_directory
from webscanner.downloader import download_js_files
from webscanner.scanner import scan_directory
from webscanner.reporter import save_report, generate_summary_and_confirm
from webscanner.endpoints import find_endpoints, check_endpoints
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
# Obter caminho absoluto para o padrão
DEFAULT_PATTERNS_PATH = os.path.join(os.path.dirname(__file__), "webscanner", "patterns.json")

# Console colors and styles
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"

def print_info(message):
    """Prints an info message."""
    print(f"{CYAN}[INFO]{RESET} {message}")

def print_success(message):
    """Prints a success message."""
    print(f"{GREEN}[SUCCESS]{RESET} {message}")

def print_warning(message):
    """Prints a warning message."""
    print(f"{YELLOW}[WARNING]{RESET} {message}")

def print_error(message):
    """Prints an error message."""
    print(f"{RED}[ERROR]{RESET} {message}")

def display_vulnerabilities(vulnerabilities):
    """Displays the found vulnerabilities in a stylized manner."""
    print(f"\n{BOLD}{CYAN}Summary of Found Vulnerabilities:{RESET}")
    if vulnerabilities:
        for vulnerability in vulnerabilities:
            severity = vulnerability.get("severity", "UNDEFINED").upper()
            color = (
                RED if severity == "HIGH" else
                YELLOW if severity == "MEDIUM" else
                GREEN
            )
            print(f"{color}Description:{RESET} {vulnerability.get('description', 'No description')}")
            print(f"{color}File:{RESET} {vulnerability.get('file', 'Unknown file')}")
            print(f"{color}Line:{RESET} {vulnerability.get('line', 'Unknown line')}")
            print(f"{color}Snippet:{RESET} {vulnerability.get('snippet', 'No snippet')}")
            print(f"{CYAN}{'-' * 80}{RESET}")
    else:
        print_success("No vulnerabilities found.")

def display_endpoints(endpoints):
    """Displays the found endpoints in a stylized manner."""
    print(f"\n{BOLD}{CYAN}Found Endpoints:{RESET}")
    if endpoints:
        for endpoint in endpoints:
            color = GREEN if endpoint.startswith("http") else YELLOW
            print(f"{color}- {endpoint}{RESET}")
    else:
        print_warning("No endpoints found.")

def load_patterns_from_json(json_file):
    """Loads vulnerability patterns from a JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print_error(f"Failed to load patterns file: {e}")
        raise e

def main():
    # Parse argumentos
    parser = argparse.ArgumentParser(
        description="WebScanner - JavaScript Vulnerability and Endpoint Analyzer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-u", "--url", help="URL to scan for JavaScript files")
    parser.add_argument("-d", "--directory", help="Directory to scan for JavaScript files")
    parser.add_argument(
        "-p", "--patterns",
        default=DEFAULT_PATTERNS_PATH,
        help=f"JSON file containing vulnerability patterns (default: {DEFAULT_PATTERNS_PATH})"
    )
    parser.add_argument("-o", "--output", default="./results", help="Directory to save reports")
    parser.add_argument("-v", "--verify-endpoints", action="store_true", help="Verify HTTP status codes for found endpoints")
    args = parser.parse_args()

    print_banner()

    # Certificar-se de que o arquivo de padrões existe
    if not os.path.isfile(args.patterns):
        print(f"[ERROR] The patterns file '{args.patterns}' does not exist.")
        return

    # Certificar-se de que o diretório de saída existe
    os.makedirs(args.output, exist_ok=True)

    # Processar lógica para URL ou diretório

    # Determine mode (URL or directory)
    if args.url:
        print_info("Scanning URL for JavaScript files...")
        dir_path = create_site_directory(args.url)
        directory = download_js_files(args.url, dir_path)
    elif args.directory:
        print_info("Scanning directory for JavaScript files...")
        directory = args.directory
        dir_path = args.output
    else:
        print_warning("No URL or directory provided. Switching to interactive mode.")
        choice = input(f"{CYAN}Do you want to scan a URL or a directory? (URL/DIR): {RESET}").strip().lower()
        if choice == "url":
            url = input(f"{BOLD}{CYAN}Enter the URL: {RESET}").strip()
            dir_path = create_site_directory(url)
            directory = download_js_files(url, dir_path)
        elif choice == "dir":
            directory = input(f"{BOLD}{CYAN}Enter the directory path: {RESET}").strip()
            dir_path = "./results/manual"
        else:
            print_error("Invalid option. Exiting...")
            return

    # Load patterns
    print_info("Loading vulnerability patterns...")
    patterns = load_patterns_from_json(args.patterns)

    # Scan for vulnerabilities
    print_info("Scanning for vulnerabilities...")
    vulnerabilities = scan_directory(directory, patterns)
    display_vulnerabilities(vulnerabilities)

    if not generate_summary_and_confirm(vulnerabilities):
        print_info("Exiting after vulnerability analysis.")
        save_report(dir_path, vulnerabilities, [], {}, [])
        return

    # Find endpoints
    print_info("Searching for possible endpoints...")
    endpoints = []
    for file in [f for f in os.listdir(directory) if f.endswith(".js")]:
        with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
            content = f.read()
            endpoints.extend(find_endpoints(content))

    endpoints = list(set(endpoints))
    display_endpoints(endpoints)

    # Optionally verify endpoints
    status_counter = {}
    endpoint_results = []
    if args.verify_endpoints and args.url:
        print_info("Verifying HTTP response codes for endpoints...")
        status_counter, endpoint_results = check_endpoints(args.url, endpoints)
    elif args.verify_endpoints:
        print_warning("Endpoint verification requires a base URL. Skipping verification.")

    # Save report
    save_report(dir_path, vulnerabilities, endpoints, status_counter, endpoint_results)
    print_success("Analysis completed successfully. Report saved.")

if __name__ == "__main__":
    main()
