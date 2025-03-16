function submitTest(event) {
    event.preventDefault();

    // Gather the data
    let testType = document.getElementById('test-type').value;
    let questions = JSON.parse(document.getElementById('questions-data').value);
    let answers = [];

    // Example of collecting answers
    questions.forEach((question, idx) => {
        let answer;
        if (question.type === "fill_in_the_blank") {
            answer = [];
            let blanks = document.querySelectorAll(`input[name^='q${idx + 1}_blank']`);
            blanks.forEach(blank => {
                answer.push(blank.value);
            });
            answers.push(answer.join(" "));
        } else {
            answer = document.querySelector(`input[name='q${idx + 1}']:checked`);
            if (answer) {
                answers.push(answer.value);
            } else {
                let textAnswer = document.querySelector(`input[name='q${idx + 1}']`);
                if (textAnswer) {
                    answers.push(textAnswer.value);
                }
            }
        }
    });

    let payload = {
        test_type: testType,
        questions: questions,
        answers: answers
    };

    fetch('/submit_test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            if (data.all_correct) {
                alert("All answers are correct!");
            } else {
                let feedbackHtml = `
                <div class="feedback-container">
                    <h2>Feedback</h2>
                    <ul>`;
                data.feedback.forEach(item => {
                    feedbackHtml += `<li><strong>Question:</strong> ${item.question}<br><strong>Your Answer:</strong> ${item.your_answer}<br><strong>Correct Answer:</strong> ${item.correct_answer}<br><strong>Explanation:</strong> ${item.explanation}</li>`;
                });
                feedbackHtml += `</ul><p><strong>Total Score:</strong> ${data.score} out of ${questions.length}</p></div>`;
                document.getElementById('test-form').innerHTML = feedbackHtml;
            }
        })
        .catch(err => {
            console.error('Error submitting test:', err);
        });
} 