# Protein Experiment Control & Data System  
**EPICS + Kafka + PyTorch + Neo4j**

This project reflects key aspects of software and control systems:

Integration of data acquisition and control systems

Real-time diagnostics and monitoring

Use of distributed streaming architectures

Handling and structuring experimental data

Bridging scientific workflows with modern software engineering practices

overall project looks like this:

```plaintext

protein-experiment-system/
│
├── README.md
├── requirements.txt
│
├── simulator/
│   └── experiment.py
│
├── streaming/
│   └── producer.py
│
├── ml/
│   ├── model.py
│   ├── train.py
│   └── inference.py
│
├── graph/
│   └── neo4j_client.py
│
├── app/
│   └── main.py
│
└── run_all.py
```


## Overview

This project simulates a simplified neutron scattering experiment on protein samples and demonstrates how experimental control systems, data streaming, machine learning, and data modelling can be integrated into a unified workflow.


---

## Key Features

- Real-time experiment simulation (protein scattering signal)
- Data streaming using Apache Kafka
- Machine learning-based anomaly detection (PyTorch-Tensorflow)
- Graph-based experiment tracking using Neo4j
- Modular and extensible system design

---

## System Architecture

Simulator → Kafka → ML Inference → Neo4j → Dashboard

---

## Motivation

Modern neutron and accelerator facilities rely on complex, distributed systems where:

- Experimental control is handled via frameworks such as EPICS
- Data is streamed and processed in real time
- Diagnostics and metadata relationships are critical for understanding experiment outcomes

This project demonstrates a simplified but realistic version of such a system.

---

## Components

### 1. Experiment Simulator
Simulates protein scattering intensity as a function of angle, including noise and injected anomalies.

### 2. Data Streaming (Kafka)
Streams experiment data in real time to downstream consumers.

### 3. Machine Learning (PyTorch)
A ML model (e.g., autoencoder model) detects anomalies in the experimental signal.

### 4. Graph Database (Neo4j)
Stores relationships between:
- Experiments
- Measurements
- System states (normal / anomaly)

Example query: 

```cypher
MATCH (m:Measurement)-[:HAS_STATE]->(s:State {label: "ANOMALY"})
RETURN m
```

This enables flexible querying and experiment diagnostics.

### 5. Dashboard
Provides a simple API endpoint for real-time monitoring.

---


##  How to run full system (Docker + app)
🐳 Step 1 — Start Kafka + Neo4j (removed it for this version)
```bash
docker compose up -d
```

Check:
```bash
docker ps
```

🚀 Step 2 — Run producer
```bash
python streaming/async_producer.py
```

⚡ Step 3 — Run FastAPI

```bash
uvicorn app.main:app --reload
```

🌐 Step 4 — Open dashboard
```plaintext
http://127.0.0.1:8000
```



## ⚠️ Known Issues Fixed

Kafka connection refused
Fixed by exposing Docker port 9092

Neo4j authentication failure
Fixed by resetting credentials and .env loading


WebSocket disconnect
Fixed using reconnect + safe broadcasting

Chart freezing
Fixed by proper Chart.js update lifecycle