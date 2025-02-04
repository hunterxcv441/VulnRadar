import os
from collections import Counter
import json

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"

def save_report(dir_path, vulnerabilities, endpoints, status_counter, endpoint_results):
    """Saves the final report in a detailed text format and a structured JSON version for LLM."""
    # Detailed TXT report
    detailed_txt_report_path = os.path.join(dir_path, "detailed_report.txt")
    with open(detailed_txt_report_path, "w", encoding="utf-8") as f:
        # Vulnerabilities with code snippets
        f.write(f"{BOLD}=== Detailed Vulnerabilities ==={RESET}\n\n")
        if vulnerabilities:
            for idx, vuln in enumerate(vulnerabilities, 1):
                f.write(f"{MAGENTA}Vulnerability #{idx}{RESET}\n")
                f.write(f"- Description: {vuln['description']}\n")
                f.write(f"- Severity: {vuln['severity']}\n")
                f.write(f"- File: {vuln['file']}\n")
                f.write(f"- Line: {vuln['line']}\n")
                f.write(f"- Snippet: {vuln['snippet']}\n\n")
        else:
            f.write("No vulnerabilities found.\n\n")

        # Endpoints section
        f.write(f"{BOLD}=== Endpoints ==={RESET}\n\n")
        if endpoints:
            for endpoint in endpoints:
                f.write(f"- {endpoint}\n")
        else:
            f.write("No endpoints found.\n\n")

        # HTTP Status section
        f.write(f"{BOLD}=== HTTP Statuses ==={RESET}\n\n")
        if status_counter:
            for status, count in status_counter.items():
                f.write(f"- {status}: {count} occurrence(s)\n")
        else:
            f.write("No HTTP status data available.\n\n")

        # Endpoint Results section
        f.write(f"{BOLD}=== Endpoint Results ==={RESET}\n\n")
        if endpoint_results:
            for result in endpoint_results:
                f.write(f"{result['url']} -> {result['status']}\n")
        else:
            f.write("No endpoint results available.\n\n")

    # JSON report for LLM
    llm_json_report_path = os.path.join(dir_path, "llm_report.json")
    with open(llm_json_report_path, "w", encoding="utf-8") as f:
        json.dump({
            "vulnerabilities": vulnerabilities,
            "endpoints": endpoints,
            "http_statuses": status_counter,
            "endpoint_results": endpoint_results
        }, f, indent=2, ensure_ascii=False)

    print(f"{GREEN}[INFO]{RESET} Detailed TXT report saved at: {detailed_txt_report_path}")
    print(f"{GREEN}[INFO]{RESET} JSON report for LLM saved at: {llm_json_report_path}")


def generate_summary_and_confirm(vulnerabilities):
    """Displays a summary of vulnerabilities and asks if the user wants to continue."""
    print(f"\n{BOLD}{CYAN}Summary of Found Vulnerabilities:{RESET}")
    if vulnerabilities:
        severities = Counter(v["description"] for v in vulnerabilities)
        for description, count in severities.items():
            print(f"{MAGENTA}- {description}:{RESET} {count} occurrence(s)")
    else:
        print(f"{GREEN}No vulnerabilities found.{RESET}")

    continue_scan = input(f"{CYAN}Do you want to continue to endpoint search? (Y/N): {RESET}").strip().lower()
    return continue_scan in ["y", "yes"]
