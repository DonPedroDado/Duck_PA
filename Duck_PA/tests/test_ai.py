import pytest
from unittest.mock import patch, MagicMock
from Duck_PA.AI.ask_ai_for_test import ask_AI_for_test
from Duck_PA.teachers.classteacher import ClassTeacher
import json

@pytest.fixture
def mock_teacher():
    return ClassTeacher(1, "Test Teacher", ["Math"], "Friendly")

@patch('Duck_PA.AI.ask_ai.model.generate_content')
def test_ask_ai_for_multiple_choice_test(mock_generate_content, mock_teacher):
    """Test generating a multiple choice test"""
    # Mock AI response
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "questions": [
            {
                "question": "What is 2+2?",
                "type": "multiple_choice",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4"
            }
        ]
    })
    mock_generate_content.return_value = mock_response

    result = ask_AI_for_test(
        teacher=mock_teacher,
        topic="Mathematics",
        test_type="Multiple Choice Tests",
        difficulty="Normal",
        language="English",
        number_of_questions=1
    )

    assert result["title"] == "Multiple Choice Tests on Mathematics"
    assert isinstance(result["questions"], list)
    assert len(result["questions"]) == 1
    assert result["questions"][0]["type"] == "multiple_choice"

@patch('Duck_PA.AI.ask_ai.model.generate_content')
def test_ask_ai_for_true_false_test(mock_generate_content, mock_teacher):
    """Test generating a true/false test"""
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "questions": [
            {
                "question": "2+2 equals 4.",
                "type": "true_false"
            }
        ]
    })
    mock_generate_content.return_value = mock_response

    result = ask_AI_for_test(
        teacher=mock_teacher,
        topic="Mathematics",
        test_type="True/False Tests",
        difficulty="Normal",
        language="English",
        number_of_questions=1
    )

    assert result["title"] == "True/False Tests on Mathematics"
    assert isinstance(result["questions"], list)
    assert len(result["questions"]) == 1
    assert result["questions"][0]["type"] == "true_false"

@patch('Duck_PA.AI.ask_ai.model.generate_content')
def test_ask_ai_for_fill_in_blank_test(mock_generate_content, mock_teacher):
    """Test generating a fill in the blank test"""
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "questions": [
            {
                "question": "2 plus 2 equals __________.",
                "type": "fill_in_the_blank"
            }
        ]
    })
    mock_generate_content.return_value = mock_response

    result = ask_AI_for_test(
        teacher=mock_teacher,
        topic="Mathematics",
        test_type="Fill-in-the-Blank Tests",
        difficulty="Normal",
        language="English",
        number_of_questions=1
    )

    assert result["title"] == "Fill-in-the-Blank Tests on Mathematics"
    assert isinstance(result["questions"], list)
    assert len(result["questions"]) == 1
    assert result["questions"][0]["type"] == "fill_in_the_blank"
    assert "__________" in result["questions"][0]["question"]

@patch('Duck_PA.AI.ask_ai.model.generate_content')
def test_ask_ai_invalid_test_type(mock_generate_content, mock_teacher):
    """Test handling of invalid test type"""
    result = ask_AI_for_test(
        teacher=mock_teacher,
        topic="Mathematics",
        test_type="Invalid Test Type",
        difficulty="Normal",
        language="English",
        number_of_questions=1
    )

    assert result["title"] == "Unknown Test Type on Mathematics"
    assert result["questions"] == []

@patch('Duck_PA.AI.ask_ai.model.generate_content')
def test_ask_ai_error_handling(mock_generate_content, mock_teacher):
    """Test error handling in AI response"""
    # Simulate an error in AI response
    mock_response = MagicMock()
    mock_response.text = "Invalid JSON"
    mock_generate_content.return_value = mock_response

    result = ask_AI_for_test(
        teacher=mock_teacher,
        topic="Mathematics",
        test_type="Multiple Choice Tests",
        difficulty="Normal",
        language="English",
        number_of_questions=1
    )

    assert result["questions"] == [] 