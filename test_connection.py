import redis
from connection import RedisConnection


# Add the test cases for the RedisConnection class. Use pytest
def test_get_instance():
    redis_connection = RedisConnection.get_instance()
    assert isinstance(redis_connection, RedisConnection)

    redis_connection2 = RedisConnection.get_instance()
    assert redis_connection is redis_connection2


def test_connection():
    redis_connection = RedisConnection.get_instance()
    connection = redis_connection.connection
    assert isinstance(connection, redis.Redis)
