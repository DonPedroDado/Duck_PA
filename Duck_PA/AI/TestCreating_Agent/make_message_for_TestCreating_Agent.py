from Duck_PA.teachers.classteacher import ClassTeacher

def make_message(topic: str, teacher: ClassTeacher, question_type: str, difficulty: str, language: str, number_of_questions: int):
    personality = (
        f"You must make questions for them. You are teacher called {teacher.name}. "
        f"Your specializations are {', '.join(teacher.specialization)} and your attitude is {teacher.attitude}. "
    )
    message = (
        f"I want you to create a test about the following topic: {topic}. "
        f"The type of the question is {question_type}. "
        f"This is the difficulty for the test: {difficulty}. "
        f"You must make the questions in {language}."
    )

    if question_type == "Multiple Choice Tests":
        message += (
            f" You are going to create a Multiple Choice Test. I want you to create {number_of_questions} questions and for each question provide 4 possible answers: "
            f"one is correct, one is almost correct, the other one is neutral and one is clearly wrong. "
            f"Be sure there is only one right answer."
        )
        message += """ I want you to return the result as a JSON. The schema of the JSON should be the following: "questions": [
                {
                    "question": "Sample Multiple Choice Question 1",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"]
                },
                {
                    "question": "Another question",
                    "type": "multiple_choice",
                    "options": ["Option A", "Option B", "Option C", "Option D"]
                }
            ]"""
        message += f" You are going to reply only with the JSON described above and NOTHING ELSE. The options must be in {language} too."

    elif question_type == "True/False Tests":
        message += (
            f" You are going to create a True/False Test. I want you to create {number_of_questions} questions. Each question should have a sentence and the answer should be either True or False."
        )
        message += """ I want you to return the result as a JSON. The schema of the JSON should be the following: "questions": [
                {
                    "question": "Sample True/False Question 1: The capital of France is Paris.",
                    "type": "true_false"
                },
                {
                    "question": "Another True/False Question: The capital of Italy is Rome.",
                    "type": "true_false"
                }
            ]"""
        message += " You are going to reply only with the JSON described above and NOTHING ELSE."

    elif question_type == "Fill-in-the-Blank Tests":
        message += (
            f" You are going to create a Fill-in-the-Blank Test. I want you to create {number_of_questions} questions. Each question should have a sentence with a blank space."
        )
        message += """ I want you to return the result as a JSON. The schema of the JSON should be the following: "questions": [
                {
                    "question": "Sample Fill-in-the-Blank Question 1: The capital of France is __________.",
                    "type": "fill_in_the_blank"
                },
                {
                    "question": "Another Fill-in-the-Blank Question: The capital of Italy is __________.",
                    "type": "fill_in_the_blank"
                }
            ]"""
        message += " You are going to reply only with the JSON described above and NOTHING ELSE. Make sure the exercises are understandable and specific to the topic."

    elif question_type == "Essay Tests":
        message += (
            f" You are going to create an Essay Test. I want you to create {number_of_questions} essay questions. Each question should require a detailed written answer."
        )
        message += """ I want you to return the result as a JSON. The schema of the JSON should be the following: "questions": [
                {
                    "question": "Sample Essay Question 1: Discuss the impact of climate change on global agriculture.",
                    "type": "essay"
                },
                {
                    "question": "Another Essay Question: Explain the significance of the Renaissance in European history.",
                    "type": "essay"
                }
            ]"""
        message += " You are going to reply only with the JSON described above and NOTHING ELSE. Make sure the questions are open-ended and require thoughtful, detailed responses."

    else:
        print("Invalid question type")
        return []

    print(message)
    return message, personality