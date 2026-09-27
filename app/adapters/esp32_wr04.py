import json, os
from urllib import request
from app.domain.action import Action
from app.ports.actuator import ActuatorPort
class ESP32WR04Actuator(ActuatorPort):
    def __init__(self, base_url=None, timeout_seconds=5.0):
        self.base_url=(base_url or os.getenv("ESP32_WR04_URL","")).rstrip("/")
        self.timeout_seconds=timeout_seconds
        if not self.base_url: raise ValueError("ESP32_WR04_URL is required")
    def execute(self, action: Action) -> None:
        payload={"action_type":action.action_type.value,"zone_id":action.zone_id,"duration_seconds":action.duration_seconds}
        req=request.Request(f"{self.base_url}/v1/actuators/irrigation",data=json.dumps(payload).encode(),method="POST",headers={"Content-Type":"application/json","Accept":"application/json"})
        with request.urlopen(req,timeout=self.timeout_seconds) as response:
            if response.status<200 or response.status>=300: raise RuntimeError(f"ESP32 HTTP {response.status}")
            result=json.loads(response.read().decode())
        if result.get("status")!="accepted": raise RuntimeError(f"ESP32 rejected action: {result}")
