window.onload = function () {
    fetchTeachers();
};

function fetchTeachers() {
    fetch('/get_teachers')
        .then(response => response.json())
        .then(data => {
            const teacherList = document.querySelector('.teacher-list');
            teacherList.innerHTML = '';

            data.teachers.forEach(teacher => {
                const teacherItem = document.createElement('div');
                teacherItem.className = 'teacher-item';
                teacherItem.innerHTML = `
                    <div class="teacher-info">
                        <input type="radio" name="teacher" value="${teacher.id}" id="teacher-${teacher.id}">
                        <label for="teacher-${teacher.id}">
                            <strong>${teacher.name}</strong><br>
                            ${teacher.specialization.join(', ')}<br>
                            <em>${teacher.attitude}</em>
                        </label>
                    </div>
                    <button onclick="deleteTeacher(${teacher.id})" class="secondary-button">Delete</button>
                `;
                teacherList.appendChild(teacherItem);
            });
        })
        .catch(err => {
            console.error('Error fetching teachers:', err);
        });
}

function generateTest() {
    const selectedTeacher = document.querySelector('input[name="teacher"]:checked');
    if (!selectedTeacher) {
        alert("Please select a teacher first!");
        return;
    }

    const payload = {
        teacher_id: selectedTeacher.value,
        topic: document.getElementById('test-topic').value,
        test_type: document.getElementById('test-type').value,
        test_difficulty: document.getElementById('test-difficulty').value,
        test_language: document.getElementById('test-language').value,
        test_questionsnumber: document.getElementById('test-questionsnumber').value
    };

    document.getElementById('result-area').innerHTML = '<div class="loading">Generating test...</div>';

    // Create a form and submit it to get a proper page load
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/generate_test';

    // Add the payload as hidden fields
    for (const key in payload) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = payload[key];
        form.appendChild(input);
    }

    // Add the form to the body and submit it
    document.body.appendChild(form);
    form.submit();
}

function deleteTeacher(teacherId) {
    if (!confirm('Are you sure you want to delete this teacher?')) {
        return;
    }

    fetch(`/delete_teacher/${teacherId}`, {
        method: 'DELETE'
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.message.includes('deleted successfully')) {
                fetchTeachers();
            }
        })
        .catch(err => {
            console.error('Error deleting teacher:', err);
        });
}
