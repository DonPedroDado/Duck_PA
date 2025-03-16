import pytest
from Duck_PA.tests.check_test import check_Test

def test_check_multiple_choice_test_all_correct():
    """Test checking a multiple choice test with all correct answers"""
    questions = [
        {
            "question": "What is 2+2?",
            "type": "multiple_choice",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4"
        }
    ]
    answers = ["4"]
    
    all_correct, feedback, score = check_Test("Multiple Choice Tests", questions, answers)
    
    assert all_correct == True
    assert len(feedback) == 0
    assert score == 1

def test_check_multiple_choice_test_incorrect():
    """Test checking a multiple choice test with incorrect answers"""
    questions = [
        {
            "question": "What is 2+2?",
            "type": "multiple_choice",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4"
        }
    ]
    answers = ["5"]
    
    all_correct, feedback, score = check_Test("Multiple Choice Tests", questions, answers)
    
    assert all_correct == False
    assert len(feedback) == 1
    assert score == 0
    assert feedback[0]["correct_answer"] == "4"
    assert feedback[0]["your_answer"] == "5"

def test_check_true_false_test_all_correct():
    """Test checking a true/false test with all correct answers"""
    questions = [
        {
            "question": "2+2 equals 4.",
            "type": "true_false",
            "correct_answer": "True"
        }
    ]
    answers = ["True"]
    
    all_correct, feedback, score = check_Test("True/False Tests", questions, answers)
    
    assert all_correct == True
    assert len(feedback) == 0
    assert score == 1

def test_check_true_false_test_incorrect():
    """Test checking a true/false test with incorrect answers"""
    questions = [
        {
            "question": "2+2 equals 4.",
            "type": "true_false",
            "correct_answer": "True"
        }
    ]
    answers = ["False"]
    
    all_correct, feedback, score = check_Test("True/False Tests", questions, answers)
    
    assert all_correct == False
    assert len(feedback) == 1
    assert score == 0
    assert feedback[0]["correct_answer"] == "True"
    assert feedback[0]["your_answer"] == "False"

def test_check_fill_in_blank_test_all_correct():
    """Test checking a fill in the blank test with all correct answers"""
    questions = [
        {
            "question": "2 plus 2 equals __________.",
            "type": "fill_in_the_blank",
            "correct_answer": "4"
        }
    ]
    answers = ["4"]
    
    all_correct, feedback, score = check_Test("Fill-in-the-Blank Tests", questions, answers)
    
    assert all_correct == True
    assert len(feedback) == 0
    assert score == 1

def test_check_fill_in_blank_test_incorrect():
    """Test checking a fill in the blank test with incorrect answers"""
    questions = [
        {
            "question": "2 plus 2 equals __________.",
            "type": "fill_in_the_blank",
            "correct_answer": "4"
        }
    ]
    answers = ["5"]
    
    all_correct, feedback, score = check_Test("Fill-in-the-Blank Tests", questions, answers)
    
    assert all_correct == False
    assert len(feedback) == 1
    assert score == 0
    assert feedback[0]["correct_answer"] == "4"
    assert feedback[0]["your_answer"] == "5"

def test_check_test_multiple_questions():
    """Test checking a test with multiple questions"""
    questions = [
        {
            "question": "What is 2+2?",
            "type": "multiple_choice",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4"
        },
        {
            "question": "2+2 equals 4.",
            "type": "true_false",
            "correct_answer": "True"
        }
    ]
    answers = ["4", "True"]
    
    all_correct, feedback, score = check_Test("Multiple Choice Tests", questions, answers)
    
    assert all_correct == True
    assert len(feedback) == 0
    assert score == 2

def test_check_test_invalid_type():
    """Test checking a test with invalid type"""
    questions = [
        {
            "question": "What is 2+2?",
            "type": "invalid_type",
            "correct_answer": "4"
        }
    ]
    answers = ["4"]
    
    all_correct, feedback, score = check_Test("Invalid Test Type", questions, answers)
    
    assert all_correct == False
    assert score == 0

def test_check_test_missing_answers():
    """Test checking a test with missing answers"""
    questions = [
        {
            "question": "What is 2+2?",
            "type": "multiple_choice",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4"
        }
    ]
    answers = []
    
    all_correct, feedback, score = check_Test("Multiple Choice Tests", questions, answers)
    
    assert all_correct == False
    assert score == 0 