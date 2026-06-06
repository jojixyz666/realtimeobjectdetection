import logging
import os
import sys

def setup_logger(log_level="INFO", log_file="logs/app.log"):
    """Set up the application logger."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger("ObjectDetection")
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

def get_logger():
    return logging.getLogger("ObjectDetection")
