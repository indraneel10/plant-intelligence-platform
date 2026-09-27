import json
import os

from sqlalchemy.orm import Session

from app.ai.tools import TOOL_SCHEMAS, execute_tool
from app.core.config import settings

SYSTEM_INSTRUCTIONS = """You are Plant Intelligence Copilot for an autonomous plant-care platform.
You are an observability and reasoning interface over the Plant Intelligence Platform.
Use platform tools to retrieve evidence before making claims about plant health, sensors, observations, decisions, or irrigation.
Never invent sensor values, plant conditions, or actions.
The platform owns plant-state logic, safety, and hardware control. You must not claim that hardware was actuated unless a platform action tool explicitly reports success.
Action requests are safety-gated. You may request irrigation only through the request_irrigation tool. Never claim hardware execution unless a future execution tool explicitly reports success.
Be concise but technically useful. Distinguish observed facts from interpretation.
"""


def _fallback(message: str, plant_id: str | None) -> str:
    if plant_id:
        return (
            "AI Copilot is not configured yet because OPENAI_API_KEY is not set. "
            f"I can still work through the platform APIs for plant {plant_id}; "
            "configure the API key to enable natural-language tool orchestration."
        )
    return (
        "AI Copilot is not configured yet because OPENAI_API_KEY is not set. "
        "Select a plant and configure the API key to enable natural-language tool orchestration."
    )


def chat(db: Session, message: str, plant_id: str | None = None) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"message": _fallback(message, plant_id), "mode": "fallback", "tools_used": []}

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    context = message
    if plant_id:
        context = f"Selected plant_id: {plant_id}\nUser request: {message}"

    response = client.responses.create(
        model=settings.ai_model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=context,
        tools=TOOL_SCHEMAS,
    )

    tools_used: list[str] = []
    while True:
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            break

        outputs = []
        for item in calls:
            tools_used.append(item.name)
            arguments = json.loads(item.arguments)
            if plant_id and "plant_id" not in arguments:
                arguments["plant_id"] = plant_id
            output = execute_tool(db, item.name, arguments)
            outputs.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": output,
            })

        response = client.responses.create(
            model=settings.ai_model,
            instructions=SYSTEM_INSTRUCTIONS,
            previous_response_id=response.id,
            input=outputs,
            tools=TOOL_SCHEMAS,
        )

    return {
        "message": response.output_text,
        "mode": "openai",
        "tools_used": tools_used,
    }
