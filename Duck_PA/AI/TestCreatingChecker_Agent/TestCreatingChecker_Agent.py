from google.adk.agents.llm_agent import Agent
from make_message_for_TestCreatingChecker_Agent import make_review_message
from Duck_PA.teachers.classteacher import ClassTeacher
import json

def review_test(test_json: dict, teacher: ClassTeacher, language: str):
    message, personality = make_review_message(test_json, teacher, language)

    TestCreatingChecker_Agent = Agent(
        model='gemini-2.5-flash-lite',
        name='TestCreatingChecker_Agent',
        description=personality,
        instruction=message,
    )

    try:
        response = TestCreatingChecker_Agent.ask(message)

        parsed = json.loads(response.text)
        questions = parsed.get("questions", [])

        if not questions:
            print("Warning: No questions found in review response.")
            return []

        return questions

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response text: {response.text}")
        return []

    except Exception as e:
        print(f"Unexpected error while asking review agent: {e}")
        return []
