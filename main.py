# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UFBhspWVA49HxcTQwS74O7aGEtmtA3Rr
"""
#  Data Ingestion API System (Colab Compatible, Assignment Ready)

#  Install dependencies
!pip install fastapi uvicorn nest_asyncio pyngrok

#  Import libraries
import nest_asyncio
nest_asyncio.apply()

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from typing import List, Dict, Literal
from threading import Thread
from time import sleep, time
from queue import PriorityQueue
from pyngrok import ngrok

#  Initialize FastAPI
app = FastAPI()

#  Define input model
class IngestRequest(BaseModel):
    ids: List[int]
    priority: Literal['HIGH', 'MEDIUM', 'LOW']

#  Priority mapping (lower value = higher priority)
priority_map = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}

#  Constants
PROCESSING_LIMIT = 3
RATE_LIMIT_SECONDS = 5

#  Shared queues and stores
queue = PriorityQueue()
ingestion_store: Dict[str, Dict] = {}

#  Worker thread to process batches respecting rate limit and priority
last_processed_time = 0.0

def worker():
    global last_processed_time
    while True:
        if queue.empty():
            sleep(1)
            continue

        _, created_time, ingestion_id, batch = queue.get()
        now = time()
        wait_time = RATE_LIMIT_SECONDS - (now - last_processed_time)
        if wait_time > 0:
            sleep(wait_time)

        batch['status'] = 'triggered'
        last_processed_time = time()

        for _ in batch['ids']:
            sleep(1)  # Simulate external API processing delay

        batch['status'] = 'completed'

        ingestion = ingestion_store[ingestion_id]
        statuses = [b['status'] for b in ingestion['batches']]

        if all(s == 'completed' for s in statuses):
            ingestion['status'] = 'completed'
        elif any(s == 'triggered' for s in statuses):
            ingestion['status'] = 'triggered'
        else:
            ingestion['status'] = 'yet_to_start'

#  Start background worker
Thread(target=worker, daemon=True).start()

#  Ingest endpoint
@app.post("/ingest")
def ingest(data: IngestRequest):
    ingestion_id = str(uuid4())
    ids = data.ids
    priority = data.priority
    now = time()

    batches = [ids[i:i + PROCESSING_LIMIT] for i in range(0, len(ids), PROCESSING_LIMIT)]
    batch_objs = []

    for b in batches:
        batch_id = str(uuid4())
        batch = {"batch_id": batch_id, "ids": b, "status": "yet_to_start"}
        batch_objs.append(batch)
        queue.put((priority_map[priority], now, ingestion_id, batch))

    ingestion_store[ingestion_id] = {
        "ingestion_id": ingestion_id,
        "status": "yet_to_start",
        "batches": batch_objs
    }

    return {"ingestion_id": ingestion_id}

#  Status endpoint
def get_status(ingestion_id: str):
    if ingestion_id not in ingestion_store:
        raise HTTPException(status_code=404, detail="Ingestion ID not found")
    return ingestion_store[ingestion_id]

#  Run with public URL using ngrok (Colab Compatible)
def start():
    from getpass import getpass
    import os
    authtoken = getpass("Paste your ngrok authtoken here: ")
    os.system(f"ngrok config add-authtoken {authtoken}")
    public_url = ngrok.connect(8000)
    print(f"\n🚀 Your app is live at: {public_url}/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

#  Start the app
start()



