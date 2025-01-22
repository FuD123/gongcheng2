class TaskError(Exception):
    """Base class for task-related errors"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)

class TaskValidationError(TaskError):
    """Raised when task validation fails"""
    def __init__(self, code, message):
        super().__init__(code, message)

class TaskNotFoundError(TaskError):
    """Raised when a task is not found"""
    def __init__(self, task_id):
        super().__init__('TASK_NOT_FOUND', f'Task {task_id} not found')

class TaskAlreadyRunningError(TaskError):
    """Raised when trying to start an already running task"""
    def __init__(self, task_id):
        super().__init__('TASK_ALREADY_RUNNING', f'Task {task_id} is already running')
