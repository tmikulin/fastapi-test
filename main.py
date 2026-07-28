from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Airtable Config
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = "IP Whitelist Test"

class AirtableTrigger(BaseModel):
    record_id: str

@app.post("/proxy")
async def proxy_request(trigger: AirtableTrigger):
    # 1. Make outbound request from THIS server (uses your Static IP)
    target_url = "https://httpbin.org/ip"
    response = requests.get(target_url).json()
    detected_ip = response.get("origin")

    # 2. Update Airtable with the IP seen by the target
    airtable_url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}/{trigger.record_id}"
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}", "Content-Type": "application/json"}
    payload = {"fields": {"Status": "Success", "Returned IP": detected_ip}}
    
    requests.patch(airtable_url, headers=headers, json=payload)

    return {"status": "success", "ip_used": detected_ip}
