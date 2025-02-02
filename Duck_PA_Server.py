from typing import Union
from fastapi import FastAPI
import google.generativeai as genai
from pydantic import BaseModel
from typing import List
import os

class ClassTeacher:
    def __init__(self, id,  name, specialization, attitude):
        self.id = id
        self.name = name
        self.specialization = specialization
        self.attitude = attitude

app = FastAPI()

auth_token = os.getenv("GEMINI_AUTH_TOKEN")  # Get the authentication token from an environment variable
genai.configure(api_key=auth_token)
model = genai.GenerativeModel("gemini-1.5-flash")

class_teacher1 = ClassTeacher(1, "William Thompson", ["Mathematics", "Geometry"], "Calm")
class_teacher2 = ClassTeacher(2, "Rachel Green", ["Physics", "Chemistry"], "Strict")
class_teacher3 = ClassTeacher(3, "Albert Taylor", ["Biology", "Geology"], "Friendly")

class_teachers = [class_teacher1, class_teacher2, class_teacher3]

@app.get("/get_teachers")
def get_teachers():
    return {"teachers": class_teachers}

@app.post("/generate_topic")
def generate_topic(text: str):
    #here you need to write the code to start to ask in an iterative 
    #way details about the topics that the student want to study 
    return {"text": "blabla"}

@app.post("/generate_test")
def generate_test(text: str):
    #here you need to write the code to start to ask in an iterative 
    #way details about the topics that the student want to study 
    return {"text": "blabla"}

@app.get("/")
def read_root():
    return {"Welcome": "to the AI"}
