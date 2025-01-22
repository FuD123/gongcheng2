import logging
from datetime import datetime
import json
from typing import List, Dict, Callable
import threading

class NotificationHandler:
    """Base class for notification handlers"""
    def send(self, message: str):
        raise NotImplementedError()

class EmailNotificationHandler(NotificationHandler):
    """Email notification handler"""
    def __init__(self, email: str):
        self.email = email
        
    def send(self, message: str):
        # Implement email sending logic
        print(f"Sending email to {self.email}: {message}")

class LogError(Exception):
    """Base class for log-related errors"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)

class LogNotFoundError(LogError):
    """Raised when trying to access non-existent logs"""
    def __init__(self, log_id):
        super().__init__('LOG_NOT_FOUND', f'Log {log_id} not found')

class LogManager:
    def __init__(self):
        self.logger = logging.getLogger('log_manager')
        self.logs = []
        self.notification_handlers: List[NotificationHandler] = []
        self.monitoring_thread = None
        self.monitoring_active = False
        self.error_threshold = 5  # Number of errors before notification
        self.error_window = 60  # Seconds to track errors
        
    def add_notification_handler(self, handler: NotificationHandler):
        """Add a notification handler"""
        self.notification_handlers.append(handler)
        
    def start_monitoring(self):
        """Start real-time log monitoring"""
        if self.monitoring_thread is not None:
            return
            
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_logs)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
    def stop_monitoring(self):
        """Stop real-time log monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
            self.monitoring_thread = None
            
    def _monitor_logs(self):
        """Internal method for monitoring logs"""
        error_count = 0
        last_error_time = datetime.now()
        
        while self.monitoring_active:
            recent_errors = [
                log for log in self.logs
                if log['event_type'] == 'error' and 
                (datetime.now() - datetime.fromisoformat(log['timestamp'])).total_seconds() < self.error_window
            ]
            
            if len(recent_errors) >= self.error_threshold:
                if error_count < self.error_threshold:
                    self._notify_admins(
                        f"High error rate detected: {len(recent_errors)} errors in last {self.error_window} seconds"
                    )
                error_count = len(recent_errors)
            else:
                error_count = 0
                
            threading.Event().wait(10)  # Check every 10 seconds
            
    def _notify_admins(self, message: str):
        """Notify all registered notification handlers"""
        for handler in self.notification_handlers:
            try:
                handler.send(message)
            except Exception as e:
                self.logger.error(f"Failed to send notification: {str(e)}")
        
    def log_event(self, event_type, message, metadata=None):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'message': message,
            'metadata': metadata or {}
        }
        self.logs.append(log_entry)
        self.logger.info(json.dumps(log_entry))
        
        # Check if this is an error and notify if needed
        if event_type == 'error' and self.monitoring_active:
            self._notify_admins(f"Error logged: {message}")
            
        return True

    def get_logs(self, filter_params=None):
        if not filter_params:
            return self.logs
            
        try:
            filtered_logs = [log for log in self.logs 
                          if all(log.get(k) == v for k, v in filter_params.items())]
            if not filtered_logs:
                raise LogNotFoundError('filtered')
            return filtered_logs
        except Exception as e:
            self.logger.error(f'Error filtering logs: {str(e)}')
            raise LogError('LOG_FILTER_ERROR', f'Error filtering logs: {str(e)}')

    def clear_logs(self):
        self.logs = []
        return True
