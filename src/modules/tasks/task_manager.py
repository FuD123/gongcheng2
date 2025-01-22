from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import logging
import time

class TaskError(Exception):
    """Base class for task-related errors"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)

class TaskNotFoundError(TaskError):
    """Raised when a task is not found"""
    def __init__(self, task_id):
        super().__init__('TASK_NOT_FOUND', f'Task {task_id} not found')

class TaskAlreadyRunningError(TaskError):
    """Raised when trying to start an already running task"""
    def __init__(self, task_id):
        super().__init__('TASK_ALREADY_RUNNING', f'Task {task_id} is already running')

class TaskManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.tasks = {}
        self.logger = logging.getLogger('task_manager')
        
    def create_task(self, title, description=None, due_date=None):
        task_id = str(datetime.now().timestamp())
        self.tasks[task_id] = {
            'id': task_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'status': 'pending',
            'progress': 0,
            'created_at': datetime.now()
        }
        return task_id

    def get_task(self, task_id):
        if task_id not in self.tasks:
            raise TaskNotFoundError(task_id)
        return self.tasks[task_id]

    def start_task(self, task_id):
        if task_id not in self.tasks:
            raise TaskNotFoundError(task_id)
            
        if self.tasks[task_id]['status'] == 'running':
            raise TaskAlreadyRunningError(task_id)
            
        def task_runner():
            try:
                self.tasks[task_id]['status'] = 'running'
                # Simulate task execution
                time.sleep(2)  # Keep task running for 2 seconds
                self.tasks[task_id]['status'] = 'completed'
            except TaskError as e:
                self.tasks[task_id]['status'] = 'failed'
                self.tasks[task_id]['error'] = {
                    'code': e.code,
                    'message': e.message
                }
                self.logger.error(f'Task {task_id} failed: {e.code} - {e.message}')
            except Exception as e:
                self.tasks[task_id]['status'] = 'failed'
                self.tasks[task_id]['error'] = {
                    'code': 'TASK_UNKNOWN_ERROR',
                    'message': str(e)
                }
                self.logger.error(f'Task {task_id} failed with unknown error: {str(e)}')

        self.executor.submit(task_runner)
        return True

    def get_task_status(self, task_id):
        task = self.tasks.get(task_id)
        if task:
            return {
                'title': task['title'],
                'status': task['status']
            }
        return None

    def list_tasks(self):
        return [{
            'title': task['title'],
            'status': task['status']
        } for task in self.tasks.values()]

    def update_task(self, task_id, updates):
        task = self.get_task(task_id)
        task.update(updates)
        return task

    def delete_task(self, task_id):
        if task_id not in self.tasks:
            raise TaskNotFoundError(task_id)
        del self.tasks[task_id]
        return True

    def change_task_status(self, task_id, new_status):
        valid_statuses = ['pending', 'in_progress', 'completed', 'failed']
        if new_status not in valid_statuses:
            raise TaskValidationError('INVALID_STATUS', 
                f'Invalid status: {new_status}. Must be one of {valid_statuses}')
        
        task = self.get_task(task_id)
        task['status'] = new_status
        return task

    def pause_task(self, task_id):
        # Implement pause logic
        pass

    def resume_task(self, task_id):
        # Implement resume logic
        pass

    def cancel_task(self, task_id):
        # Implement cancel logic
        pass
