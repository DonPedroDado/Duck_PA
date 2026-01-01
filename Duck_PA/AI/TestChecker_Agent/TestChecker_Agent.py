import asyncio
import json

from Duck_PA.AI.TestChecker_Agent.make_message_for_TestChecker_Agent import make_message_for_TestChecker_Agent
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


# Shared session service
_SESSION_SERVICE = InMemorySessionService()
_APP_USER_ID = "system"
_APP_APP_NAME = "duck_pa"

async def _run_agent(agent: Agent, prompt: str) -> str:
    # Create a session (or reuse an existing one)
    session = await _SESSION_SERVICE.create_session(
        app_name=_APP_APP_NAME,
        user_id=_APP_USER_ID,
        session_id="default"  # You can choose any ID you like
    )

    # Create the runner and attach the shared session service
    runner = InMemoryRunner(agent, app_name=_APP_APP_NAME)
    runner.session_service = _SESSION_SERVICE

    # Prepare content
    content = Content(parts=[Part(text=prompt)])

    # Run the agent
    async for event in runner.run_async(user_id=session.user_id, session_id=session.id, new_message=content):
        if event.is_final_response():
            return "".join(part.text for part in event.content.parts if getattr(part, "text", None))

    raise RuntimeError("Agent did not return a final response")


def check_test_with_agent(questions: list, answers: list, teacher: ClassTeacher, test_type: str):
    message, instruction, personality = make_message_for_TestChecker_Agent(questions, answers, teacher, test_type)

    agent = Agent(
        model="gemini-2.5-flash",
        name="TestChecker_Agent",
        description=personality,
        instruction=instruction
    )

    try:
        response_text = asyncio.run(_run_agent(agent, message))
        response_text = extract_json(response_text)
        parsed = json.loads(response_text)

        if isinstance(parsed, list):
            return parsed
        elif isinstance(parsed, dict):
            return parsed.get("questions", [])
        else:
            print(f"Unexpected JSON structure: {parsed}")
            return []

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}\nResponse: {response_text}")
        return []
    except Exception as e:
        print(f"Unexpected agent error: {e}")
        return []
