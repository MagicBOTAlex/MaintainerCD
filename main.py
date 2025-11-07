# main.py Completely chatGPT'd
import os
from typing import Any, Dict, Optional
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel
import subprocess

targetContainer = os.getenv("TARGET_CONTAINER_NAME")
timeoutTime = int(os.getenv("TIMEOUT_TIME", '-1'))

app = FastAPI()


class WebhookPayload(BaseModel):
    event_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return "pong"


@app.post("/webhook")
def webhook(payload: WebhookPayload, x_webhook_token: Optional[str] = Header(default=None)):
    runParams = ["docker", "restart", targetContainer]
    print("Restarting")
    if timeoutTime >= 0:
        runParams.append("-t")
        runParams.append(timeoutTime)
    subprocess.run(["docker", "restart", targetContainer], check=True)
    return JSONResponse({"ok": True, "event_id": payload.event_id})
