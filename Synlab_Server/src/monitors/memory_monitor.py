import psutil
from datetime import datetime
import logging

class MemoryMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_metrics(self):
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'timestamp': datetime.now(),
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used,
                    'free': memory.free
                },
                'swap': {
                    'total': swap.total,
                    'used': swap.used,
                    'free': swap.free,
                    'percent': swap.percent
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting memory metrics: {str(e)}")
            return None
