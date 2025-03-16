from Duck_PA import app
from Duck_PA.tests.check_test import check_Test
from flask import request, jsonify

@app.route("/submit_test", methods=["POST"])
def submit_test():
    """
    Accepts JSON with {test_type, questions, answers}
    Returns a JSON response indicating if the answers are correct.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data received"}), 400
        
    test_type = data.get("test_type")
    questions = data.get("questions", [])
    answers = data.get("answers", [])
    
    if not all([test_type, questions, answers]):
        return jsonify({"error": "Missing required data"}), 400

    all_correct, feedback, score = check_Test(test_type, questions, answers)
    
    return jsonify({
        "all_correct": all_correct,
        "feedback": feedback,
        "score": score
    })