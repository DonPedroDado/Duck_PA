import google.generativeai as genai
from pydantic import BaseModel
import os
from flask import Flask, request, jsonify
import json
import re

class Question(BaseModel):
    question: str
    type: str
    options: list[str]
    correct_answer: str

class QuestionsList(BaseModel):
    questions: list[Question]

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


auth_token = os.getenv("GEMINI_API_KEY")  # Get the authentication token from an environment variable
genai.configure(api_key=auth_token)
model = genai.GenerativeModel("gemini-1.5-flash")

teacher1 = ClassTeacher(1, "William Thompson", ["Mathematics", "Computer science"], "Calm")
teacher2 = ClassTeacher(2, "Rachel Green", ["Physics", "Chemistry"], "Strict")
teacher3 = ClassTeacher(3, "Albert Taylor", ["Biology", "Geology"], "Friendly")
teacher4 = ClassTeacher(4, "Ira Abruzzo", ["English", "German", "Linguistics"], "Angry")

teachers = [teacher1, teacher2, teacher3, teacher4]

@app.route("/get_teachers", methods=["GET"])
def get_teachers():
    teachers_data = [t.to_dict() for t in teachers]
    return jsonify({"teachers": teachers_data})

@app.route("/delete_teacher/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    """
    Deletes a teacher by ID.
    """
    global teachers
    teachers = [teacher for teacher in teachers if teacher.id != teacher_id]
    return jsonify({"message": "Teacher deleted successfully"}), 200

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

def ask_AI(topic: str, teacher: ClassTeacher, question_type: str):
    # model is already initialized globally
    message = (
        f"You must make questions for them. You are teacher called {teacher.name}. "
        f"Your specializations are {', '.join(teacher.specialization)} and your attitude is {teacher.attitude}. "
        f"I want you to create a test about the following topic: {topic}. "
        f"The type of the question is {question_type}."
    )



    if question_type == "Multiple Choice Tests":
        message += "You are going to create a Multiple Choice Test. I want you to create 10 questions and for each question to provide 4 possible answers. One is correct, one is almost correct, the other one is neutral and one is clearly wrong."
        message += """I want you to return the result as a JSON. The schema of the JSON should be the following: questions": [
                {
                    "question": "Sample Multiple Choice Question 1",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"]
                },
                {
                    "question": "Another question",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"]
                }
            ]"""
        message += "You are going to reply only if the JSON described above and NOTHING ELSE. Make sure the question only have one possible answer."

    elif question_type == "True/False Tests":
        message += "You are going to create a True/False Test. I want you to create 10 questions. Each question should have a sentence and the answer should be either True or False. I want you to return the result as a JSON. The schema of the JSON should be the following:"
        message += """questions": [
                {
                    "question": "Sample True/False Question 1: The capital of France is Paris.",
                    "type": "true_false"
                },
                {
                    "question": "Another True/False Question: The capital of Italy is Rome.",
                    "type": "true_false"
                }
            ]"""
        message += "You are going to reply only if the JSON described above and NOTHING ELSE"

    elif question_type == "Fill-in-the-Blank Tests":
        message += "You are going to create a Fill-in-the-Blank Test. I want you to create 10 questions. Each question should have a sentence with a blank space. I want you to return the result as a JSON. The schema of the JSON should be the following:"
        message += """questions": [
                {
                    "question": "Sample Fill-in-the-Blank Question 1: The capital of France is __________.",
                    "type": "fill_in_the_blank"
                },
                {
                    "question": "Another Fill-in-the-Blank Question: The capital of Italy is __________.",
                    "type": "fill_in_the_blank"
                }
            ]"""
        message += "You are going to reply only if the JSON described above and NOTHING ELSE. Make sure that the excercises yoou maked are understandable and make sure that the excercises you make are specific for the topic. If the topic is something connected to grammar(like tenses, for example:past participle, simple part, and so on) make sure you put the infinitive form in brackets. Make sure to put a blank space in the place where the answer should be."   



    response = model.generate_content(message,
                                      generation_config={
                                          'response_mime_type': 'application/json',
                                      },)

    message2=(
        f"This is the input I gave you before: {message}"
        f"This is the output you gave me: {response}"
        f"Check the output and fix the json. Like the questions and the explanations and so on."
    )    

    response2 = model.generate_content(message,
                                    generation_config={
                                        'response_mime_type': 'application/json',
                                    },)

    print(response2)

    try:
        my_questions = response2.text
        my_questions_json = json.loads(my_questions).get("questions")
        return my_questions_json
    except Exception as e:
        print(f"Error: {e}")
        return None




@app.route("/add_teacher", methods=["GET"])
def add_teacher_page():
    """
    Returns the page for adding a new teacher.
    """
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Add Teacher</title>
    <style>
        .specialization-row {
            display: flex;
            align-items: center;
        }
        .specialization-row input {
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <h1>Add a New Teacher</h1>
    <form id="create-teacher-form" onsubmit="createTeacher(event)">
        <div>
            <label for="first-name">First Name:</label>
            <input type="text" id="first-name" name="first-name" required>
        </div>
        <div>
            <label for="last-name">Last Name:</label>
            <input type="text" id="last-name" name="last-name" required>
        </div>
        <div id="specializations">
            <label>Specializations:</label>
            <div class="specialization-row">
                <input type="text" name="specialization" required>
                <button type="button" onclick="addSpecialization()">+</button>
            </div>
        </div>
        <div>
            <label>Attitude:</label>
            <button type="button" onclick="setAttitude('Strict')">Strict</button>
            <button type="button" onclick="setAttitude('Friendly')">Friendly</button>
            <button type="button" onclick="setAttitude('Angry')">Angry</button>
            <button type="button" onclick="setAttitude('Calm')">Calm</button>
        </div>
        <input type="hidden" id="attitude" name="attitude" required>
        <button type="submit">Create Teacher</button>
    </form>
    <button onclick="window.location.href='/'">Go Back</button>
    <script>
        function addSpecialization() {
            const specializationsDiv = document.getElementById('specializations');
            const newRow = document.createElement('div');
            newRow.className = 'specialization-row';
            newRow.innerHTML = '<input type="text" name="specialization" required><button type="button" onclick="removeSpecialization(this)">-</button>';
            specializationsDiv.appendChild(newRow);
        }

        function removeSpecialization(button) {
            button.parentElement.remove();
        }

        function setAttitude(attitude) {
            document.getElementById('attitude').value = attitude;
        }

        function createTeacher(event) {
            event.preventDefault();
            const form = document.getElementById('create-teacher-form');
            const formData = new FormData(form);
            const data = {
                first_name: formData.get('first-name'),
                last_name: formData.get('last-name'),
                specializations: Array.from(formData.getAll('specialization')),
                attitude: formData.get('attitude')
            };

            fetch('/create_teacher', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.href = '/';
            })
            .catch(err => {
                console.error('Error creating teacher:', err);
            });
        }
    </script>
</body>
</html>
    """






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
    <button onclick="window.location.href='/add_teacher'">Make Teacher</button>

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
                    <button onclick="deleteTeacher(${teacher.id})">Delete</button>
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

    function deleteTeacher(teacherId) {
        fetch(`/delete_teacher/${teacherId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.reload();
        })
        .catch(err => {
            console.error('Error deleting teacher:', err);
        });
    }
    </script>
</body>
</html>
    """

def ask_AI_for_test(teacher, topic, test_type):
    response = ask_AI(topic=topic, teacher=teacher, question_type=test_type)

    if test_type == "Multiple Choice Tests":
        return {
            "title": f"{test_type} on {topic}",
            "teacher_type": str(teacher),
            "questions": response,
        }
    elif test_type == "True/False Tests":
        return {
            "title": f"{test_type} on {topic}",
            "teacher_type": str(teacher),
            "questions": response,
        }
    elif test_type == "Fill-in-the-Blank Tests":
        return {
            "title": f"{test_type} on {topic}",
            "teacher_type": str(teacher),
            "questions": response,
        }
    else:
        return {
            "title": f"Unknown Test Type on {topic}",
            "teacher_type": str(teacher),
            "questions": []
        }
    
def check_Test(test_type: str, questions: list, answers: list):
    feedback = []
    all_correct = True
    score = 0

    message3=(
        f"You got the questions and the answers to them. The number of a question matches with number of an answer. Check if the answers are correct."
    )

    for i, (q, a) in enumerate(zip(questions, answers), start=1):
        append_question = q.get("question", "N/A")
        message3 += f"This is the question {i}: {append_question}\n"

        if isinstance(a, dict):  # Check if 'a' is a dictionary before calling .get()
            append_answer = a.get("answer", "N/A")
        else:
            append_answer = str(a)
            
        message3 += f"This is the answer {i}: {append_answer}\n"

        if test_type == "Multiple Choice Tests":
            append_options = q.get("options", [])
            message3 += f"These are the options for question {i}: {append_options}\n"

    message3 += """
                Respond to every question with a JSON. It should look like this:

                {
                    "question": "the question",
                    "answer": "answer the user gave to the question",
                    "correct_answer": "the right answer",
                    "explanation": "explanation why the answer is wrong"
                }
                """

    response3=model.generate_content(message3,
                                      generation_config={
                                          'response_mime_type': 'application/json',
                                      },)
    
    json_response=json.loads(response3.text)

    print(json_response)

    if test_type == "Multiple Choice Tests":
        for i in json_response:
            correct_answer = json_response.get("correct_answer")
            explanation = json_response.get("explanation", "No explanation provided.")
            answer=json_response.get("answer")
            print(answer)
            print(correct_answer)
            print(explanation)
            if correct_answer != answer:
                all_correct = False
                feedback.append({
                    "question": json_response.get("question"),
                    "your_answer": answer,
                    "correct_answer": correct_answer,
                    "explanation": explanation
                })
            else:
                score += 1
    elif test_type == "True/False Tests":
        for i in json_response:
            correct_answer = json_response.get("correct_answer")
            explanation = json_response.get("explanation", "No explanation provided.")
            answer=json_response.get("answer")
            if correct_answer != answer:
                all_correct = False
                feedback.append({
                    "question": json_response.get("question"),
                    "your_answer": answer,
                    "correct_answer": correct_answer,
                    "explanation": explanation
                })
            else:
                score += 1
    elif test_type == "Fill-in-the-Blank Tests":
        for i in json_response:
            correct_answer = json_response.get("correct_answer")
            explanation = json_response.get("explanation", "No explanation provided.")
            answer=json_response.get("answer")
            if correct_answer.lower() != answer.lower():  # Case insensitive comparison
                all_correct = False
                feedback.append({
                    "question": json_response.get("question"),
                    "your_answer": answer,
                    "correct_answer": correct_answer,
                    "explanation": explanation
                })
            else:
                score += 1
    else:
        return False, [], 0

    return all_correct, feedback, score



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
    print(test_type)
    # Find the teacher object
    selected_teacher = None
    for t in teachers:
        if str(t.id) == str(teacher_id):
            selected_teacher = t
            break

    # Call the mock AI function to get the test structure
    ai_test_data = ask_AI_for_test(selected_teacher, topic, test_type)

    # Now we convert that structured data into HTML
    # We'll do a simple conversion based on the question types
    title = ai_test_data.get("title", "No Title")
    questions = ai_test_data.get("questions", [])

    # Let's build the HTML content step by step
    test_content = f"""
    <h2>{title}</h2>
    <p>Teacher: {selected_teacher.name}</p>
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

    # Return the HTML test page
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Generated Test</title>
</head>
<body>
    <form id="test-form" onsubmit="submitTest(event)">
        {test_content}
        <button type="submit">Submit Test</button>
    </form>
    <script>
    function submitTest(event) {{
        event.preventDefault();

        // Gather the data
        let testType = "{test_type}";
        let questions = {questions};
        let answers = [];

        // Example of collecting answers
        questions.forEach((question, idx) => {{
            let answer;
            if (question.type === "fill_in_the_blank") {{
                answer = [];
                let blanks = document.querySelectorAll(`input[name^='q${{idx + 1}}_blank']`);
                blanks.forEach(blank => {{
                    answer.push(blank.value);
                }});
                answers.push(answer.join(" "));
            }} else {{
                answer = document.querySelector(`input[name='q${{idx + 1}}']:checked`);
                if (answer) {{
                    answers.push(answer.value);
                }} else {{
                    let textAnswer = document.querySelector(`input[name='q${{idx + 1}}']`);
                    if (textAnswer) {{
                        answers.push(textAnswer.value);
                    }}
                }}
            }}
        }});

        let payload = {{
            test_type: testType,
            questions: questions,
            answers: answers
        }};

        fetch('/submit_test', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify(payload)
        }})
        .then(response => response.json())
        .then(data => {{
            if (data.all_correct) {{
                alert("All answers are correct!");
            }} else {{
                let feedbackHtml = "<h2>Feedback</h2><ul>";
                data.feedback.forEach(item => {{
                    feedbackHtml += `<li><strong>Question:</strong> ${{item.question}}<br><strong>Your Answer:</strong> ${{item.your_answer}}<br><strong>Correct Answer:</strong> ${{item.correct_answer}}<br><strong>Explanation:</strong> ${{item.explanation}}</li>`;
                }});
                feedbackHtml += `</ul><p><strong>Total Score:</strong> ${{data.score}} out of 10</p>`;
                document.open();
                document.write(feedbackHtml);
                document.close();
            }}
        }})
        .catch(err => {{
            console.error('Error submitting test:', err);
        }});
    }}
    </script>
    <hr>
    <button onclick="window.history.back()">Go Back</button>
</body>
</html>
    """


@app.route("/submit_test", methods=["POST"])
def submit_test():
    """
    Accepts JSON with {test_type, questions, answers}
    Returns a JSON response indicating if the answers are correct.
    """
    data = request.get_json()
    test_type = data.get("test_type", "")
    questions = data.get("questions", [])
    answers = data.get("answers", [])

    # Use the check_Test function to evaluate the answers
    all_correct, feedback, score = check_Test(test_type, questions, answers)

    return jsonify({"all_correct": all_correct, "feedback": feedback, "score": score})

if __name__ == "__main__":
    app.run(debug=True)