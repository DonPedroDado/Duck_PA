import pytest
from Duck_PA import app
import json
from unittest.mock import patch, MagicMock

# Import routes to ensure they are registered
from Duck_PA.routes import generate_test, submit_test

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test the homepage route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Duck Practice Assistant' in response.data

@patch('Duck_PA.AI.ask_ai.model.generate_content')
def test_generate_test(mock_generate_content, client):
    """Test generating a test"""
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

    test_data = {
        'topic': 'Mathematics',
        'test_type': 'Multiple Choice Tests',
        'test_difficulty': 'Normal',
        'test_language': 'English',
        'test_questionsnumber': '1'
    }
    
    response = client.post('/generate_test', data=test_data)
    assert response.status_code == 200
    assert b'Mathematics' in response.data

def test_submit_test(client):
    """Test submitting a test"""
    test_data = {
        'test_type': 'Multiple Choice Tests',
        'questions': [
            {
                'question': 'What is 2+2?',
                'type': 'multiple_choice',
                'options': ['3', '4', '5', '6'],
                'correct_answer': '4'
            }
        ],
        'answers': ['4']
    }
    
    response = client.post('/submit_test', 
                         json=test_data,
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'all_correct' in data
    assert 'feedback' in data
    assert 'score' in data

def test_submit_test_invalid_data(client):
    """Test submitting a test with invalid data"""
    response = client.post('/submit_test', 
                         json={},
                         content_type='application/json')
    assert response.status_code == 400
    
def test_submit_test_missing_data(client):
    """Test submitting a test with missing data"""
    test_data = {
        'test_type': 'Multiple Choice Tests'
        # Missing questions and answers
    }
    response = client.post('/submit_test', 
                         json=test_data,
                         content_type='application/json')
    assert response.status_code == 400
