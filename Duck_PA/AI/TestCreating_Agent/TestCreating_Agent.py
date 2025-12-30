from google.adk.agents.llm_agent import Agent
from Duck_PA.AI.TestCreating_Agent.make_message_for_TestCreating_Agent import make_message
from Duck_PA.teachers.classteacher import ClassTeacher
import json

def ask_for_test(topic: str, teacher: ClassTeacher, question_type: str, difficulty: str, language: str, number_of_questions: int):
    message, personality = make_message(topic, teacher, question_type, difficulty, language, number_of_questions)

    TestCreating_Agent = Agent(
        model='gemini-2.5-flash-lite',
        name='TestCreating_Agent',
        description=personality,
        instruction=message,
    )

    try:
        response = TestCreating_Agent.ask(message)

        parsed = json.loads(response.text)
        questions = parsed.get("questions", [])

        if not questions:
            print("Warning: No questions found in response.")
            return []

        return questions

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response text: {response.text}")
        return []

    except Exception as e:
        print(f"Unexpected error while asking agent: {e}")
        return []