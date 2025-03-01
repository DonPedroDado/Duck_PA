from flask import request, jsonify
from Duck_PA.teachers.classteacher import ClassTeacher
from Duck_PA.teachers.teachers import teachers

@app.route("/create_teacher", methods=["POST"])
def create_teacher():
    """
    Accepts JSON with {first_name, last_name, specializations, attitude}
    Adds a new teacher to the list of teachers.
    """
    data = request.get_json()
    new_teacher = ClassTeacher(
        id=len(teachers) + 1,
        name=f"{data.get('first_name')} {data.get('last_name')}",
        specialization=data.get("specializations"),
        attitude=data.get("attitude")
    )
    teachers.append(new_teacher)
    return jsonify({"message": "Teacher created successfully"}), 201