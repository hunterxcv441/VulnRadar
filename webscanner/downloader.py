import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from webscanner.utils import sanitize_filename


def extract_inline_scripts(soup, js_dir):
    """Saves inline JavaScript blocks found in the HTML."""
    inline_scripts = soup.find_all("script", src=False)
    count = 0
    for idx, script in enumerate(inline_scripts, start=1):
        content = script.get_text().strip()
        if not content:
            continue
        filename = os.path.join(js_dir, f"inline_{idx}.js")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
    return count

def download_js_files(url, dir_path, save_inline=True):
    """Downloads JavaScript files associated with the provided URL.

    Args:
        url (str): Website URL to scan.
        dir_path (str): Directory to store the downloaded files.
        save_inline (bool): If True, also save inline <script> blocks.

    Returns:
        str: Path to the directory containing the downloaded JavaScript files.
    """
    js_dir = os.path.join(dir_path, "js_files")
    os.makedirs(js_dir, exist_ok=True)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        scripts = soup.find_all("script", src=True)

        for script in tqdm(scripts, desc="Downloading files", ncols=80, colour="blue"):
            js_url = urljoin(url, script["src"])
            try:
                js_response = requests.get(js_url, timeout=10)
                js_response.raise_for_status()
                filename = sanitize_filename(os.path.basename(script["src"]))
                with open(os.path.join(js_dir, filename), "w", encoding="utf-8") as f:
                    f.write(js_response.text)
            except Exception as e:
                print(f"[WARNING] Unable to download {js_url}: {e}")

    except Exception as e:
        print(f"[ERROR] Failed to access the URL {url}: {e}")
        raise e

    if save_inline:
        count = extract_inline_scripts(soup, js_dir)
        if count:
            print(f"[INFO] Saved {count} inline script(s)")

    return js_dir
