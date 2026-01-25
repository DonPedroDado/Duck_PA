function generateTest() {
    // Validate required fields
    const requiredFields = ['test-topic', 'test-type', 'test-difficulty', 'test-questionsnumber', 'test-language'];
    for (const fieldId of requiredFields) {
        const field = document.getElementById(fieldId);
        if (!field.value.trim()) {
            field.focus();
            return;
        }
    }

    const payload = {
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
