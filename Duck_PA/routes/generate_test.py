from Duck_PA import app
from Duck_PA.AI.generate_test_helpers import generate_and_review_test, format_test_output
from Duck_PA.teachers.teachers import teachers
from flask import request, render_template
import re

@app.route("/generate_test", methods=["GET", "POST"])
def generate_test():
    teacher_id = request.form.get("teacher_id")
    topic = request.form.get("topic", "")
    test_type = request.form.get("test_type", "")
    test_difficulty = request.form.get("test_difficulty", "Normal")
    test_language = request.form.get("test_language", "english")
    test_number_of_questions = int(request.form.get("test_questionsnumber", 10))

    selected_teacher = next((t for t in teachers if str(t.id) == str(teacher_id)), None)
    if not selected_teacher:
        return render_template(
            'generated_test.html',
            title="No Teacher Selected",
            teacher_name="Unknown",
            test_content="<p>No teacher selected or teacher not found.</p>",
            test_type=test_type,
            questions=[],
            test_number_of_questions=test_number_of_questions
        )

    questions = generate_and_review_test(
        topic=topic,
        teacher=selected_teacher,
        question_type=test_type,
        difficulty=test_difficulty,
        language=test_language,
        number_of_questions=test_number_of_questions
    )

    ai_test_data = format_test_output(
        teacher=selected_teacher,
        topic=topic,
        test_type=test_type,
        questions=questions
    )

    test_content = ""
    if not ai_test_data["questions"]:
        test_content += "<p>No questions available or unknown test type.</p>"
    else:
        for idx, q in enumerate(ai_test_data["questions"], start=1):
            question_text = q.get("question", "Untitled Question")
            question_type = q.get("type", "unknown")

            if question_type == "multiple_choice":
                options = q.get("options", [])
                test_content += f"<p><strong>Question {idx}:</strong> {question_text}</p>\n<ul>"
                for opt in options:
                    test_content += f"<li><input type='radio' name='q{idx}' value='{opt}'> {opt}</li>"
                test_content += "</ul><hr>"

            elif question_type == "true_false":
                test_content += f"<p><strong>Question {idx}:</strong> {question_text}</p>\n"
                test_content += f"<input type='radio' name='q{idx}' value='True'> True\n"
                test_content += f"<input type='radio' name='q{idx}' value='False'> False\n<hr>"

            elif question_type == "fill_in_the_blank":
                question_text = re.sub(
                    r"__________",
                    lambda m, idx=idx: f"<input type='text' name='q{idx}_blank{m.start()}' style='width:100px;'>",
                    question_text
                )
                test_content += f"<p><strong>Question {idx}:</strong> {question_text}</p><hr>"

            elif question_type == "essay":
                test_content += f"<p><strong>Question {idx}:</strong> {question_text}</p>\n"
                test_content += f"<textarea name='q{idx}' rows='6' cols='80' placeholder='Write your answer here...'></textarea><hr>"

            else:
                test_content += f"<p><strong>Question {idx} (Unknown type):</strong> {question_text}</p><hr>"

    return render_template(
        'generated_test.html',
        title=ai_test_data["title"],
        teacher_name=selected_teacher.name,
        test_content=test_content,
        test_type=test_type,
        questions=ai_test_data["questions"],
        test_number_of_questions=test_number_of_questions
    )
