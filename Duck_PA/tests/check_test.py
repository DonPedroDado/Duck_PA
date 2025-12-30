from Duck_PA.AI.genai import model
import json
import re

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
            "question_number": i,
            "question": q.get("question", ""),
            "question_type": q.get("type", ""),
            "user_answer": a
        })

    # Compose the prompt for the AI model - special handling for essay tests
    if test_type == "Essay Tests":
        prompt = (
            f"{message3}\n"
            f"{json.dumps(qa_pairs, indent=2)}\n"
            "For each essay question, evaluate the user's answer based on:\n"
            "1. Relevance to the question\n"
            "2. Completeness and depth\n"
            "3. Accuracy and correctness\n"
            "4. Quality of reasoning\n"
            "Provide constructive feedback and explanation for each answer. "
            "Return ONLY a valid JSON array with these fields: question_number, question, user_answer, is_correct, correct_answer, explanation. "
            "Do not include any text before or after the JSON array. "
            "Ensure all strings are properly formatted with escaped characters."
        )
    else:
        prompt = (
            f"{message3}\n"
            f"{json.dumps(qa_pairs, indent=2)}\n"
            "For each question, evaluate if the user's answer is correct. "
            "Return ONLY a valid JSON array with these fields: question_number, question, user_answer, is_correct, correct_answer, explanation. "
            "Do not include any text before or after the JSON array. "
            "Ensure all strings are properly formatted with escaped characters."
        )

    # Get AI response
    ai_response = model.generate_content(prompt)
    try:
        response_text = ai_response.text
        
        # Try to extract JSON from the response (in case there's extra text)
        # Look for the first [ and the last ]
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']')
        
        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            json_str = response_text[start_idx:end_idx+1]
            # Clean up common issues with escape sequences
            json_str = json_str.replace('\\"', '"').replace('\\\\', '\\')
            json_response = json.loads(json_str)
        else:
            json_response = json.loads(response_text)
            
    except json.JSONDecodeError as e:
        print(f"Error parsing AI response: {e}")
        print(f"Response text: {response_text[:500]}")  # Print first 500 chars for debugging
        return False, [{"question": "Error", "your_answer": "N/A", "explanation": f"AI response format error. Please try again."}], 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"Response text: {response_text[:500]}")
        return False, [{"question": "Error", "your_answer": "N/A", "explanation": f"Unexpected error: {str(e)}"}], 0

    # Scoring logic for all test types, including essay
    for item in json_response:
        if not isinstance(item, dict):
            continue
        
        question_text = item.get("question", "Unknown question")
        user_answer = item.get("user_answer", "No answer provided")
        explanation = item.get("explanation", "No explanation provided.")
        correct_answer = item.get("correct_answer", "N/A")
        is_correct = item.get("is_correct", False)
        
        # Handle various boolean representations
        if isinstance(is_correct, bool):
            is_correct_bool = is_correct
        else:
            is_correct_bool = str(is_correct).lower() in ["yes", "true", "correct", "1"]
        
        if not is_correct_bool:
            all_correct = False
            # For essay tests, if marked as incorrect, show the user's answer as the "correct answer" 
            # since essays are subjective and the user's answer is their correct response
            if test_type == "Essay Tests":
                correct_answer = user_answer
            
            # Only add wrong answers to feedback
            feedback.append({
                "question": question_text,
                "your_answer": user_answer,
                "correct_answer": correct_answer if correct_answer and correct_answer != "N/A" else user_answer,
                "explanation": explanation,
                "is_correct": is_correct_bool
            })
        else:
            score += 1

    return all_correct, feedback, score