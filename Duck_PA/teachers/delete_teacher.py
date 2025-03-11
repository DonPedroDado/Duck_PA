from flask import jsonify
from Duck_PA import app
from Duck_PA.teachers.teachers import teachers

def get_teacher_and_remaining(teacher_id):
    teacher_to_delete = next((t for t in teachers if t.id == teacher_id), None)
    remaining_teachers = [teacher for teacher in teachers if teacher.id != teacher_id]
    return teacher_to_delete, remaining_teachers

def define_variables(teacher_id):
    teacher_to_delete, remaining_teachers = get_teacher_and_remaining(teacher_id)
    return teacher_to_delete, remaining_teachers

@app.route("/delete_teacher/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    """
    Deletes a teacher by ID.
    """
    global teachers
    teacher_to_delete, remaining_teachers = define_variables(teacher_id)
    
    if teacher_to_delete is None:
        return jsonify({"error": "Teacher not found"}), 404
    
    teachers = remaining_teachers
    return jsonify({"message": f"{teacher_id} deleted successfully"}), 200