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