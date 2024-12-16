import yaml
import os
import logging

class Config:
    def __init__(self, config_path='config/config.yaml'):
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        try:
            if not os.path.exists(self.config_path):
                self._create_default_config()
            
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return self._get_default_config()

    def _create_default_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as file:
            yaml.dump(self._get_default_config(), file)

    def _get_default_config(self):
        return {
            'monitoring': {
                'interval': 5,  # segundos
                'enabled_monitors': ['cpu', 'memory', 'disk', 'network']
            },
            'database': {
                'url': 'sqlite:///monitoring.db',
                'backup_interval': 86400  # 24 horas
            },
            'logging': {
                'level': 'INFO',
                'retention_days': 7
            },
            'alerts': {
                'cpu_threshold': 80,
                'memory_threshold': 80,
                'disk_threshold': 90
            }
        }

    def get(self, key, default=None):
        try:
            keys = key.split('.')
            value = self.config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
