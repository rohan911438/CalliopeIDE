import json
import unittest
from flask import Flask, g
import logging
from server.utils.metrics import metrics as metrics_dict, increment as increment_metric
from server.utils import logger
from server.utils.structured_logging import JsonFormatter
from server.middleware.observability import init_observability
import io

class TestModularObservability(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        init_observability(self.app)
        # Reset metrics dictionary
        metrics_dict.update({
            "request_count": 0,
            "error_count": 0,
            "execution_count": 0,
            "slow_requests": 0
        })

    def test_json_logging_modular(self):
        """Test that logs are in JSON format via the new logger wrapper"""
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setFormatter(JsonFormatter())
        logger.base_logger.addHandler(handler)
        
        with self.app.test_request_context('/test-modular', headers={'X-Request-ID': 'modular-123'}):
            g.request_id = 'modular-123'
            g.user_id = 100
            
            logger.log_info("modular test", extra={"key": "value"})
            
            log_output = log_capture.getvalue().strip().split('\n')[-1] # Get last line
            log_json = json.loads(log_output)
            
            self.assertEqual(log_json['message'], "modular test")
            self.assertEqual(log_json['request_id'], "modular-123")
            self.assertEqual(log_json['key'], "value")

    def test_metrics_increment(self):
        """Test specific metrics.increment functionality"""
        increment_metric("execution_count")
        self.assertEqual(metrics_dict["execution_count"], 1)
        
        increment_metric("error_count")
        self.assertEqual(metrics_dict["error_count"], 1)

    def test_slow_request_logging_logic(self):
        """Test slow request logging triggers properly in middleware context"""
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setFormatter(JsonFormatter())
        logger.base_logger.addHandler(handler)
        
        with self.app.test_request_context('/slow'):
            # Manually simulate a slow request logic (usually in after_request)
            duration = 600
            increment_metric("slow_requests")
            logger.log_warning("slow_request", extra={"duration_ms": duration})
            
            log_output = log_capture.getvalue().strip().split('\n')[-1]
            log_json = json.loads(log_output)
            
            self.assertEqual(log_json['message'], "slow_request")
            self.assertEqual(log_json['duration_ms'], 600)
            self.assertEqual(metrics_dict["slow_requests"], 1)

    def test_execution_lifecycle_modular(self):
        """Test the specific log_execution_lifecycle format requested by user"""
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setFormatter(JsonFormatter())
        logger.base_logger.addHandler(handler)
        
        exec_id = "test-exec-789"
        logger.log_execution_lifecycle("execution_started", exec_id)
        
        log_lines = log_capture.getvalue().strip().split('\n')
        start_log = json.loads(log_lines[-1])
        self.assertEqual(start_log['message'], "execution_started")
        self.assertEqual(start_log['execution_id'], exec_id)
        self.assertEqual(metrics_dict["execution_count"], 1)
        
        logger.log_execution_lifecycle("execution_completed", exec_id, extra={"execution_time": 0.5})
        log_lines = log_capture.getvalue().strip().split('\n')
        comp_log = json.loads(log_lines[-1])
        self.assertEqual(comp_log['message'], "execution_completed")
        self.assertEqual(comp_log['execution_time'], 0.5)

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
