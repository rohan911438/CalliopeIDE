"""
High-level logging wrapper for Calliope IDE
"""
import logging
import os
from typing import Any, Dict, Optional
from server.utils.metrics import metrics as metrics_dict, increment as increment_metric
from server.utils.structured_logging import JsonFormatter, ENABLE_STRUCTURED_LOGGING

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

def get_base_logger():
    """Setup or return the base logger"""
    logger = logging.getLogger("calliope-ide")
    level = getattr(logging, LOG_LEVEL, logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        if ENABLE_STRUCTURED_LOGGING:
            handler.setFormatter(JsonFormatter())
        else:
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
        logger.addHandler(handler)
    
    # Ensure no duplicate handlers from other modules
    logger.propagate = False
    return logger

base_logger = get_base_logger()

def log_info(message: str, extra: Optional[Dict[str, Any]] = None):
    """Log information level message"""
    base_logger.info(message, extra={'extra_data': extra} if extra else None)

def log_error(message: str, error: Optional[Exception] = None, extra: Optional[Dict[str, Any]] = None):
    """Log error level message and increment error count"""
    increment_metric("error_count")
    
    log_extra = extra.copy() if extra else {}
    if error:
        log_extra["error_type"] = type(error).__name__
        log_extra["error_message"] = str(error)
        
    base_logger.error(message, exc_info=bool(error), extra={'extra_data': log_extra})

def log_warning(message: str, extra: Optional[Dict[str, Any]] = None):
    """Log warning level message"""
    base_logger.warning(message, extra={'extra_data': extra} if extra else None)

def log_execution_lifecycle(phase: str, execution_id: str, extra: Optional[Dict[str, Any]] = None):
    """Specialized logging for execution lifecycle"""
    data = {"execution_id": execution_id}
    if extra:
        data.update(extra)
    
    if phase == "execution_started":
        increment_metric("execution_count")
        log_info("execution_started", extra=data)
    elif phase == "execution_completed":
        log_info("execution_completed", extra=data)
    elif phase == "execution_failed":
        log_error(f"execution_failed: {execution_id}", extra=data)
