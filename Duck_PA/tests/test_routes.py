import pytest
from Duck_PA import app
from Duck_PA.teachers.teachers import teachers, teacher1, teacher2, teacher3, teacher4
import json
from unittest.mock import patch, MagicMock

# Import routes to ensure they are registered
from Duck_PA.routes import generate_test, submit_test

@pytest.fixture(autouse=True)
def reset_teachers():
    """Reset teachers list before each test"""
    teachers.clear()
    teachers.extend([teacher1, teacher2, teacher3, teacher4])

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

def test_get_teachers(client):
    """Test getting the list of teachers"""
    response = client.get('/get_teachers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'teachers' in data
    assert len(data['teachers']) > 0
    assert all(isinstance(t, dict) for t in data['teachers'])

def test_create_teacher(client):
    """Test creating a new teacher"""
    initial_teacher_count = len(teachers)
    teacher_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'specializations': ['Math', 'Physics'],
        'attitude': 'Friendly'
    }
    response = client.post('/create_teacher', 
                         json=teacher_data,
                         content_type='application/json')
    assert response.status_code == 201
    assert len(teachers) == initial_teacher_count + 1
    assert teachers[-1].name == 'John Doe'

def test_delete_teacher(client):
    """Test deleting a teacher"""
    initial_teacher_count = len(teachers)
    response = client.delete(f'/delete_teacher/{teachers[0].id}')
    assert response.status_code == 200
    assert len(teachers) == initial_teacher_count - 1

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
        'teacher_id': '1',
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