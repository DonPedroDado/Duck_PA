function submitTest(event) {
    event.preventDefault();

    // Gather the data
    let testType = document.getElementById('test-type').value;
    let questions = JSON.parse(document.getElementById('questions-data').value);
    let answers = [];

    // Collect answers for all question types, including essay
    questions.forEach((question, idx) => {
        let answer;
        if (question.type === "fill_in_the_blank") {
            answer = [];
            let blanks = document.querySelectorAll(`input[name^='q${idx + 1}_blank']`);
            blanks.forEach(blank => {
                answer.push(blank.value);
            });
            answers.push(answer.join(" "));
        } else if (question.type === "essay") {
            let essayAnswer = document.querySelector(`textarea[name='q${idx + 1}']`);
            if (essayAnswer) {
                answers.push(essayAnswer.value);
            } else {
                answers.push("");
            }
        } else {
            answer = document.querySelector(`input[name='q${idx + 1}']:checked`);
            if (answer) {
                answers.push(answer.value);
            } else {
                let textAnswer = document.querySelector(`input[name='q${idx + 1}']`);
                if (textAnswer) {
                    answers.push(textAnswer.value);
                } else {
                    answers.push("");
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
                let feedbackHtml = `
                <div class="feedback-container">
                    <h2>Feedback</h2>
                    <p style="color: green; font-weight: bold;">🎉 Congratulations! All answers are correct!</p>
                    <p><strong>Total Score:</strong> ${data.score} out of ${questions.length}</p>
                </div>`;
                document.getElementById('test-form').innerHTML = feedbackHtml;
            } else {
                let feedbackHtml = `
                <div class="feedback-container">
                    <h2>Wrong Answers</h2>
                    <ul>`;
                
                // Only show wrong answers
                data.feedback.forEach(item => {
                    if (!item.is_correct) {
                        feedbackHtml += `<li>
                            <strong>Question:</strong> ${item.question || 'N/A'}<br>
                            <strong style="color: #dc2626;">Your Answer:</strong> ${item.your_answer || 'N/A'}<br>`;
                        if (item.correct_answer !== undefined && item.correct_answer !== null) {
                            feedbackHtml += `<strong style="color: #16a34a;">Correct Answer:</strong> ${item.correct_answer}<br>`;
                        }
                        feedbackHtml += `<strong>Explanation:</strong> ${item.explanation || 'N/A'}<br>
                        </li>`;
                    }
                });
                
                feedbackHtml += `</ul><p><strong>Total Score:</strong> ${data.score} out of ${questions.length}</p></div>`;
                document.getElementById('test-form').innerHTML = feedbackHtml;
            }
        })
        .catch(err => {
            console.error('Error submitting test:', err);
            alert('Error submitting test: ' + err.message);
        });
}