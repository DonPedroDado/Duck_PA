window.onload = function () {
    fetchTeachers();
};

function fetchTeachers() {
    fetch('/get_teachers')
        .then(response => response.json())
        .then(data => {
            const teacherList = document.querySelector('.teacher-list');
            teacherList.innerHTML = '';

            if (data.teachers.length === 0) {
                teacherList.innerHTML = `
                    <div class="no-teachers">
                        <p>No teachers available. Please add a teacher first.</p>
                    </div>
                `;
                return;
            }

            data.teachers.forEach(teacher => {
                const teacherItem = document.createElement('div');
                teacherItem.className = 'teacher-item';
                teacherItem.innerHTML = `
                    <div class="teacher-info">
                        <input type="radio" name="teacher" value="${teacher.id}" id="teacher-${teacher.id}" required>
                        <label for="teacher-${teacher.id}">
                            <strong>${teacher.name}</strong><br>
                            ${teacher.specialization.join(', ')}<br>
                            <em>${teacher.attitude}</em>
                        </label>
                    </div>
                    <button onclick="deleteTeacher(${teacher.id})" class="secondary-button">Delete</button>
                `;
                teacherList.appendChild(teacherItem);

                // Add click handler for the entire teacher item
                teacherItem.addEventListener('click', function(e) {
                    if (e.target.tagName !== 'BUTTON') {
                        const radio = this.querySelector('input[type="radio"]');
                        radio.checked = true;
                        updateTeacherSelection();
                    }
                });
            });

            // Add change listeners to radio buttons
            document.querySelectorAll('input[name="teacher"]').forEach(radio => {
                radio.addEventListener('change', updateTeacherSelection);
            });
        })
        .catch(err => {
            console.error('Error fetching teachers:', err);
            const teacherList = document.querySelector('.teacher-list');
            teacherList.innerHTML = '<p>Error loading teachers. Please try again.</p>';
        });
}

function updateTeacherSelection() {
    const teacherError = document.getElementById('teacher-error');
    const selectedTeacher = document.querySelector('input[name="teacher"]:checked');
    
    // Update all teacher items
    document.querySelectorAll('.teacher-item').forEach(item => {
        const radio = item.querySelector('input[type="radio"]');
        item.classList.toggle('selected', radio.checked);
    });

    // Hide error message if a teacher is selected
    if (selectedTeacher) {
        teacherError.style.display = 'none';
    }
}

function generateTest() {
    const selectedTeacher = document.querySelector('input[name="teacher"]:checked');
    const teacherError = document.getElementById('teacher-error');
    
    if (!selectedTeacher) {
        teacherError.style.display = 'block';
        document.getElementById('teacher-selection').scrollIntoView({ behavior: 'smooth' });
        return;
    }

    // Validate other required fields
    const requiredFields = ['test-topic', 'test-type', 'test-difficulty', 'test-questionsnumber', 'test-language'];
    for (const fieldId of requiredFields) {
        const field = document.getElementById(fieldId);
        if (!field.value.trim()) {
            field.focus();
            return;
        }
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
