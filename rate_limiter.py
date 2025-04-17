import datetime

from connection import RedisConnection


class RateLimiter(object):
    """
    """
    THRESHOLD = 5
    # Duration within which till THRESHOLD number of requests can be made.
    TTL_DURATION = 30

    @classmethod
    def _get_connection(cls):
        connection = getattr(cls, '_connection', None)
        if connection is None:
            connection = RedisConnection()
            cls._connection = connection
        return connection

    @staticmethod
    def _set_first_request(identifier):
        redis_connection = RateLimiter._get_connection()
        connection = redis_connection.connection
        reset_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=RateLimiter.TTL_DURATION)
        value = {'count': 1, 'reset_at': reset_at.isoformat()}
        connection.hmset(identifier, value)

    @staticmethod
    def validate(identifier):
        """
        Check if this identifier should be allowed to proceed or not.
        """
        redis_connection = RateLimiter._get_connection()
        connection = redis_connection.connection
        entry = connection.hgetall(identifier)
        entry = {k.decode(): v.decode() for k, v in entry.items()}
        if entry == {}:
            # This doesn't exist in the cache yet.
            # This is the first request for this quota duration
            RateLimiter._set_first_request(identifier)
            return True
        else:
            # If the quota duration has already elapsed, a new quota window starts.
            reset_time = datetime.datetime.fromisoformat(entry['reset_at'])
            current_time = datetime.datetime.utcnow()
            if current_time > reset_time:
                RateLimiter._set_first_request(identifier)
                return True
            # There has already been a request in this quota duration
            current_count = int(entry['count'])
            if current_count >= RateLimiter.THRESHOLD:
                return False
            else:
                # Haven't reached the threshold yet 
                increased_count = current_count + 1
                connection.hset(identifier, 'count', increased_count)
                return True
