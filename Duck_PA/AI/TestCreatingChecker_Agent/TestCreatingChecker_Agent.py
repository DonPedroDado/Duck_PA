import asyncio
import json

from Duck_PA.AI.TestCreatingChecker_Agent.make_message_for_TestCreatingChecker_Agent import make_review_message
from Duck_PA.teachers.classteacher import ClassTeacher

from google.adk.agents.llm_agent import Agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part
from google.adk.sessions import InMemorySessionService

import re
import json

def extract_json(text: str) -> str:
    """Remove Markdown ```json or ``` fences from agent output."""
    text = re.sub(r"^```json\s*", "", text.strip())
    text = re.sub(r"^```\s*", "", text.strip())
    text = re.sub(r"```\s*$", "", text.strip())
    return text

def normalize_questions(parsed):
    """
    Ensure we return a list of question dicts.
    Accepts either a list or a dict with 'questions'.
    """
    if isinstance(parsed, list) and all(isinstance(q, dict) and "question" in q for q in parsed):
        return parsed
    if isinstance(parsed, dict) and "questions" in parsed and isinstance(parsed["questions"], list):
        return parsed["questions"]
    print(f"Warning: unexpected JSON structure, returning empty list. Parsed: {parsed}")
    return []


_SESSION_SERVICE = InMemorySessionService()
_APP_USER_ID = "system"
_APP_APP_NAME = "duck_pa"

async def _run_agent(agent: Agent, prompt: str) -> str:
    session = await _SESSION_SERVICE.create_session(
        app_name=_APP_APP_NAME,
        user_id=_APP_USER_ID,
        session_id="default"
    )

    runner = InMemoryRunner(agent, app_name=_APP_APP_NAME)
    runner.session_service = _SESSION_SERVICE

    content = Content(parts=[Part(text=prompt)])

    async for event in runner.run_async(user_id=session.user_id, session_id=session.id, new_message=content):
        if event.is_final_response():
            return "".join(part.text for part in event.content.parts if getattr(part, "text", None))

    raise RuntimeError("Agent did not return a final response")


def review_test(test_json: dict, teacher: ClassTeacher, language: str):
    message, instruction, personality = make_review_message(test_json, teacher, language)

    agent = Agent(
        model="gemini-2.5-flash",
        name="TestCreatingChecker_Agent",
        description=personality,
        instruction=instruction
    )

    try:
        response_text = asyncio.run(_run_agent(agent, message))
        response_text = extract_json(response_text)
        parsed = json.loads(response_text)

        if isinstance(parsed, dict):
            return parsed.get("questions", [])
        elif isinstance(parsed, list):
            return parsed
        else:
            print(f"Unexpected JSON structure: {parsed}")
            return []

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}\nResponse: {response_text}")
        return []
    except Exception as e:
        print(f"Unexpected agent error: {e}")
        return []
