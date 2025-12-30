import json
from Duck_PA.teachers.classteacher import ClassTeacher

def make_message_for_TestChecker_Agent(questions: list, answers: list, teacher: ClassTeacher, test_type: str):
    qa_pairs = []
    for i, (q, a) in enumerate(zip(questions, answers), start=1):
        qa_pairs.append({
            "question_number": i,
            "question": q.get("question", ""),
            "question_type": q.get("type", ""),
            "user_answer": a
        })

    personality = (
        f"You are an AI assistant that acts as a knowledgeable {teacher.name} "
        f"with specializations in {', '.join(teacher.specialization)} and attitude '{teacher.attitude}'. "
        f"You check students' submitted tests and provide detailed feedback."
    )

    if test_type == "Essay Tests":
        message = (
            f"You got the questions and the answers to them. The number of a question matches with the number of an answer. "
            f"Questions and answers: {json.dumps(qa_pairs, indent=2)}\n"
            "For each essay question, evaluate the user's answer based on:\n"
            "1. Relevance to the question\n"
            "2. Completeness and depth\n"
            "3. Accuracy and correctness\n"
            "4. Quality of reasoning\n"
            "Provide constructive feedback and explanation for each answer. "
            "Return ONLY a valid JSON array with fields: question_number, question, user_answer, is_correct, correct_answer, explanation. "
            "Do not include any text before or after the JSON array. "
            "Ensure all strings are properly formatted with escaped characters."
        )
    else:
        message = (
            f"You got the questions and the answers to them. The number of a question matches with the number of an answer. "
            f"Questions and answers: {json.dumps(qa_pairs, indent=2)}\n"
            "For each question, evaluate if the user's answer is correct. "
            "Return ONLY a valid JSON array with fields: question_number, question, user_answer, is_correct, correct_answer, explanation. "
            "Do not include any text before or after the JSON array. "
            "Ensure all strings are properly formatted with escaped characters."
        )

    return message, personality