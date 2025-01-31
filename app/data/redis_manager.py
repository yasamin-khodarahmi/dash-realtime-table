import json
from redis import Redis

class RedisManager:
    _instance = None
    DEFAULT_DATA = [{'multi': [], 'active': False}]

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.redis = Redis(*args, **kwargs)
            cls._instance._initialize_data()
        return cls._instance

    def _initialize_data(self):
        if not self.redis.exists('message_service_data'):
            self.redis.set('message_service_data', json.dumps(self.DEFAULT_DATA))

    def get_connection(self):
        return self.redis
