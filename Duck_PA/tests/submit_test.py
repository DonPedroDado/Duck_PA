from Duck_PA import app
from flask import request, jsonify
from Duck_PA.tests.check_test import check_Test

@app.route("/submit_test", methods=["POST"])
def submit_test():
    """
    Accepts JSON with {test_type, questions, answers}
    Returns a JSON response indicating if the answers are correct.
    """
    data = request.get_json()
    test_type = data.get("test_type", "")
    questions = data.get("questions", [])
    answers = data.get("answers", [])

    # Use the check_Test function to evaluate the answers
    all_correct, feedback, score = check_Test(test_type, questions, answers)

    return jsonify({"all_correct": all_correct, "feedback": feedback, "score": score})