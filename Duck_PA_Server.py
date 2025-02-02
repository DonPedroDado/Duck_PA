from typing import Union
import google.generativeai as genai
from pydantic import BaseModel
from typing import List
import os
from flask import Flask, request, jsonify


class ClassTeacher:
    def __init__(self, id, name, specialization, attitude):
        self.id = id
        self.name = name
        self.specialization = specialization
        self.attitude = attitude

    def to_dict(self):
        """
        Helper method to convert the ClassTeacher instance
        to a dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "attitude": self.attitude
        }


app = Flask(__name__)


auth_token = os.getenv("GEMINI_AUTH_TOKEN")  # Get the authentication token from an environment variable
genai.configure(api_key=auth_token)
model = genai.GenerativeModel("gemini-1.5-flash")

teacher1 = ClassTeacher(1, "William Thompson", ["Mathematics", "Geometry"], "Calm")
teacher2 = ClassTeacher(2, "Rachel Green", ["Physics", "Chemistry"], "Strict")
teacher3 = ClassTeacher(3, "Albert Taylor", ["Biology", "Geology"], "Friendly")

teachers = [teacher1, teacher2, teacher3]

@app.route("/get_teachers", methods=["GET"])
def get_teachers():
    teachers_data = [t.to_dict() for t in teachers]
    return jsonify({"teachers": teachers_data})
@app.route("/", methods=["GET"])
def homepage():
    """
    Returns the main page which is divided into:
      a) Teacher selection (info + radio button or some control to choose).
      b) A text area to specify the test topic.
      c) A selection for the type of test.
    There's also a "Generate Test" button that sends a JSON POST request
    to /generate_test endpoint.
    """
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Test Generator</title>
</head>
<body>
    <h1>Welcome to the Test Generator</h1>

    <div id="teacher-selection">
        <h2>1. Choose a Teacher:</h2>
        <p>Loading teacher list...</p>
    </div>

    <div>
        <h2>2. Write the topic of the test:</h2>
        <textarea id="test-topic" rows="4" cols="50"></textarea>
    </div>

    <div>
        <h2>3. Select the type of test:</h2>
        <select id="test-type">
            <option value="Multiple Choice Tests">Multiple Choice Tests</option>
            <option value="True/False Tests">True/False Tests</option>
            <option value="Fill-in-the-Blank Tests">Fill-in-the-Blank Tests</option>
        </select>
    </div>

    <br>
    <button onclick="generateTest()">Generate Test</button>

    <script>
    // On page load, fetch the teachers and display them
    window.onload = function() {
        fetch('/get_teachers')
        .then(response => response.json())
        .then(data => {
            const teacherDiv = document.getElementById('teacher-selection');
            teacherDiv.innerHTML = '<h2>1. Choose a Teacher:</h2>';
            data.teachers.forEach(teacher => {
                // Build a radio button + summary of teacher
                let teacherInfo = document.createElement('div');
                teacherInfo.innerHTML = `
                    <input type="radio" name="teacher" value="${teacher.id}" />
                    <strong>Name:</strong> ${teacher.name}<br>
                    <strong>Specialization:</strong> ${teacher.specialization.join(', ')}<br>
                    <strong>Attitude:</strong> ${teacher.attitude}
                    <hr>
                `;
                teacherDiv.appendChild(teacherInfo);
            });
        })
        .catch(err => {
            console.error(err);
        });
    };

    function generateTest() {
        // Gather the data
        let selectedTeacher = document.querySelector('input[name="teacher"]:checked');
        if (!selectedTeacher) {
            alert("Please select a teacher first!");
            return;
        }

        let teacherId = selectedTeacher.value;
        let topic = document.getElementById('test-topic').value;
        let testType = document.getElementById('test-type').value;

        let payload = {
            teacher_id: teacherId,
            topic: topic,
            test_type: testType
        };

        fetch('/generate_test', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.text()) // We'll receive HTML
        .then(htmlContent => {
            // Replace the entire document with the returned HTML
            document.open();
            document.write(htmlContent);
            document.close();
        })
        .catch(err => {
            console.error('Error generating test:', err);
        });
    }
    </script>
</body>
</html>
    """


def ask_AI_for_text(teacher_type, topic, test_type):
    """
    This function simulates a call to Gemini AI to create a test.
    In a real scenario, you'd replace this with the actual call to the AI system,
    sending `teacher_type`, `topic`, and `test_type` as part of your prompt or request.

    Returns a JSON-like Python dictionary representing the generated test.
    """

    # Here we build the prompt (mocked). In a real integration,
    # you might do something like: 
    # prompt = f"""
    #   Hello Gemini AI,
    #   Please create a {test_type} test for a teacher of type "{teacher_type}" 
    #   on the topic "{topic}".
    #   Return the test in a JSON structure with a list of questions, etc.
    # """

    # For illustration, we'll return a dummy JSON structure with
    # a single question that changes slightly based on the test_type.
    if test_type == "Multiple Choice Tests":
        return {
            "title": f"{test_type} on {topic}",
            "teacher_type": teacher_type,
            "questions": [
                {
                    "question": f"Sample Multiple Choice Question about {topic}",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A"
                },
                                {
                    "question": f"Another question about {topic}",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A"
                }
            ]
        }
    elif test_type == "True/False Tests":
        return {
            "title": f"{test_type} on {topic}",
            "teacher_type": teacher_type,
            "questions": [
                {
                    "question": f"Sample True/False statement about {topic}",
                    "type": "true_false",
                    "correct_answer": True
                }
            ]
        }
    elif test_type == "Fill-in-the-Blank Tests":
        return {
            "title": f"{test_type} on {topic}",
            "teacher_type": teacher_type,
            "questions": [
                {
                    "question": f"Fill in the blank about {topic}",
                    "type": "fill_in_the_blank",
                    "correct_answer": "SAMPLE_ANSWER"
                }
            ]
        }
    else:
        return {
            "title": f"Unknown Test Type on {topic}",
            "teacher_type": teacher_type,
            "questions": []
        }

@app.route("/generate_test", methods=["POST"])
def generate_test():
    """
    Accepts JSON with {teacher_id, topic, test_type}
    Returns a new HTML page containing the generated test.
    We'll now use ask_AI_for_text to simulate calling an AI service
    for generating the actual test content in a structured format,
    then we'll convert that into an HTML layout.
    """
    data = request.get_json()
    teacher_id = data.get("teacher_id")
    topic = data.get("topic", "")
    test_type = data.get("test_type", "")

    # Find the teacher object
    selected_teacher = None
    for t in teachers:
        if str(t.id) == str(teacher_id):
            selected_teacher = t
            break

    # Fallback if teacher not found
    if not selected_teacher:
        teacher_type = "Unknown"
        teacher_name = "Unknown Teacher"
    else:
        # We'll pass something like the teacher's "attitude" or "specialization"
        # as the "type" - you can modify as needed.
        teacher_type = f"{selected_teacher.attitude} | {', '.join(selected_teacher.specialization)}"
        teacher_name = selected_teacher.name

    # Call the mock AI function to get the test structure
    ai_test_data = ask_AI_for_text(teacher_type, topic, test_type)

    # Now we convert that structured data into HTML
    # We'll do a simple conversion based on the question types
    title = ai_test_data.get("title", "No Title")
    questions = ai_test_data.get("questions", [])

    # Let's build the HTML content step by step
    test_content = f"""
    <h2>{title}</h2>
    <p>Teacher: {teacher_name}</p>
    <hr>
    """

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
                    test_content += f"<li><input type='radio' name='q{idx}'> {opt}</li>"
                test_content += "</ul><hr>"
            elif question_type == "true_false":
                test_content += f"<p><strong>Question {idx}:</strong> {question_text}</p>\n"
                test_content += f"<input type='radio' name='q{idx}'> True\n"
                test_content += f"<input type='radio' name='q{idx}'> False\n<hr>"
            elif question_type == "fill_in_the_blank":
                test_content += f"<p><strong>Question {idx}:</strong> {question_text}</p>\n"
                test_content += f"<input type='text' name='q{idx}' style='width:300px;'><hr>"
            else:
                # If we don't recognize the question type
                test_content += f"<p><strong>Question {idx} (Unknown type):</strong> {question_text}</p><hr>"

    # Return the HTML test page
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Generated Test</title>
</head>
<body>
    {test_content}
    <hr>
    <button onclick="window.history.back()">Go Back</button>
</body>
</html>
    """


if __name__ == "__main__":
    app.run(debug=True)