from Duck_PA.teachers.classteacher import ClassTeacher

def make_review_message(test_json: dict, teacher: ClassTeacher, language: str):
    
    personality = (
        f"You are a teacher called {teacher.name}. "
        f"Your specializations are {', '.join(teacher.specialization)} and your attitude is {teacher.attitude}. "
    )

    instruction = (
        f"You must follow these instructions given below."
        f"You have received a test created by another AI agent. "
        f"Your task is to carefully review and correct it. "
        f"Check each question for correctness, clarity, and completeness. "
        f"Ensure that all questions are accurate, answerable, and specific to the topic. "
        f"For multiple choice questions, make sure there is exactly one correct answer. "
        f"Do not change the JSON schema. "
        f"Reply ONLY with the corrected JSON, NOTHING ELSE."
    )

    message = (
        f"All text should remain in {language}. "
        f"Here is the test to review:\n{test_json}"
    )

    return message, instruction, personality