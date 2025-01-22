import pytest
from datetime import datetime, timedelta
from src.modules.tasks.task_manager import TaskManager
from src.modules.tasks.exceptions import TaskValidationError, TaskNotFoundError

@pytest.fixture
def task_manager():
    return TaskManager()

def test_create_task(task_manager):
    task = task_manager.create_task(
        title='Test Task',
        description='Test Description',
        due_date=datetime.utcnow() + timedelta(days=1)
    )
    
    assert task.id is not None
    assert task.title == 'Test Task'
    assert task.status == 'pending'

def test_get_task(task_manager):
    created_task = task_manager.create_task(
        title='Test Task',
        description='Test Description'
    )
    
    retrieved_task = task_manager.get_task(created_task.id)
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == 'Test Task'

def test_update_task(task_manager):
    task = task_manager.create_task(
        title='Old Title',
        description='Old Description'
    )
    
    updated_task = task_manager.update_task(task.id, {
        'title': 'New Title',
        'description': 'New Description'
    })
    
    assert updated_task.title == 'New Title'
    assert updated_task.description == 'New Description'

def test_delete_task(task_manager):
    task = task_manager.create_task(
        title='Delete Me',
        description='Test Description'
    )
    
    task_manager.delete_task(task.id)
    
    with pytest.raises(TaskNotFoundError):
        task_manager.get_task(task.id)

def test_list_tasks(task_manager):
    task_manager.create_task(title='Task 1')
    task_manager.create_task(title='Task 2')
    
    tasks = task_manager.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == 'Task 1'
    assert tasks[1].title == 'Task 2'

def test_change_task_status(task_manager):
    task = task_manager.create_task(title='Test Task')
    
    # Test valid status transitions
    task_manager.change_task_status(task.id, 'in_progress')
    assert task_manager.get_task(task.id).status == 'in_progress'
    
    task_manager.change_task_status(task.id, 'completed')
    assert task_manager.get_task(task.id).status == 'completed'

def test_invalid_task_creation(task_manager):
    with pytest.raises(TaskValidationError):
        task_manager.create_task(title='')  # Empty title
        
    with pytest.raises(TaskValidationError):
        task_manager.create_task(
            title='Test',
            due_date=datetime.utcnow() - timedelta(days=1)  # Past due date
        )

def test_invalid_status_transition(task_manager):
    task = task_manager.create_task(title='Test Task')
    
    with pytest.raises(TaskValidationError):
        task_manager.change_task_status(task.id, 'invalid_status')
        
    # Test invalid transition from completed
    task_manager.change_task_status(task.id, 'completed')
    with pytest.raises(TaskValidationError):
        task_manager.change_task_status(task.id, 'in_progress')

def test_task_not_found(task_manager):
    with pytest.raises(TaskNotFoundError):
        task_manager.get_task('non-existent-id')
        
    with pytest.raises(TaskNotFoundError):
        task_manager.update_task('non-existent-id', {'title': 'New Title'})
        
    with pytest.raises(TaskNotFoundError):
        task_manager.delete_task('non-existent-id')
