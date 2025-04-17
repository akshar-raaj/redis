import sys
import time
import redis


DEFAULT_QUEUE = 'hello'


def get_connection():
    connection = redis.Redis()
    return connection


def consume(queue):
    connection = get_connection()
    while True:
        value = connection.rpop(queue)
        if value is not None:
            print(f"Processed {value}")
        # Mimic a processing time of 1 second
        time.sleep(1)


if __name__ == '__main__':
    queue = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUEUE
    consume(queue)
