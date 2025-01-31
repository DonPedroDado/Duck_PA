from typing import Union
from fastapi import FastAPI
from ollama import chat
from ollama import ChatResponse
#import re

app = FastAPI()

def ask_AI(text: str):
    response: ChatResponse = chat(model='llama3.2:latest', messages=[
       # {
        #    "role": "system",
       #     "content": "You are an assistant that helps students with different topics. You must explain the topics in an easy way.",
        #},
        {
            "role": "user",
            "content": text,
        },
    ])
    
    #cleaned_content = re.sub(r"<think>.*?</think>\n?", "",
    #response, flags=re.DOTALL)

    #return cleaned_content
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/first_prompt/{name}")
def first_promt(name: str):
    message=f"You are an AI assistant that now will be used to allow students to learn particular topics. The first thing we are going to do is to create a profile of the student. The name of the student is {name}. In the following you are going to ask question one by one and after each question I'm going to provide the answer. Once you are ready just reply to the last question with the string TYYUIOH."

    return {"name": ask_AI(message)}