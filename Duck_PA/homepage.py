from Duck_PA import app

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
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden; /* Prevents unnecessary scrolling */
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 80%;
            max-width: 600px;
            max-height: 90vh; /* Ensures the content fits within the screen */
            overflow-y: auto; /* Enables scrolling if content is too long */
        }
        h1, h2 {
            color: #333;
            text-align: center; /* Ensures the title is always centered */
        }
        textarea, select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            margin: 10px 5px;
            border: none;
            border-radius: 4px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        #teacher-selection {
            max-height: 200px; /* Ensures all teachers are visible within a scrollable area */
            overflow-y: auto; /* Allows scrolling if there are too many teachers */
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 4px;
            background-color: #f9f9f9;
        }
        #teacher-selection div {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
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

        <div>
            <h2>4. Select the difficulty of the test:</h2>
            <select id="test-difficulty">
                <option value="Easy">Easy</option>
                <option value="Normal">Normal</option>
                <option value="Hard">Hard</option>
                <option value="Very hard">Very hard</option>
                <option value="PhD level">PhD level</option>
            </select>
        </div>

        <div>
            <h2>5. Write number of questions:</h2>
            <textarea id="test-questionsnumber" rows="1" cols="20"></textarea>
        </div>

        <div>
            <h2>6. Write the language:</h2>
            <textarea id="test-language" rows="1" cols="20"></textarea>
        </div>

        <br>
        <button onclick="generateTest()">Generate Test</button>
        <button onclick="window.location.href='/add_teacher'">Make Teacher</button>
    </div>

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
        let testDifficulty = document.getElementById('test-difficulty').value;
        let testLanguage = document.getElementById('test-language').value;
        let testNumber_of_questions = document.getElementById('test-questionsnumber').value;

        let payload = {
            teacher_id: teacherId,
            topic: topic,
            test_type: testType,
            test_difficulty: testDifficulty,
            test_language: testLanguage,
            test_questionsnumber: testNumber_of_questions
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
            if (data.message.includes('deleted successfully')) {
                // Remove the teacher from the DOM
                const teacherElement = document.querySelector(`input[name="teacher"][value="${teacherId}"]`).parentElement;
                teacherElement.remove();
            }
        })
        .catch(err => {
            console.error('Error deleting teacher:', err);
        });
    }
    </script>
</body>
</html>
    """