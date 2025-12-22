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

    # Prepare the list for the AI
    qa_pairs = []
    for i, (q, a) in enumerate(zip(questions, answers), start=1):
        qa_pairs.append({
            "question": q.get("question", ""),
            "user_answer": a
        })

    # Compose the prompt for the AI model
    prompt = (
        f"{message3}\n"
        f"{qa_pairs}\n"
        "For each question, evaluate if the user's answer is correct. "
        "For essay questions, judge based on relevance, completeness, and correctness. "
        "Return a JSON list with: question, user_answer, correct_answer (True/False), explanation."
    )

    # Get AI response
    ai_response = model.generate_content(prompt)
    try:
        json_response = ai_response.text
        import json
        json_response = json.loads(json_response)
    except Exception as e:
        return False, [{"error": f"AI response error: {e}"}], 0

    # Scoring logic for all test types, including essay
    for item in json_response:
        if not isinstance(item, dict):
            continue
        answer = item.get("user_answer", "No answer provided")
        explanation = item.get("explanation", "No explanation provided.")
        is_correct = str(item.get("correct_answer", "")).lower() in ["yes", "true", "correct", "1"]
        if not is_correct:
            all_correct = False
        else:
            score += 1
        feedback.append({
            "question": item.get("question"),
            "your_answer": answer,
            "explanation": explanation
        })

    return all_correct, feedback,