from Duck_PA import app
from flask import request, render_template, json
from Duck_PA.teachers.teachers import teachers
from Duck_PA.AI.ask_ai_for_test import ask_AI_for_test
import re

@app.route("/generate_test", methods=["POST"])
def generate_test():
    """
    Accepts form data with {teacher_id, topic, test_type}
    Returns a new HTML page containing the generated test.
    We'll now use ask_AI_for_text to simulate calling an AI service
    for generating the actual test content in a structured format,
    then we'll convert that into an HTML layout.
    """
    # Get data from form
    teacher_id = request.form.get("teacher_id")
    topic = request.form.get("topic", "")
    test_type = request.form.get("test_type", "")
    test_difficulty = request.form.get("test_difficulty", "Normal")
    test_language = request.form.get("test_language", "english")
    test_number_of_questions = request.form.get("test_questionsnumber", 10)

    # Find the teacher object
    selected_teacher = None
    for t in teachers:
        if str(t.id) == str(teacher_id):
            selected_teacher = t
            break

    ai_test_data = ask_AI_for_test(selected_teacher, topic, test_type, difficulty=test_difficulty, language=test_language, number_of_questions=test_number_of_questions)

    # Now we convert that structured data into HTML
    # We'll do a simple conversion based on the question types
    title = ai_test_data.get("title", "No Title")
    questions = ai_test_data.get("questions", [])

    # Ensure questions is a valid JSON-serializable list
    try:
        # Test JSON serialization
        json.dumps(questions)
    except Exception as e:
        print(f"Error serializing questions: {e}")
        print(f"Questions data: {questions}")
        questions = []

    # Let's build the HTML content step by step
    test_content = ""
    if not questions:
        # If the AI returned no questions (e.g., unknown test type)
        test_content += "<p>No questions available or unknown test type.</p>"
    else:
        # Loop through questions and build HTML
        for idx, q in enumerate(questions, start=1):
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
                # Replace each blank with an input box using regex
                question_text = re.sub(r"__________", lambda m, idx=idx: f"<input type='text' name='q{idx}_blank{m.start()}' style='width:100px;'>", question_text)
                test_content += f"<p><strong>Question {idx}:</strong> {question_text}</p><hr>"
            else:
                # If we don't recognize the question type
                test_content += f"<p><strong>Question {idx} (Unknown type):</strong> {question_text}</p><hr>"

    return render_template('generated_test.html', 
                         title=title, 
                         teacher_name=selected_teacher.name, 
                         test_content=test_content, 
                         test_type=test_type, 
                         questions=questions, 
                         test_number_of_questions=test_number_of_questions)