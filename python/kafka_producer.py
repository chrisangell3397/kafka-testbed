"""Simple Kafka producer that sends incrementing numbers to a topic.

Creates the topic first if it does not already exist.

Requires: pip install confluent-kafka
"""
import time

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic # type: ignore

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = 'numbers-test-v0p1'
NUM_PARTITIONS = 1
REPLICATION_FACTOR = 1
DELAY_SECONDS = 1.0


def ensure_topic(admin: AdminClient, topic: str) -> None:
    """Create the topic if it is not already present on the cluster."""
    metadata = admin.list_topics(timeout=10)
    if topic in metadata.topics:
        print(f"Topic '{topic}' already exists")
        return

    futures = admin.create_topics(
        [NewTopic(topic, num_partitions=NUM_PARTITIONS, replication_factor=REPLICATION_FACTOR)]
    )
    for name, future in futures.items():
        try:
            future.result()  # block until the topic is created
            print(f"Created topic '{name}'")
        except Exception as e:
            # Another client may have created it in the meantime
            if "TOPIC_ALREADY_EXISTS" in str(e):
                print(f"Topic '{name}' already exists")
            else:
                raise


def delivery_report(err, msg) -> None:
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Sent {msg.value().decode()} -> "
            f"{msg.topic()}[{msg.partition()}] @ offset {msg.offset()}"
        )


def main() -> None:
    conf = {"bootstrap.servers": BOOTSTRAP_SERVERS}
    ensure_topic(AdminClient(conf), TOPIC) # type: ignore

    producer = Producer(conf)
    counter = 0
    try:
        while True:
            producer.produce(
                TOPIC, value=str(counter).encode("utf-8"), callback=delivery_report
            )
            producer.poll(0)  # serve delivery callbacks
            counter += 1
            time.sleep(DELAY_SECONDS)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        producer.flush()


if __name__ == "__main__":
    main()
