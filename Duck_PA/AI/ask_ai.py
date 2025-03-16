from Duck_PA.AI.genai import model
from Duck_PA.teachers.classteacher import ClassTeacher
import json

def ask_AI(topic: str, teacher: ClassTeacher, question_type: str, difficulty: str, language: str, number_of_questions: int):
    # model is already initialized globally
    message = (
        f"You must make questions for them. You are teacher called {teacher.name}. "
        f"Your specializations are {', '.join(teacher.specialization)} and your attitude is {teacher.attitude}. "
        f"I want you to create a test about the following topic: {topic}. "
        f"The type of the question is {question_type}."
        f"This is the difficulty for the test: {difficulty}."
        f"You must make the questions in {language}."
    )
    if question_type == "Multiple Choice Tests":
        message += f"You are going to create a Multiple Choice Test. I want you to create {number_of_questions} questions and for each question to provide 4 possible answers. One is correct, one is almost correct, the other one is neutral and one is clearly wrong. Be sure that there is only one right answer."
        message += """I want you to return the result as a JSON. The schema of the JSON should be the following: questions": [
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
        message += "You are going to reply only if the JSON described above and NOTHING ELSE. Make sure that there is a right answer and that the questions only have one right answer."
        message += f"The options must be in {language} too"

    elif question_type == "True/False Tests":
        message += f"You are going to create a True/False Test. I want you to create {number_of_questions} questions. Each question should have a sentence and the answer should be either True or False. I want you to return the result as a JSON. The schema of the JSON should be the following:"
        message += """questions": [
                {
                    "question": "Sample True/False Question 1: The capital of France is Paris.",
                    "type": "true_false"
                },
                {
                    "question": "Another True/False Question: The capital of Italy is Rome.",
                    "type": "true_false"
                }
            ]"""
        message += "You are going to reply only if the JSON described above and NOTHING ELSE"

    elif question_type == "Fill-in-the-Blank Tests":
        message += f"You are going to create a Fill-in-the-Blank Test. I want you to create {number_of_questions} questions. Each question should have a sentence with a blank space. I want you to return the result as a JSON. The schema of the JSON should be the following:"
        message += """questions": [
                {
                    "question": "Sample Fill-in-the-Blank Question 1: The capital of France is __________.",
                    "type": "fill_in_the_blank"
                },
                {
                    "question": "Another Fill-in-the-Blank Question: The capital of Italy is __________.",
                    "type": "fill_in_the_blank"
                }
            ]"""
        message += "You are going to reply only if the JSON described above and NOTHING ELSE. Make sure that the excercises yoou maked are understandable and make sure that the excercises you make are specific for the topic. If the topic is something connected to grammar(like tenses, for example:past participle, simple part, and so on) make sure you put the infinitive form in brackets. Make sure to put a blank space in the place where the answer should be."   
    else:
        print("invalid question type")


    print(message)

    response = model.generate_content(message,
                                      generation_config={
                                          'response_mime_type': 'application/json',
                                      },)

    message2=(
        f"This is the input I gave you before: {message}"
        f"This is the output you gave me: {response}"
        f"Check the output and fix the json. Like the questions and the explanations and so on."
    )    

    response2 = model.generate_content(message,
                                    generation_config={
                                        'response_mime_type': 'application/json',
                                    },)



    try:
        my_questions = response2.text
        my_questions_json = json.loads(my_questions).get("questions")
        return my_questions_json
    except Exception as e:
        return None