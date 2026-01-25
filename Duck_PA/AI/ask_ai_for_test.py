from Duck_PA.AI.ask_ai import ask_AI

def ask_AI_for_test(topic, test_type, difficulty, language, number_of_questions: int):
    response = ask_AI(topic=topic, question_type=test_type, difficulty=difficulty, language=language, number_of_questions=number_of_questions)

    if test_type == "Multiple Choice Tests":
        return {
            "title": f"{test_type} on {topic}",
            "questions": response,
        }
    elif test_type == "True/False Tests":
        return {
            "title": f"{test_type} on {topic}",
            "questions": response,
        }
    elif test_type == "Fill-in-the-Blank Tests":
        return {
            "title": f"{test_type} on {topic}",
            "questions": response,
        }
    elif test_type == "Essay Tests":
        return {
            "title": f"{test_type} on {topic}",
            "questions": response,
        }
    else:
        return {
            "title": f"Unknown Test Type on {topic}",
            "questions": []
        }