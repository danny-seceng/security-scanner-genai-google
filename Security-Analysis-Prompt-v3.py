import hashlib
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()


def add_colors_to_output(text):
    """Add colors to severity levels in the output."""
    text = text.replace(
        "SEVERITY: CRITICAL", f"SEVERITY: {Fore.RED}{Style.BRIGHT}CRITICAL{Style.RESET_ALL}")
    text = text.replace(
        "SEVERITY: HIGH", f"SEVERITY: {Fore.YELLOW}{Style.BRIGHT}HIGH{Style.RESET_ALL}")
    text = text.replace("SEVERITY: MEDIUM",
                        f"SEVERITY: {Fore.BLUE}MEDIUM{Style.RESET_ALL}")
    text = text.replace(
        "SEVERITY: LOW", f"SEVERITY: {Fore.GREEN}LOW{Style.RESET_ALL}")
    return text


def scan_file(filepath):
    """
    Read a file and analyze it for vulnerabilities.
    """
    try:
        with open(filepath, 'r') as f:
            code = f.read()

        print(f"\n{'=' * 60}")
        print(f"Scanning: {filepath}")
        print(f"{'=' * 60}\n")

        # Use the existing security prompt
        response = model.generate_content(security_prompt.format(code=code))
        output = add_colors_to_output(response.text)
        print(output)
    except FileNotFoundError:
        print(f"{Fore.RED} Error: File '{filepath}' not found.{Style.RESET_ALL}")


# Configure with your API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-2.5-flash")

security_prompt = """
Analyze this code for security vulnerabilities. Be concise.

For each issue use this exact format:

- --
SEVERITY: [CRITICAL/HIGH/MEDIUM/LOW]
TYPE: [Vulnerability Name]
DESCRIPTION: [One sentence explaining the issue]
IMPACT: [One sentence on potential damage]
FIX: [Code snippet only]
---

Code:
{code}
"""


# Check if a filename was provided
if len(sys.argv) > 1:
    filepath = sys.argv[1]
    print(f"Scanning file: {filepath}\n")
    scan_file(filepath)
else:
    print("Usage: python scanner.py <filepath>")
    print("Example: python scanner.py vulnerable.py")
