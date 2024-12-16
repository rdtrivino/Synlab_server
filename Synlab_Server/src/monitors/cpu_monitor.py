import psutil
from datetime import datetime
import logging

class CPUMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_metrics(self):
        try:
            return {
                'timestamp': datetime.now(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'cpu_per_core': psutil.cpu_percent(percpu=True),
                'cpu_freq': psutil.cpu_freq()._asdict(),
                'cpu_stats': psutil.cpu_stats()._asdict(),
                'cpu_count': {
                    'physical': psutil.cpu_count(logical=False),
                    'logical': psutil.cpu_count(logical=True)
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting CPU metrics: {str(e)}")
            return None
