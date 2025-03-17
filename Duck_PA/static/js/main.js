window.onload = function () {
    fetchTeachers();
};

function fetchTeachers() {
    fetch('/get_teachers')
        .then(response => response.json())
        .then(data => {
            const teacherDropdown = document.querySelector('.teacher-dropdown');
            const defaultTeacher = document.getElementById('default-teacher');
            
            // Clear existing options except the placeholder
            while (teacherDropdown.options.length > 1) {
                teacherDropdown.remove(1);
            }

            if (data.teachers.length === 0) {
                defaultTeacher.style.display = 'none';
                teacherDropdown.style.display = 'none';
                document.querySelector('.teacher-list').innerHTML = `
                    <div class="no-teachers">
                        <p>No teachers available. Please add a teacher first.</p>
                    </div>
                `;
                return;
            }

            // Add all teachers except Rachel Green to the dropdown
            data.teachers.forEach(teacher => {
                if (teacher.id !== 2) { // Rachel Green's ID
                    const option = document.createElement('option');
                    option.value = teacher.id;
                    option.textContent = `${teacher.name} (${teacher.specialization.join(', ')})`;
                    teacherDropdown.appendChild(option);
                }
            });

            // Set Rachel Green as selected by default
            const rachelGreen = data.teachers.find(t => t.id === 2);
            if (rachelGreen) {
                defaultTeacher.querySelector('.teacher-name').textContent = rachelGreen.name;
                defaultTeacher.querySelector('.teacher-specialization').textContent = rachelGreen.specialization.join(', ');
                defaultTeacher.querySelector('.teacher-attitude').textContent = rachelGreen.attitude;
                defaultTeacher.dataset.teacherId = rachelGreen.id;
                defaultTeacher.style.display = 'block';
                document.getElementById('teacher-error').style.display = 'none';
            } else {
                defaultTeacher.style.display = 'none';
            }
        })
        .catch(err => {
            console.error('Error fetching teachers:', err);
            document.querySelector('.teacher-list').innerHTML = '<p>Error loading teachers. Please try again.</p>';
        });
}

function selectTeacher(teacherId) {
    if (!teacherId) return;

    fetch('/get_teachers')
        .then(response => response.json())
        .then(data => {
            const teacher = data.teachers.find(t => t.id === parseInt(teacherId));
            if (teacher) {
                const defaultTeacher = document.getElementById('default-teacher');
                defaultTeacher.querySelector('.teacher-name').textContent = teacher.name;
                defaultTeacher.querySelector('.teacher-specialization').textContent = teacher.specialization.join(', ');
                defaultTeacher.querySelector('.teacher-attitude').textContent = teacher.attitude;
                defaultTeacher.dataset.teacherId = teacher.id;
                document.getElementById('teacher-error').style.display = 'none';
            }
        });
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
            if (data.message.includes('deleted successfully')) {
                fetchTeachers();
                // If we deleted the currently displayed teacher, clear the display
                const defaultTeacher = document.getElementById('default-teacher');
                if (defaultTeacher.querySelector('.delete-btn').getAttribute('onclick').includes(teacherId)) {
                    defaultTeacher.style.display = 'none';
                }
            }
        })
        .catch(err => {
            console.error('Error deleting teacher:', err);
        });
}

function generateTest() {
    const defaultTeacher = document.getElementById('default-teacher');
    const teacherId = defaultTeacher.dataset.teacherId;
    const teacherError = document.getElementById('teacher-error');
    
    if (!teacherId || defaultTeacher.style.display === 'none') {
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
        teacher_id: teacherId,
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
