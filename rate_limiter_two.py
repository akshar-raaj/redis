"""
An identifier should be allowed at max n requests per unit of time.
"""
from connection import RedisConnection


class RateLimiter(object):

    MAX_REQUESTS = 3
    INVERVAL = 60

    @classmethod
    def get_connection(cls):
        return RedisConnection().connection

    @classmethod
    def check(cls, identifier):
        """
        Is this identifier still within the limits
        """
        connection = cls.get_connection()
        value = connection.get(identifier)
        # Not yet in the cache, hence this is the first request of this window.
        if value is None:
            connection.set(identifier, 1, ex=cls.INVERVAL)
            return True
        value = int(value)
        # A request has already happened in this window
        # Alread MAX_REQUESTS requests have been made in this window
        if value >= cls.MAX_REQUESTS:
            return False
        else:
            # This request should be allowed, but at the same time increment the counter
            connection.incr(identifier)
            return True
