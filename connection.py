import redis


class RedisConnection(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.connection = redis.Redis()
        return cls._instance

    @classmethod
    def get_instance(cls):
        return RedisConnection()
