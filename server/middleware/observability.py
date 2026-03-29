import time
import uuid
from flask import request, g
from server.utils.metrics import metrics as metrics_dict, increment as increment_metric
from server.utils import logger

def init_observability(app):
    """Register observability hooks with the Flask app"""
    
    @app.before_request
    def start_timer():
        g.start_time = time.time()
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        g.endpoint = request.path
        g.user_id = None
        
        increment_metric("request_count")

    @app.after_request
    def log_request(response):
        if not hasattr(g, 'start_time'):
            return response
            
        duration = (time.time() - g.start_time) * 1000  # ms
        status_code = response.status_code
        
        log_data = {
            "method": request.method,
            "path": request.path,
            "status": status_code,
            "duration_ms": round(duration, 2),
            "ip": request.remote_addr
        }
        
        # Log slow requests (>500ms) - Match user's specific requirement
        if duration > 500:
            increment_metric("slow_requests")
            logger.log_warning("slow_request", extra={"duration_ms": round(duration, 2), "path": request.path})
        
        # Standard request log
        logger.log_info(f"Request: {request.method} {request.path} {status_code}", extra=log_data)
        
        # Add request_id to response headers
        response.headers['X-Request-ID'] = g.request_id
        
        return response

    @app.teardown_request
    def handle_teardown(exception):
        if exception:
            logger.log_error(f"Request teardown exception: {str(exception)}", error=exception)
