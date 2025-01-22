from flask import Blueprint, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy.exc import IntegrityError
from .models import Task, Log, db
import logging

# Swagger UI configuration
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

bp = Blueprint('api', __name__, url_prefix='/api/v1')

@bp.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Welcome to File Operations API'
    })

def init_routes(app):
    """Initialize routes and register blueprints"""
    # Register Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "File Operations API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        tasks = db.session.query(Task).all()
        return jsonify([{
            'id': task.id,
            'name': task.name,
            'status': task.status,
            'priority': task.priority,
            'created_at': task.created_at.isoformat()
        } for task in tasks]), 200
    except Exception as e:
        logging.error(f"Get tasks error: {e}")
        return jsonify({'message': 'Failed to get tasks'}), 500

@bp.route('/tasks', methods=['POST'])
def create_task():
    """Create new task"""
    if not request.is_json:
        return jsonify({'message': 'Request must be JSON'}), 400
        
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    if not name:
        return jsonify({'message': 'Task name is required'}), 400
        
    try:
        new_task = Task(
            name=name,
            description=description
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'}), 201
    except Exception as e:
        logging.error(f"Create task error: {e}")
        db.session.rollback()
        return jsonify({'message': 'Failed to create task'}), 500

@bp.route('/logs', methods=['GET'])
def get_logs():
    """Get all logs"""
    try:
        logs = db.session.query(Log).order_by(Log.task_time.desc()).limit(100).all()
        
        return jsonify([{
            'id': log.id,
            'task_id': log.task_id,
            'task_name': log.task.name,
            'source_server_name': log.source_server_name,
            'task_time': log.task_time.isoformat(),
            'error_message': log.error_message
        } for log in logs]), 200
    except Exception as e:
        logging.error(f"Get logs error: {e}")
        return jsonify({'message': 'Failed to get logs'}), 500

@bp.route('/dashboard/charts', methods=['GET'])
def get_dashboard_charts():
    """Get dashboard charts data"""
    try:
        # Example chart data
        return jsonify({
            'lineChart': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'datasets': [{
                    'label': 'Tasks Completed',
                    'data': [12, 19, 3, 5, 2, 3],
                    'borderColor': '#36a2eb',
                    'fill': False
                }]
            },
            'pieChart': {
                'labels': ['Pending', 'In Progress', 'Completed'],
                'datasets': [{
                    'data': [12, 19, 3],
                    'backgroundColor': ['#ff6384', '#36a2eb', '#cc65fe']
                }]
            },
            'barChart': {
                'labels': ['High', 'Medium', 'Low'],
                'datasets': [{
                    'label': 'Task Priority',
                    'data': [5, 10, 15],
                    'backgroundColor': ['#ff6384', '#36a2eb', '#cc65fe']
                }]
            }
        }), 200
    except Exception as e:
        logging.error(f"Get dashboard charts error: {e}")
        return jsonify({'message': 'Failed to get dashboard charts'}), 500
