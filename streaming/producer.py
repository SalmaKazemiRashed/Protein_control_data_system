from kafka import KafkaProducer
import json
import time
from simulator.experiment import generate_data

producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def run():
    while True:
        data = generate_data()
        producer.send("experiment.data", data)
        print("Produced:", data)
        time.sleep(0.5)

if __name__ == "__main__":
    run()