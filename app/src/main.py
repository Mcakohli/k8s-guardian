import os
import time
from fastapi import FastAPI, Response, status

app = FastAPI(title="k8s-guardian-app")

START_TIME = time.time()
IS_READY = False
IS_ALIVE = True
POD_NAME = os.getenv("POD_NAME", "unknown-pod")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.on_event("startup")
def startup_event():
    global IS_READY
    # Simulate a 5-second bootstrap delay before becoming ready
    time.sleep(5)
    IS_READY = True

@app.get("/")
def get_root():
    return {
        "status": "online",
        "service": "k8s-guardian",
        "version": APP_VERSION,
        "pod": POD_NAME,
        "uptime_seconds": round(time.time() - START_TIME, 2)
    }

@app.get("/healthz")
def get_healthz(response: Response):
    """Liveness probe: returns 500 if deliberately killed."""
    if not IS_ALIVE:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "unhealthy", "pod": POD_NAME}
    return {"status": "alive", "pod": POD_NAME}

@app.get("/ready")
def get_ready(response: Response):
    """Readiness probe: handles graceful traffic removal."""
    if not IS_READY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not_ready", "pod": POD_NAME}
    return {"status": "ready", "pod": POD_NAME}

@app.post("/kill")
def trigger_failure():
    """Forces liveness check to fail, simulating an internal deadlock/crash."""
    global IS_ALIVE
    IS_ALIVE = False
    return {"message": "Application poisoned. Liveness probe will fail."}

@app.post("/unready")
def trigger_unready():
    """Forces readiness to fail, validating traffic removal without pod restart."""
    global IS_READY
    IS_READY = False
    return {"message": "Application drained. Readiness probe will fail."}