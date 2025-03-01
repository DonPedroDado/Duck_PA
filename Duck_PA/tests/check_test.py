import json
from Duck_PA.AI.genai import model

def check_Test(test_type: str, questions: list, answers: list):
    feedback = []
    all_correct = True
    score = 0

    message3 = """
        You got the questions and the answers to them. The number of a question matches with the number of an answer. 
        Check if the answers are correct.

        Here is the list of questions and answers:
    """

    for i, (q, a) in enumerate(zip(questions, answers), start=1):
        question_text = q.get("question", "N/A")
        answer_text = a.get("answer", "N/A") if isinstance(a, dict) else str(a)
        
        message3 += f"""
        {{
            "question": "{question_text}",
            "answer": "{answer_text}"
        }},
        """

        if test_type == "Multiple Choice Tests":
            options = q.get("options", [])
            message3 += f'"options": {options},\n'

    message3 += """
        Respond with a JSON **array** of objects. The output should be formatted as follows:
        
        [
            {
                "question": "The question text",
                "answer": "The answer provided by the user",
                "correct_answer": "The correct answer",
                "explanation": "Explanation for incorrect answers"
            }
        ]
    """

    response3=model.generate_content(message3,
                                    generation_config={
                                        'response_mime_type': 'application/json',
                                    },)
    


    try:
        json_response = json.loads(response3.text) 
        if isinstance(json_response, str):  
            json_response = json.loads(json_response) 
    except json.JSONDecodeError as e:
        return False, [], 0

    if test_type == "Multiple Choice Tests":
        for item in json_response:
            if not isinstance(item, dict):
                continue

            answer = item.get("answer", "No answer provided")
            correct_answer = item.get("correct_answer", "No correct answer provided")
            explanation = item.get("explanation", "No explanation provided.")
            if correct_answer != answer:
                all_correct = False
                feedback.append({
                    "question": item.get("question"),
                    "your_answer": answer,
                    "correct_answer": correct_answer,
                    "explanation": explanation
                })
            else:
                score += 1
    elif test_type == "True/False Tests":
        for item in json_response:
            if not isinstance(item, dict):
                continue
            answer = item.get("answer", "No answer provided")
            correct_answer = item.get("correct_answer", "No correct answer provided")
            explanation = item.get("explanation", "No explanation provided.")
            if correct_answer != answer:
                all_correct = False
                feedback.append({
                    "question": item.get("question"),
                    "your_answer": answer,
                    "correct_answer": correct_answer,
                    "explanation": explanation
                })
            else:
                score += 1
    elif test_type == "Fill-in-the-Blank Tests":
        for item in json_response:
            if not isinstance(item, dict):
                continue
            answer = item.get("answer", "No answer provided")
            correct_answer = item.get("correct_answer", "No correct answer provided")
            explanation = item.get("explanation", "No explanation provided.")
            if correct_answer.lower() != answer.lower():  # Case insensitive comparison
                all_correct = False
                feedback.append({
                    "question": item.get("question"),
                    "your_answer": answer,
                    "correct_answer": correct_answer,
                    "explanation": explanation
                })
            else:
                score += 1
    else:
        return False, [], 0

    return all_correct, feedback, score