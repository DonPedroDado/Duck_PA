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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #e9ecef;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 800px;
            max-height: 90vh;
            overflow-y: auto;
        }
        h1 {
            color: #343a40;
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-top: 10px;
            font-weight: bold;
            color: #495057;
        }
        input[type="text"], textarea, select {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #ced4da;
            border-radius: 6px;
            font-size: 1rem;
        }
        button {
            padding: 12px 24px;
            margin: 10px 5px;
            border: none;
            border-radius: 6px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #0056b3;
        }
        .specialization-row {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        .specialization-row input {
            margin-right: 10px;
        }
        @media (max-width: 768px) {
            .container {
                width: 95%;
                padding: 20px;
            }
            button {
                width: 100%;
                margin: 10px 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
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
    </div>
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
