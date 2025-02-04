"""
Package `webscanner`: Scanner for analyzing vulnerabilities in JavaScript files,
detecting possible endpoints, and generating detailed reports.

Available modules:
- banner: Displays the initial banner in the console.
- utils: Utility functions for file and directory handling.
- downloader: Downloads JavaScript files from a URL.
- scanner: Analyzes JavaScript files for vulnerability patterns.
- reporter: Generates and saves detailed reports.
- endpoints: Detects and verifies possible endpoints in JavaScript files.

Usage:
    from webscanner import main
    main.run()
"""

from .banner import print_banner
from .utils import create_site_directory, sanitize_filename
from .downloader import download_js_files
from .scanner import scan_directory, check_js_file
from .reporter import save_report, generate_summary_and_confirm
from .endpoints import find_endpoints, check_endpoints
