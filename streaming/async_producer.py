import asyncio
import json
from aiokafka import AIOKafkaProducer
from simulator.experiment import generate_data

KAFKA_BOOTSTRAP = "127.0.0.1:9092"
TOPIC = "experiment.data"


async def produce():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    await producer.start()
    print(" Kafka producer started")

    try:
        while True:
            # Generate simulated experiment data
            data = generate_data()

            # Send to Kafka
            await producer.send_and_wait(TOPIC, data)

            print(f" Sent: {data}")

            # Control data rate (adjust as needed)
            await asyncio.sleep(0.5)

    except asyncio.CancelledError:
        print(" Producer stopped")

    finally:
        await producer.stop()
        print(" Kafka producer closed")


if __name__ == "__main__":
    try:
        asyncio.run(produce())
    except KeyboardInterrupt:
        print(" Exiting producer")