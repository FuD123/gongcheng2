import pytest
import tempfile
from app import create_app
from app.models import db
from datetime import datetime, timedelta
import os

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure the app with testing settings
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False
    })

    # Create all database tables
    with app.app_context():
        db.create_all()

    yield app

    # Clean up after testing
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

def test_index(client):
    """Test the index page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_protected_route_unauthenticated(client):
    """Test accessing protected route without authentication"""
    response = client.get('/protected')
    assert response.status_code == 401

def test_protected_route_authenticated(client):
    """Test accessing protected route with authentication"""
    # First login
    login_response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert login_response.status_code == 200
    
    # Then access protected route
    response = client.get('/protected')
    assert response.status_code == 200

def test_create_task(client):
    """Test creating a new task"""
    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'Test Description',
        'due_date': (datetime.utcnow() + timedelta(days=1)).isoformat()
    })
    assert response.status_code == 201
    assert 'id' in response.json

def test_get_tasks(client):
    """Test getting all tasks"""
    # First create a task
    client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'Test Description'
    })
    
    # Then get all tasks
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_single_task(client):
    """Test getting a single task"""
    # First create a task
    create_response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'Test Description'
    })
    task_id = create_response.json['id']
    
    # Then get the task
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['title'] == 'Test Task'

def test_update_task(client):
    """Test updating a task"""
    # First create a task
    create_response = client.post('/tasks', json={
        'title': 'Old Title',
        'description': 'Old Description'
    })
    task_id = create_response.json['id']
    
    # Then update the task
    response = client.put(f'/tasks/{task_id}', json={
        'title': 'New Title',
        'description': 'New Description'
    })
    assert response.status_code == 200
    assert response.json['title'] == 'New Title'

def test_delete_task(client):
    """Test deleting a task"""
    # First create a task
    create_response = client.post('/tasks', json={
        'title': 'Delete Me',
        'description': 'Test Description'
    })
    task_id = create_response.json['id']
    
    # Then delete the task
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204
    
    # Verify task is deleted
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404

def test_invalid_task_operations(client):
    """Test invalid task operations"""
    # Test creating task with invalid data
    response = client.post('/tasks', json={})
    assert response.status_code == 400

def test_unauthorized_task_access(client):
    """Test unauthorized access to tasks"""
    # Create a task
    create_response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'Test Description'
    })
    task_id = create_response.json['id']
    
    # Clear authentication
    client.delete('/logout')
    
    # Try to access the task
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 401
