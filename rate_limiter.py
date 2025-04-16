import datetime

from connection import RedisConnection


class RateLimiter(object):
    """
    """
    THRESHOLD = 3
    # Duration within which till THRESHOLD number of requests can be made.
    TTL_DURATION = 60

    @staticmethod
    def validate(identifier):
        """
        Check if this identifier should be allowed to proceed or not.
        """
        redis_connection = RedisConnection()
        connection = redis_connection.connection
        entry = connection.hgetall(identifier)
        entry = {k.decode(): v.decode() for k, v in entry.items()}
        if entry == {}:
            # This doesn't exist in the cache yet.
            # This is the first request for this quota duration
            reset_at = datetime.datetime.now() + datetime.timedelta(seconds=RateLimiter.TTL_DURATION)
            value = {'count': 1, 'reset_at': reset_at.isoformat()}
            connection.hmset(identifier, value)
            return True
        else:
            # There has already been a request in this quota duration
            current_count = int(entry['count'])
            if current_count >= RateLimiter.THRESHOLD:
                return False
            else:
                # Haven't reached the threshold yet 
                increased_count = current_count + 1
                connection.hset(identifier, 'count', increased_count)
                return True
