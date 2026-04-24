import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load .env file
load_dotenv()
print(os.getenv("NEO4J_PASSWORD"))
      

class GraphHandler:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")

        if not all([uri, user, password]):
            raise ValueError("Missing Neo4j environment variables")

        self.driver = GraphDatabase.driver(
            uri,
            auth=(user, password)
        )

    def close(self):
        self.driver.close()

    def store_measurement(self, data):
        with self.driver.session() as session:
            session.execute_write(self._write_tx, data)

    def _write_tx(self, tx, data):
        tx.run("""
        MERGE (e:Experiment {id: $exp_id})

        CREATE (m:Measurement {
            angle: $angle,
            intensity: $intensity,
            timestamp: $timestamp,
            anomaly_score: $score
        })

        MERGE (s:State {label: $state})

        MERGE (e)-[:HAS_MEASUREMENT]->(m)
        MERGE (m)-[:HAS_STATE]->(s)
        """,
        exp_id="EXP001",
        angle=data["angle"],
        intensity=data["intensity"],
        timestamp=data["timestamp"],
        score=data["anomaly_score"],
        state=data["state"])