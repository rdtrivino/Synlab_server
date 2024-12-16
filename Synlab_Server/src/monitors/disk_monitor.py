import psutil
from datetime import datetime
import logging

class DiskMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_metrics(self):
        try:
            partitions = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    partitions.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent
                    })
                except Exception:
                    continue

            io_counters = psutil.disk_io_counters()
            
            return {
                'timestamp': datetime.now(),
                'partitions': partitions,
                'io_counters': {
                    'read_bytes': io_counters.read_bytes,
                    'write_bytes': io_counters.write_bytes,
                    'read_count': io_counters.read_count,
                    'write_count': io_counters.write_count
                } if io_counters else None
            }
        except Exception as e:
            self.logger.error(f"Error getting disk metrics: {str(e)}")
            return None
