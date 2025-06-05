Data Ingestion API

A simple FastAPI-based service to ingest data in batches with priority handling and rate limiting.

##  Technologies Used

- Python 3
- FastAPI
- Uvicorn
- Nest AsyncIO
- Pyngrok (for Colab testing)
- Threading and Queues

---

## Features

- Accepts IDs with priorities: HIGH / MEDIUM / LOW
- Processes data in batches (3 IDs per batch)
- Batches are processed with rate limits (1 batch every 5 sec)
- Each request is tracked using a unique `ingestion_id`
- Status can be checked anytime

---

##  How to Run Locally

uvicorn main:app --host 0.0.0.0 --port 8000

Visit - http://localhost:8000/docs

- On Google Colab
   run the last cell  in which start is writtern
  after installing dependencies and creating functions

  API Endpoints
1. /ingest – Submit IDs
Method: POST
Body Example:

json
Copy
Edit
{
  "ids": [1, 2, 3, 4, 5],
  "priority": "HIGH"
}

2. /status/{ingestion_id} – Check Status
Method: GET
Response: Shows status of all batches
