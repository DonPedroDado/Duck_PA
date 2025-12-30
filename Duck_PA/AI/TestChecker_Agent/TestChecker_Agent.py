from google.adk.agents.llm_agent import Agent
from make_message_for_TestChecker_Agent import make_message_for_TestChecker_Agent
from Duck_PA.teachers.classteacher import ClassTeacher
import json

def check_test_with_agent(questions: list, answers: list, teacher: ClassTeacher, test_type: str):
    message, personality = make_message_for_TestChecker_Agent(questions, answers, teacher, test_type)

    TestChecker_Agent = Agent(
        model='gemini-2.5-flash-lite',
        name='TestChecker_Agent',
        description=personality,
        instruction=message,
    )

    try:
        response = TestChecker_Agent.ask(message)

        parsed = json.loads(response.text)
        feedback = parsed if isinstance(parsed, list) else []

        if not feedback:
            print("Warning: No feedback returned by the agent.")
            return []

        return feedback

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response text: {response.text}")
        return []

    except Exception as e:
        print(f"Unexpected error while asking TestChecker agent: {e}")
        return []
