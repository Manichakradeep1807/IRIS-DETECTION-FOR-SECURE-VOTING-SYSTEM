"""
Performance Monitoring System for Iris Recognition
Tracks system performance, accuracy, and resource usage
"""

import time
import psutil
import numpy as np
import json
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading
import matplotlib.pyplot as plt
import seaborn as sns
from functools import wraps
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('iris_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """
    Comprehensive performance monitoring system
    """
    
    def __init__(self, db_path='performance.db', max_history=1000):
        self.db_path = db_path
        self.max_history = max_history
        
        # In-memory metrics storage
        self.metrics = defaultdict(deque)
        self.real_time_metrics = {}
        
        # Initialize database
        self.init_database()
        
        # Start background monitoring
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._background_monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        logger.info("Performance monitoring system initialized")
    
    def init_database(self):
        """Initialize SQLite database for metrics storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                additional_data TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recognition_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                person_id INTEGER,
                confidence REAL,
                processing_time REAL,
                success BOOLEAN,
                error_message TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_health (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cpu_usage REAL,
                memory_usage REAL,
                gpu_usage REAL,
                temperature REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def measure_time(self, func_name=None):
        """Decorator to measure function execution time"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    success = True
                    error_msg = None
                except Exception as e:
                    result = None
                    success = False
                    error_msg = str(e)
                    logger.error("Error in {}: {e}".format(func.__name__))
                    raise
                finally:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    metric_name = func_name or func.__name__
                    self.log_metric("{}_execution_time".format(metric_name), execution_time)
                    self.log_metric("{}_success_rate".format(metric_name), 1 if success else 0)
                    
                    # Log to database
                    if metric_name == "recognition":
                        self.log_recognition(
                            person_id=kwargs.get('person_id', -1),
                            confidence=kwargs.get('confidence', 0.0),
                            processing_time=execution_time,
                            success=success,
                            error_message=error_msg
                        )
                
                return result
            return wrapper
        return decorator
    
    def log_metric(self, metric_name, value, additional_data=None):
        """Log a metric value"""
        # Store in memory
        self.metrics[metric_name].append({
            'timestamp': datetime.now(),
            'value': value,
            'additional_data': additional_data
        })
        
        # Limit memory usage
        if len(self.metrics[metric_name]) > self.max_history:
            self.metrics[metric_name].popleft()
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO performance_metrics (metric_name, metric_value, additional_data)
            VALUES (?, ?, ?)
        ''', (metric_name, value, json.dumps(additional_data) if additional_data else None))
        conn.commit()
        conn.close()
        
        # Update real-time metrics
        self.real_time_metrics[metric_name] = value
    
    def log_recognition(self, person_id, confidence, processing_time, success, error_message=None):
        """Log recognition attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recognition_logs 
            (person_id, confidence, processing_time, success, error_message)
            VALUES (?, ?, ?, ?, ?)
        ''', (person_id, confidence, processing_time, success, error_message))
        conn.commit()
        conn.close()
    
    def _background_monitor(self):
        """Background thread for system monitoring"""
        while self.monitoring:
            try:
                # System metrics
                cpu_usage = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                memory_usage = memory.percent
                
                # GPU metrics (if available)
                gpu_usage = self._get_gpu_usage()
                temperature = self._get_cpu_temperature()
                
                # Log system health
                self.log_metric('cpu_usage', cpu_usage)
                self.log_metric('memory_usage', memory_usage)
                self.log_metric('gpu_usage', gpu_usage)
                
                # Store in system health table
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO system_health (cpu_usage, memory_usage, gpu_usage, temperature)
                    VALUES (?, ?, ?, ?)
                ''', (cpu_usage, memory_usage, gpu_usage, temperature))
                conn.commit()
                conn.close()
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                logger.error("Error in background monitoring: {}".format(e))
                time.sleep(10)
    
    def _get_gpu_usage(self):
        """Get GPU usage if available"""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].load * 100
        except ImportError:
            pass
        return 0.0
    
    def _get_cpu_temperature(self):
        """Get CPU temperature if available"""
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                return temps['coretemp'][0].current
        except (AttributeError, KeyError):
            pass
        return 0.0
    
    def get_metric_stats(self, metric_name, hours=24):
        """Get statistics for a specific metric"""
        if metric_name not in self.metrics:
            return None
        
        # Filter by time
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_data = [
            item for item in self.metrics[metric_name]
            if item['timestamp'] > cutoff_time
        ]
        
        if not recent_data:
            return None
        
        values = [item['value'] for item in recent_data]
        
        return {
            'count': len(values),
            'mean': np.mean(values),
            'median': np.median(values),
            'std': np.std(values),
            'min': np.min(values),
            'max': np.max(values),
            'latest': values[-1] if values else None
        }
    
    def get_system_health(self):
        """Get current system health status"""
        return {
            'cpu_usage': self.real_time_metrics.get('cpu_usage', 0),
            'memory_usage': self.real_time_metrics.get('memory_usage', 0),
            'gpu_usage': self.real_time_metrics.get('gpu_usage', 0),
            'recognition_success_rate': self.calculate_success_rate(),
            'average_processing_time': self.get_average_processing_time(),
            'status': self.get_health_status()
        }
    
    def calculate_success_rate(self, hours=24):
        """Calculate recognition success rate"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cursor.execute('''
            SELECT success FROM recognition_logs 
            WHERE timestamp > ?
        ''', (cutoff_time,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return 100.0
        
        success_count = sum(1 for (success,) in results if success)
        return (success_count / len(results)) * 100
    
    def get_average_processing_time(self, hours=24):
        """Get average processing time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cursor.execute('''
            SELECT AVG(processing_time) FROM recognition_logs 
            WHERE timestamp > ? AND success = 1
        ''', (cutoff_time,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 0.0
    
    def get_health_status(self):
        """Determine overall system health status"""
        cpu = self.real_time_metrics.get('cpu_usage', 0)
        memory = self.real_time_metrics.get('memory_usage', 0)
        success_rate = self.calculate_success_rate()
        
        if cpu > 90 or memory > 90 or success_rate < 80:
            return 'CRITICAL'
        elif cpu > 70 or memory > 70 or success_rate < 90:
            return 'WARNING'
        else:
            return 'HEALTHY'
    
    def generate_performance_report(self, hours=24):
        """Generate comprehensive performance report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'period_hours': hours,
            'system_health': self.get_system_health(),
            'metrics': {}
        }
        
        # Get stats for key metrics
        key_metrics = [
            'recognition_execution_time',
            'model_prediction_time',
            'preprocessing_time',
            'cpu_usage',
            'memory_usage'
        ]
        
        for metric in key_metrics:
            stats = self.get_metric_stats(metric, hours)
            if stats:
                report['metrics'][metric] = stats
        
        return report
    
    def plot_performance_trends(self, metric_name, hours=24, save_path=None):
        """Plot performance trends for a metric"""
        if metric_name not in self.metrics:
            print("No data available for metric: {}".format(metric_name))
            return
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_data = [
            item for item in self.metrics[metric_name]
            if item['timestamp'] > cutoff_time
        ]
        
        if not recent_data:
            print("No recent data for metric: {}".format(metric_name))
            return
        
        timestamps = [item['timestamp'] for item in recent_data]
        values = [item['value'] for item in recent_data]
        
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, values, marker='o', linewidth=2, markersize=4)
        plt.title('{} - Last {hours} Hours'.format(metric_name.replace("_", " ").title()))
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    def create_dashboard_data(self):
        """Create data for real-time dashboard"""
        return {
            'current_time': datetime.now().isoformat(),
            'system_health': self.get_system_health(),
            'recent_metrics': {
                name: list(deque)[-10:] if deque else []
                for name, deque in self.metrics.items()
            },
            'alerts': self.get_active_alerts()
        }
    
    def get_active_alerts(self):
        """Get active system alerts"""
        alerts = []
        health = self.get_system_health()
        
        if health['cpu_usage'] > 90:
            alerts.append({
                'level': 'CRITICAL',
                'message': "High CPU usage: {:.1f}%".format(health['cpu_usage'])
            })
        
        if health['memory_usage'] > 90:
            alerts.append({
                'level': 'CRITICAL',
                'message': "High memory usage: {:.1f}%".format(health['memory_usage'])
            })
        
        if health['recognition_success_rate'] < 80:
            alerts.append({
                'level': 'WARNING',
                'message': "Low success rate: {:.1f}%".format(health['recognition_success_rate'])
            })
        
        return alerts
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.monitoring = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join()
        logger.info("Performance monitoring stopped")

# Global monitor instance
monitor = PerformanceMonitor()

# Convenience decorators
def monitor_recognition(func):
    """Decorator for monitoring recognition functions"""
    return monitor.measure_time('recognition')(func)

def monitor_preprocessing(func):
    """Decorator for monitoring preprocessing functions"""
    return monitor.measure_time('preprocessing')(func)

def monitor_model_prediction(func):
    """Decorator for monitoring model prediction"""
    return monitor.measure_time('model_prediction')(func)

if __name__ == "__main__":
    # Test the monitoring system
    print("Testing performance monitoring system...")
    
    # Simulate some metrics
    for i in range(10):
        monitor.log_metric('test_metric', np.random.random())
        time.sleep(0.1)
    
    # Get stats
    stats = monitor.get_metric_stats('test_metric')
    print("Test metric stats: {}".format(stats))
    
    # Generate report
    report = monitor.generate_performance_report(hours=1)
    print("Performance report: {}".format(json.dumps(report, indent=2)))
    
    print("Performance monitoring test completed!")
