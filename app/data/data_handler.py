import json
from .redis_manager import RedisManager

class DataHandler:
    REDIS_KEY = "message_service_data"
    
    def __init__(self):
        self.redis = RedisManager().get_connection()
        
    def load_data(self):
        data = self.redis.get(self.REDIS_KEY)
        return json.loads(data) if data else RedisManager.DEFAULT_DATA

    def save_data(self, data):
        self.redis.set(self.REDIS_KEY, json.dumps(data))
        self.redis.publish('data_updates', json.dumps(data))