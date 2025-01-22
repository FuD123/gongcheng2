import logging
from datetime import datetime

class UserError(Exception):
    """Base class for user-related errors"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(UserError):
    """Raised when a user is not found"""
    def __init__(self, user_id):
        super().__init__('USER_NOT_FOUND', f'User {user_id} not found')

class UserAlreadyExistsError(UserError):
    """Raised when trying to create a user that already exists"""
    def __init__(self, username):
        super().__init__('USER_ALREADY_EXISTS', f'User {username} already exists')

class UserManager:
    def __init__(self):
        self.users = {}
        self.logger = logging.getLogger('user_manager')
        
    def create_user(self, user_data):
        username = user_data.get('username')
        if any(u['username'] == username for u in self.users.values()):
            raise UserAlreadyExistsError(username)
            
        user_id = str(datetime.now().timestamp())
        self.users[user_id] = {
            'id': user_id,
            'username': username,
            'email': user_data.get('email'),
            'created_at': datetime.now(),
            'last_login': None
        }
        return user_id

    def get_user(self, user_id):
        return self.users.get(user_id)

    def update_user(self, user_id, update_data):
        if user_id not in self.users:
            raise UserNotFoundError(user_id)
            
        self.users[user_id].update(update_data)
        return True

    def delete_user(self, user_id):
        if user_id not in self.users:
            raise UserNotFoundError(user_id)
            
        del self.users[user_id]
        return True

    def list_users(self):
        return list(self.users.values())
