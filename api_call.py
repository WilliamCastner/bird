import requests
from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables from .env file
api_key = os.environ.get("api_token")

# Replace these with your actual values
serverName = "api.ebird.org"
contextRoot = "v2"
regionCode = "US-IL-031"
y = "2025"
m = "08"
d = "20"
api_token = "br39qj9m24rq"

url = f"https://{serverName}/{contextRoot}/data/obs/{regionCode}/historic/{y}/{m}/{d}"

headers = {
    "x-ebirdapitoken": api_key
}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print("Response body:", response.json())