from Duck_PA.AI.ask_ai import ask_AI

def ask_AI_for_test(teacher, topic, test_type):
    response = ask_AI(topic=topic, teacher=teacher, question_type=test_type)

    if test_type == "Multiple Choice Tests":
        return {
            "title": f"{test_type} on {topic}",
            "teacher_type": str(teacher),
            "questions": response,
        }
    elif test_type == "True/False Tests":
        return {
            "title": f"{test_type} on {topic}",
            "teacher_type": str(teacher),
            "questions": response,
        }
    elif test_type == "Fill-in-the-Blank Tests":
        return {
            "title": f"{test_type} on {topic}",
            "teacher_type": str(teacher),
            "questions": response,
        }
    else:
        return {
            "title": f"Unknown Test Type on {topic}",
            "teacher_type": str(teacher),
            "questions": []
        }