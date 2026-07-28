from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Proxy Config (Format: http://username:password@proxy.dns.com:port)
PROXY_URL = os.getenv("OUTBOUNDGATEWAY_URL")
PROXIES = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None

class AirtableTrigger(BaseModel):
    record_id: str

@app.post("/proxy")
async def proxy_request(trigger: AirtableTrigger):
    # 1. Make outbound request THROUGH the static IP proxy
    target_url = "https://httpbin.org/ip"
    
    response = requests.get(target_url, proxies=PROXIES).json()
    detected_ip = response.get("origin")

    return {
        "status": "success", 
        "ip_used": detected_ip
    }
