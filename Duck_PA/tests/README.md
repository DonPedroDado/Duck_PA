# Duck PA Tests

This directory contains the test suite for the Duck PA application. The tests cover various aspects of the application including:

- Route testing
- AI integration testing
- Test generation and checking functionality
- Teacher management

## Test Structure

- `test_routes.py`: Tests for all Flask routes and endpoints
- `test_ai.py`: Tests for AI integration and test generation
- `test_check_test.py`: Tests for test checking functionality

## Requirements

To run the tests, you need:

1. Python 3.7+
2. pytest
3. pytest-cov (for coverage reports)

Install the test dependencies:

```bash
pip install pytest pytest-cov
```

## Running Tests

From the root directory of the project, run:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=Duck_PA

# Run specific test file
pytest Duck_PA/tests/test_routes.py

# Run tests with verbose output
pytest -v
```

## Mocking

The tests use Python's `unittest.mock` to mock external dependencies:

- AI service calls are mocked to avoid actual API calls
- Database interactions are mocked where applicable

## Test Data

The tests use predefined test data and fixtures:

- Mock teachers are created for testing
- Sample test questions and answers are provided
- Various test scenarios are covered (correct/incorrect answers, invalid inputs, etc.)

## Adding New Tests

When adding new tests:

1. Follow the existing test structure
2. Use appropriate fixtures and mocks
3. Cover both success and failure cases
4. Add docstrings explaining test purpose
5. Update this README if adding new test categories

## Coverage

Aim to maintain high test coverage. Current coverage targets:

- Routes: 100%
- AI Integration: 90%
- Test Checking: 100%
- Teacher Management: 100% 