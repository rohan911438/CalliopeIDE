"""
Monitoring utilities - bridge to modular observability system
"""
import logging
from typing import Any, Dict, Optional
from flask import Flask
from server.utils import metrics, logger

def setup_logging(name: str):
    """Setup logging via unified base logger"""
    # We return the unified logger but ensure it's named for the module if requested
    # However, logger.py already provides a 'calliope-ide' logger
    return logger.base_logger

def init_sentry(app: Flask):
    """Stub - Sentry integration removed"""
    pass

def log_info(message: str, extra: Optional[Dict[str, Any]] = None):
    logger.log_info(message, extra)

def log_error(message: str, error: Optional[Exception] = None, extra: Optional[Dict[str, Any]] = None):
    logger.log_error(message, error, extra)

def log_execution(phase: str, execution_id: str, status: Optional[str] = None, 
                 duration_ms: Optional[float] = None, extra: Optional[Dict[str, Any]] = None):
    """Bridge to log_execution_lifecycle plus extra data for backward compatibility"""
    data = extra.copy() if extra else {}
    if status: data["status"] = status
    if duration_ms: data["execution_time"] = duration_ms
    
    logger.log_execution_lifecycle(phase, execution_id, data)

def get_monitoring_stats() -> Dict[str, Any]:
    """Return real-time observability metrics from metrics.py"""
    return {
        'enabled': True,
        'metrics': metrics.get_metrics_stats(),
        'config': {
            'level': logger.LOG_LEVEL,
            'structured': True # Defaulting to True for now
        }
    }

def track_error(error: Exception, context: Optional[Dict[str, Any]] = None):
    logger.log_error("Captured exception", error=error, extra=context)

def capture_exception(error: Exception, context: Optional[Dict[str, Any]] = None):
    track_error(error, context)

def init_sentry(app: Flask):
    """Stub - Sentry integration removed"""
    pass

def monitor_endpoint(func):
    """Wrapper to monitor endpoint (usually handled by middleware)"""
    return func

def get_monitoring_stats() -> Dict[str, Any]:
    """Return real-time observability metrics"""
    return {
        'enabled': True,
        'metrics': obs_manager.get_stats(),
        'config': {
            'level': LOG_LEVEL,
            'structured': ENABLE_STRUCTURED_LOGGING
        }
    }

def track_error(error: Exception, context: Optional[Dict[str, Any]] = None):
    """Log errors with context"""
    log_error("Captured exception", error=error, extra=context)

def capture_exception(error: Exception, context: Optional[Dict[str, Any]] = None):
    """Alias for track_error for backward compatibility"""
    track_error(error, context)
