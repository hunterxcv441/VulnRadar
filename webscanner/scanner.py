import os
import re
from tqdm import tqdm

def check_js_file(js_path, patterns):
    """Checks patterns in JavaScript files."""
    vulnerabilities = []
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.splitlines()
        for line_number, line in enumerate(lines, start=1):
            for pattern in patterns:
                if re.search(pattern["pattern"], line):
                    vulnerabilities.append({
                        "file": js_path,
                        "line": line_number,
                        "snippet": line.strip()[:80] + "..." if len(line) > 80 else line.strip(),
                        "description": pattern.get("description", "No description"),
                        "severity": pattern.get("severity", "UNDEFINED")
                    })
    except Exception as e:
        print(f"[ERROR] Failed to analyze the file {js_path}: {e}")
    return vulnerabilities

def scan_directory(directory, patterns):
    """Scans a directory for vulnerabilities in JavaScript files."""
    file_list = []
    vulnerabilities = []

    # Collect all .js files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".js"):
                file_list.append(os.path.join(root, file))

    # Scan each file for vulnerabilities
    with tqdm(total=len(file_list), desc="Analyzing JavaScript files", ncols=80, colour="green") as pbar:
        for js_path in file_list:
            vulnerabilities.extend(check_js_file(js_path, patterns))
            pbar.update(1)

    return vulnerabilities
