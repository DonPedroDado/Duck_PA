from Duck_PA import app
from Duck_PA.AI.TestChecker_Agent.TestChecker_Agent import check_test_with_agent
from Duck_PA.teachers.teachers import get_teacher_by_id
from flask import request, jsonify

@app.route("/submit_test", methods=["POST"])
def submit_test():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data received"}), 400
        
    test_type = data.get("test_type")
    questions = data.get("questions", [])
    answers = data.get("answers", [])
    teacher_id = data.get("teacher_id")
    
    if not all([test_type, questions, answers, teacher_id]):
        return jsonify({"error": "Missing required data"}), 400

    teacher = get_teacher_by_id(teacher_id)
    if teacher is None:
        return jsonify({"error": "Invalid teacher_id"}), 400

    feedback = check_test_with_agent(questions, answers, teacher, test_type)
    
    score = sum(1 for f in feedback if f.get("is_correct"))
    all_correct = score == len(feedback)

    return jsonify({
        "all_correct": all_correct,
        "feedback": feedback,
        "score": score
    })