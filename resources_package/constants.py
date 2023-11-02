import yaml
import os
from threading import Lock

class ConstantMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            else:
                cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]
    
class Constant(metaclass=ConstantMeta):

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        yaml_path = os.path.join(dir_path, 'resource.yaml')
        with open(yaml_path, 'r') as f:
            self.data = yaml.safe_load(f)
            self.spotify = self.data["spotify_api_access_data"]