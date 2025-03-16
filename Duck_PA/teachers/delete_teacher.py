from flask import jsonify
from Duck_PA import app
from Duck_PA.teachers.teachers import teachers

@app.route("/delete_teacher/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    """
    Deletes a teacher by ID.
    """
    global teachers
    teacher_to_delete = next((t for t in teachers if t.id == teacher_id), None)
    
    if teacher_to_delete is None:
        return jsonify({"error": "Teacher not found"}), 404
    
    teachers[:] = [t for t in teachers if t.id != teacher_id]
    return jsonify({"message": f"{teacher_id} deleted successfully"}), 200