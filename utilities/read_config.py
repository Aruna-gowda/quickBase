import os
from dotenv import load_dotenv

load_dotenv()

def read_data(key):
    value = os.getenv(key.upper())
    if not value:
        raise ValueError(f"Environment variable '{key.upper()}' not found.")
    return value.strip()
