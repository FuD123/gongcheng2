from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    """任务模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(db.String(20), nullable=False, default='pending')
    priority = db.Column(db.String(20), nullable=False, default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    logs = relationship('Log', back_populates='task')
    
    def __repr__(self):
        return f'<Task {self.name}>'

class Log(db.Model):
    """日志模型"""
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, ForeignKey('task.id'))
    task = relationship('Task', back_populates='logs')
    source_server_name = db.Column(db.String(100))
    source_server_ip = db.Column(db.String(15))
    source_server_file_path = db.Column(db.String(200))
    source_server_file_name = db.Column(db.String(100))
    task_time = db.Column(db.DateTime, default=datetime.utcnow)
    error_message = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<Log {self.task_id}>'
