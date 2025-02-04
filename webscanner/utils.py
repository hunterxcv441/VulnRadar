import os
from urllib.parse import urlparse

def sanitize_filename(filename):
    """Removes or replaces invalid characters in file names."""
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '&', '=']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def create_site_directory(url):
    """Creates a directory based on the site name."""
    parsed_url = urlparse(url)
    site_name = parsed_url.netloc.replace("www.", "").replace(":", "_")
    dir_path = os.path.join("./results", site_name)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path
