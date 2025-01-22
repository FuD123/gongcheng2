import os
import logging
from datetime import datetime

def setup_logger():
    """配置日志记录器"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("system.log"),
            logging.StreamHandler()
        ]
    )

def validate_file_path(file_path):
    """验证文件路径是否存在"""
    return os.path.exists(file_path)

def get_current_timestamp():
    """获取当前时间戳"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
