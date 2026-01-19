# main.py Completely chatGPT'd
import os
import threading
import time
import subprocess
from typing import Any, Dict, Optional

from fastapi import FastAPI, Header
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel

targetContainer = os.getenv("TARGET_CONTAINER_NAME")
timeoutTime = int(os.getenv("TIMEOUT_TIME", "-1"))

app = FastAPI()


class WebhookPayload(BaseModel):
    event_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return "pong"


def restart_container_later(delay: float = 1.0):
    if not targetContainer:
        print("No TARGET_CONTAINER_NAME set, skipping restart")
        return

    time.sleep(delay)  # give the response time to be sent

    cmd = ["docker", "restart"]
    if timeoutTime >= 0:
        cmd.extend(["-t", str(timeoutTime)])
    cmd.append(targetContainer)

    print("Restarting:", " ".join(cmd))
    # do NOT block, just fire and forget
    subprocess.Popen(cmd)


@app.post("/webhook")
def webhook(
    payload: WebhookPayload,
    x_webhook_token: Optional[str] = Header(default=None),
):
    # run restart in background, slightly delayed
    threading.Thread(
        target=restart_container_later,
        kwargs={"delay": 1.0},
        daemon=True,
    ).start()

    # immediately respond
    return JSONResponse({"ok": True, "event_id": payload.event_id})
