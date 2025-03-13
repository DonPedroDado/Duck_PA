from Duck_PA import app
from flask import request
from Duck_PA.teachers.teachers import teachers
from Duck_PA.AI.ask_ai_for_test import ask_AI_for_test
import re

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
    test_difficulty = data.get("test_difficulty", "Normal")
    test_language = data.get("test_language", "english")
    # Find the teacher object
    selected_teacher = None
    for t in teachers:
        if str(t.id) == str(teacher_id):
            selected_teacher = t
            break

    ai_test_data = ask_AI_for_test(selected_teacher, topic, test_type, difficulty=test_difficulty, language=test_language)

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
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden; /* Prevents unnecessary scrolling */
        }}
        .container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 80%;
            max-width: 600px;
            max-height: 90vh; /* Ensures the content fits within the screen */
            overflow-y: auto; /* Enables scrolling if content is too long */
        }}
        h2 {{
            color: #333;
            text-align: center; /* Ensures the title is always centered */
        }}
        p {{
            color: #333;
        }}
        input[type="text"], input[type="radio"] {{
            margin: 10px 0;
        }}
        button {{
            padding: 10px 20px;
            margin: 10px 5px;
            border: none;
            border-radius: 4px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #0056b3;
        }}
        .feedback-container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 80%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
            margin-top: 20px;
        }}
        .feedback-container h2 {{
            color: #333;
            text-align: center;
        }}
        .feedback-container ul {{
            list-style-type: none;
            padding: 0;
        }}
        .feedback-container li {{
            background-color: #f9f9f9;
            margin: 10px 0;
            padding: 10px;
            border-radius: 4px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }}
        .feedback-container li strong {{
            display: block;
            margin-bottom: 5px;
        }}
        .feedback-container p {{
            text-align: center;
            font-weight: bold;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <form id="test-form" onsubmit="submitTest(event)">
            {test_content}
            <button type="submit">Submit Test</button>
        </form>
        <button onclick="window.history.back()">Go Back</button>
    </div>
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
                let feedbackHtml = `
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f9;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            overflow: hidden; /* Prevents unnecessary scrolling */
                        }}
                        .feedback-container {{
                            background-color: white;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            width: 80%;
                            max-width: 600px;
                            max-height: 90vh;
                            overflow-y: auto;
                            margin-top: 20px;
                        }}
                        .feedback-container h2 {{
                            color: #333;
                            text-align: center;
                        }}
                        .feedback-container ul {{
                            list-style-type: none;
                            padding: 0;
                        }}
                        .feedback-container li {{
                            background-color: #f9f9f9;
                            margin: 10px 0;
                            padding: 10px;
                            border-radius: 4px;
                            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
                        }}
                        .feedback-container li strong {{
                            display: block;
                            margin-bottom: 5px;
                        }}
                        .feedback-container p {{
                            text-align: center;
                            font-weight: bold;
                            color: #333;
                        }}
                    </style>
                </head>
                <body>
                    <div class="feedback-container">
                        <h2>Feedback</h2>
                        <ul>`;
                data.feedback.forEach(item => {{
                    feedbackHtml += `<li><strong>Question:</strong> ${{item.question}}<br><strong>Your Answer:</strong> ${{item.your_answer}}<br><strong>Correct Answer:</strong> ${{item.correct_answer}}<br><strong>Explanation:</strong> ${{item.explanation}}</li>`;
                }});
                feedbackHtml += `</ul><p><strong>Total Score:</strong> ${{data.score}} out of 10</p></div>
                </body>
                </html>`;
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
</body>
</html>
    """