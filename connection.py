import redis


class RedisConnection(object):
    """
    Usage:
        redis_connection = RedisConnection()
        conn = redis_connection.connection
        conn.set('foo', 'bar')
        foo = conn.get('foo') # Returns 'bar'
    """
    # Supposed to be a private variable, hence kept it with _ prepended.
    # Also supposed to be a static, i.e class variable and not an instance variable.
    _instance = None

    # Java has a way to restrict the invocation of constructor by making it private.
    # Python doesn't have such way, even dunder methods can be called.
    # A user might calls RedisConnection() directly.
    # As instantiation happens inside __new__ hence, override it to ensure only one instance ever would be created.
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.connection = redis.Redis()
        return cls._instance

    # Global point of access
    @classmethod
    def get_instance(cls):
        return RedisConnection()
