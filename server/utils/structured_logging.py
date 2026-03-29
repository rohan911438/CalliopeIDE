"""
JSON structured logging formatter for production observability
"""
import logging
import json
import os
from datetime import datetime
from flask import g, has_request_context

ENABLE_STRUCTURED_LOGGING = os.getenv('ENABLE_STRUCTURED_LOGGING', 'true').lower() == 'true'

class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    def format(self, record):
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Inject tracing information if available in Flask context
        try:
            if has_request_context():
                log_data.update({
                    "request_id": getattr(g, 'request_id', None),
                    "user_id": getattr(g, 'user_id', None),
                    "endpoint": getattr(g, 'endpoint', getattr(g, 'request_path', None)),
                    "execution_id": getattr(g, 'execution_id', None)
                })
        except (RuntimeError, AttributeError):
            pass

        # Add extra fields if provided via 'extra'
        if hasattr(record, 'extra_data') and isinstance(record.extra_data, dict):
            log_data.update(record.extra_data)

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)
