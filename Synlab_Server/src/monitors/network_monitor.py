import psutil
from datetime import datetime
import logging

class NetworkMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._last_io_counters = None
        self._last_timestamp = None

    def get_metrics(self):
        try:
            current_io = psutil.net_io_counters()
            current_time = datetime.now()
            
            connections = [conn._asdict() for conn in psutil.net_connections()]
            interfaces = psutil.net_if_addrs()
            
            metrics = {
                'timestamp': current_time,
                'interfaces': interfaces,
                'connections_count': len(connections),
                'io_counters': {
                    'bytes_sent': current_io.bytes_sent,
                    'bytes_recv': current_io.bytes_recv,
                    'packets_sent': current_io.packets_sent,
                    'packets_recv': current_io.packets_recv,
                    'errin': current_io.errin,
                    'errout': current_io.errout,
                    'dropin': current_io.dropin,
                    'dropout': current_io.dropout
                }
            }
            
            # Calcular velocidad de transferencia si hay datos previos
            if self._last_io_counters and self._last_timestamp:
                time_delta = (current_time - self._last_timestamp).total_seconds()
                metrics['transfer_rates'] = {
                    'upload_speed': (current_io.bytes_sent - self._last_io_counters.bytes_sent) / time_delta,
                    'download_speed': (current_io.bytes_recv - self._last_io_counters.bytes_recv) / time_delta
                }
            
            self._last_io_counters = current_io
            self._last_timestamp = current_time
            
            return metrics
        except Exception as e:
            self.logger.error(f"Error getting network metrics: {str(e)}")
            return None
