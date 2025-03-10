from flask import jsonify
from Duck_PA.teachers.teachers import teachers
from Duck_PA import app

@app.route("/get_teachers", methods=["GET"])
def get_teachers():
    teachers_data = [t.to_dict() for t in teachers]
    return jsonify({"teachers": teachers_data})