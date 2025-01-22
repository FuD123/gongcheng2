import json
import os
import logging
from typing import Dict, Optional
from pydantic import BaseModel, validator, Field

class SettingsError(Exception):
    """Base class for settings errors"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)

class SMTPConfig(BaseModel):
    """SMTP configuration model"""
    host: str = Field(default="smtp.example.com")
    port: int = Field(default=587)
    username: str = Field(default="")
    password: str = Field(default="")
    use_tls: bool = Field(default=True)
    from_email: str = Field(default="noreply@example.com")

    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v

class WebConfig(BaseModel):
    """Web server configuration model"""
    port: int = Field(default=8000)
    host: str = Field(default="0.0.0.0")
    debug: bool = Field(default=False)

    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v

class SettingsManager:
    def __init__(self):
        self.logger = logging.getLogger('settings_manager')
        self.config_file = 'config/settings.json'
        self.smtp_config = SMTPConfig()
        self.web_config = WebConfig()
        self._load_settings()

    def _load_settings(self):
        """Load settings from config file"""
        try:
            os.makedirs('config', exist_ok=True)
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.smtp_config = SMTPConfig(**data.get('smtp', {}))
                    self.web_config = WebConfig(**data.get('web', {}))
        except Exception as e:
            self.logger.error(f"Failed to load settings: {str(e)}")
            raise SettingsError('LOAD_FAILED', f'Failed to load settings: {str(e)}')

    def _save_settings(self):
        """Save settings to config file"""
        try:
            data = {
                'smtp': self.smtp_config.dict(),
                'web': self.web_config.dict()
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save settings: {str(e)}")
            raise SettingsError('SAVE_FAILED', f'Failed to save settings: {str(e)}')

    def update_smtp_settings(self, settings: Dict) -> bool:
        """Update SMTP settings"""
        try:
            self.smtp_config = SMTPConfig(**settings)
            self._save_settings()
            return True
        except Exception as e:
            self.logger.error(f"Failed to update SMTP settings: {str(e)}")
            raise SettingsError('UPDATE_FAILED', f'Failed to update SMTP settings: {str(e)}')

    def update_web_settings(self, settings: Dict) -> bool:
        """Update web server settings"""
        try:
            self.web_config = WebConfig(**settings)
            self._save_settings()
            return True
        except Exception as e:
            self.logger.error(f"Failed to update web settings: {str(e)}")
            raise SettingsError('UPDATE_FAILED', f'Failed to update web settings: {str(e)}')

    def get_smtp_settings(self) -> Dict:
        """Get current SMTP settings"""
        return self.smtp_config.dict()

    def get_web_settings(self) -> Dict:
        """Get current web server settings"""
        return self.web_config.dict()

    def validate_settings(self) -> bool:
        """Validate all settings"""
        try:
            self.smtp_config.validate()
            self.web_config.validate()
            return True
        except Exception as e:
            self.logger.error(f"Settings validation failed: {str(e)}")
            raise SettingsError('VALIDATION_FAILED', f'Settings validation failed: {str(e)}')
