'''Simple Kafka consumer that prints messages from a topic to the console.

Requires: pip install confluent-kafka
'''
from confluent_kafka import Consumer, KafkaError

BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC = 'numbers-test-v0p1'
GROUP_ID = 'numbers-consumer-python'


def main() -> None:
    consumer = Consumer(
        {
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'group.id': GROUP_ID,
            'auto.offset.reset': 'earliest',  # start from the beginning if no committed offset
        }
    )
    consumer.subscribe([TOPIC])
    print(f"Listening on '{TOPIC}'... (Ctrl+C to stop)")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF: # type: ignore
                    continue
                print(f'Error: {msg.error()}')
                continue

            print(
                f'{msg.topic()}[{msg.partition()}] @ offset {msg.offset()}: '
                f"{msg.value().decode('utf-8')}" # type: ignore
            )
    except KeyboardInterrupt:
        print('\nStopping...')
    finally:
        consumer.close()


if __name__ == '__main__':
    main()
