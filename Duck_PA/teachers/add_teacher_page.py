from Duck_PA import app

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
        h1 {
            color: #333;
            text-align: center; /* Ensures the title is always centered */
        }
        label {
            display: block;
            margin-top: 10px;
            font-weight: bold;
        }
        input[type="text"], textarea, select {
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
