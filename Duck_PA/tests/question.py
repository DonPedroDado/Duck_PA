from pydantic import BaseModel

class Question(BaseModel):
    question: str
    type: str
    options: list[str]
    correct_answer: str

class QuestionsList(BaseModel):
    questions: list[Question]