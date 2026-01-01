from Duck_PA.AI.TestCreating_Agent.TestCreating_Agent import ask_for_test
from Duck_PA.AI.TestCreatingChecker_Agent.TestCreatingChecker_Agent import review_test
from Duck_PA.teachers.classteacher import ClassTeacher

def generate_and_review_test(topic: str, teacher: ClassTeacher, question_type: str, difficulty: str, language: str, number_of_questions: int):
    questions = ask_for_test(topic, teacher, question_type, difficulty, language, number_of_questions)

    corrected_questions = review_test(questions, teacher, language)

    return corrected_questions


def format_test_output(teacher: ClassTeacher, topic: str, test_type: str, questions: list):
    return {
        "title": f"{test_type} on {topic}",
        "teacher_type": str(teacher),
        "questions": questions
    }
