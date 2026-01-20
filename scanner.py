import hashlib
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure with your API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-2.5-flash")

# Test code with a security vulnerablility
test_code = '''
password = "admin123"
'''

# Ask Gemini to analyze it
"""
prompt = f"Analyze this code for security issues:\n{test_code}"
response = model.generate_content(prompt)
print(response)
"""

response = model.generate_content(
    "Say 'Hello, security scanner!' if you can hear me.")
print(response.text)
