import socketio
from ..data.redis_manager import RedisManager

class WebSocketManager:
    def __init__(self):
        self.sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)
        self.redis = RedisManager().get_connection()
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe('data_updates')

        @self.sio.event
        def connect(sid, environ):
            self._start_background_thread()

        def background_thread():
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    self.sio.emit('data_update', message['data'])

        self._start_background_thread = lambda: self.sio.start_background_task(background_thread)
