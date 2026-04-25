import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import json
import asyncio
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from ml.inference import anomaly_score
#from graph.neo4j_client import GraphHandler

app = FastAPI()

latest_data = {}

#graph = GraphHandler()

KAFKA_TOPIC = "experiment.data"
KAFKA_BOOTSTRAP = "127.0.0.1:9092"


import asyncio

async def consume():
    global latest_data

    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers="127.0.0.1:9092",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="experiment-group",
    )

    await consumer.start()
    print("✅ Kafka consumer started")

    try:
        async for msg in consumer:
            data = msg.value
            print("📥 RAW:", data)

            score = anomaly_score(data["angle"], data["intensity"])
            data["anomaly_score"] = score
            data["state"] = "ANOMALY" if score > 500 else "NORMAL"

            # ✅ ALWAYS update API state
            latest_data = data

            print("📡 UPDATED:", latest_data)

    finally:
        await consumer.stop()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())


@app.get("/data")
async def get_data():
    return latest_data


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/neo4j-health")
async def neo4j_health():
    try:
        with graph.driver.session() as session:
            session.run("RETURN 1")
        return {"status": "connected"}
    except:
        return {"status": "error"}
    
@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Kafka + ML + Neo4j pipeline active"
    }


