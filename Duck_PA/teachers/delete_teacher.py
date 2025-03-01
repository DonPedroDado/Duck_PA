from flask import jsonify
from Duck_PA import app

@app.route("/delete_teacher/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    """
    Deletes a teacher by ID.
    """
    global teachers
    teachers = [teacher for teacher in teachers if teacher.id != teacher_id]
    return jsonify({"message": "Teacher deleted successfully"}), 200