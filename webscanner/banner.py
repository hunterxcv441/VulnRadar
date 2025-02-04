# Console colors and styles
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

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

def print_banner():
    """Displays a custom banner for VulnRadar."""
    banner = f"""
{CYAN}{BOLD}__     __     _       ____           _            
\\ \\   / /   _| |_ __ |  _ \\ __ _  __| | __ _ _ __ 
 \\ \\ / / | | | | '_ \\| |_) / _` |/ _` |/ _` | '__|
  \\ V /| |_| | | | | |  _ < (_| | (_| | (_| | |   
   \\_/  \\__,_|_|_| |_|_| \\_\\__,_|\\__,_|\\__,_|_|  
{RESET}"""
    subtitle = f"{MAGENTA}{BOLD}Web Vulnerability Detection and Analysis Tool{RESET}"
    creator = f"{YELLOW}Created by Buch - Stay Secure!{RESET}"
    github = f"{GREEN}GitHub: https://github.com/hunterxcv441{RESET}"
    print(f"{banner}\n{subtitle}\n{creator}\n{github}\n")
