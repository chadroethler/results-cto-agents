"""
Utility functions shared across agents
"""

import json
import logging
import os
from typing import Dict, Any
from datetime import datetime


def load_json_config(filepath: str) -> Dict[str, Any]:
    """
    Load JSON configuration file
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Parsed JSON data
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {filepath}: {e}")
        raise


def setup_logging(agent_name: str, level: str = None) -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        agent_name: Name of the agent (for log file)
        level: Logging level (defaults to LOG_LEVEL env var or INFO)
    
    Returns:
        Configured logger
    """
    # Get log level from env or parameter
    log_level = level or os.getenv('LOG_LEVEL', 'INFO')
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # File handler
    file_handler = logging.FileHandler(f'logs/{agent_name}.log')
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Setup logger
    logger = logging.getLogger(agent_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def sanitize_text(text: str, max_length: int = 500) -> str:
    """
    Sanitize and truncate text
    
    Args:
        text: Input text
        max_length: Maximum length
    
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
    
    # Truncate if needed
    if len(text) > max_length:
        text = text[:max_length] + '...'
    
    return text.strip()


def get_timestamp() -> str:
    """
    Get formatted timestamp
    
    Returns:
        Timestamp string in YYYY-MM-DD HH:MM:SS format
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_date() -> str:
    """
    Get formatted date
    
    Returns:
        Date string in YYYY-MM-DD format
    """
    return datetime.now().strftime('%Y-%m-%d')


def is_production() -> bool:
    """
    Check if running in production environment
    
    Returns:
        True if ENVIRONMENT=production
    """
    return os.getenv('ENVIRONMENT', 'development').lower() == 'production'


def send_alert(subject: str, message: str):
    """
    Send alert notification (placeholder for future implementation)
    
    Args:
        subject: Alert subject
        message: Alert message
    """
    # TODO: Implement email/Slack alerts
    logging.warning(f"ALERT: {subject} - {message}")
