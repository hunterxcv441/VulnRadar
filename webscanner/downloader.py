import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from webscanner.utils import sanitize_filename

def download_js_files(url, dir_path):
    """Downloads JavaScript files associated with the provided URL."""
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

    return js_dir
