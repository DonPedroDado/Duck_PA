from typing import Union
from fastapi import FastAPI
from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel
from typing import List

#app = FastAPI()

first_message={}

def ask_AI(text: str):
    response: ChatResponse = chat(model='llama3.2:latest', messages=[
        {
            "role": "user",
            "content": text,
        },
    ])

    return response["message"]["content"]


#@app.get("/")
def read_root():
    return {"Welcome": "to the AI"}


#@app.get("/create_profile/{name}")
def create_profile(name: str):
    message=f"You are an AI assistant that now will be used to allow students to learn particular topics. You are talking to the student and he is called {name}. Our plan is the following, we will first ask questions to create his profile. You want to assess his degree level, age and other information that is pertinent to students. Once you are done creating the profile, you are going to reply with a full summary of the profile that can be used for next steps. Now ask questions one by one and after each question the student is going to profile the answer. Once you are ready, reply with the message <EOP> the summary of the profile <EOP>. You are going to ask at most 5 questions."

    first_message[name] = message

    return {"text": ask_AI(message)}

class ProfileContinuation(BaseModel):
    name: str
    messages: List[str]


#@app.post("/continue_profile_creation")
def continue_profile_creation(data: ProfileContinuation):
    if data.name not in first_message:
        return {"error": "unknown user"}

    messages=[{
            "role": "user",
            "content": first_message[data.name],
        }]

    for i in data.messages:
        messages.append({
            "role": "user",
            "content": i,
        })

    print(messages)
    response: ChatResponse = chat(model='llama3.2:latest', messages=messages)

    return {"question": response["message"]["content"]}