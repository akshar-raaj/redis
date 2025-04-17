import sys
import redis


DEFAULT_QUEUE = 'hello'
DEFAULT_MESSAGE = 'Hello World'


def get_connection():
    connection = redis.Redis()
    return connection


def publish(queue: str, message: str):
    connection = get_connection()
    connection.lpush(queue, message)


if __name__ == "__main__":
    queue = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUEUE
    message = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MESSAGE
    publish(queue=queue, message=message)
