# Data Ingestion API

## Documentation

### Approach

This project implements a data ingestion system using FastAPI. The core goal is to accept a list of IDs from users and process them in batches, while ensuring:

- Controlled processing using a rate limiter
- Batches are created from input IDs (3 per batch)
- Prioritization: HIGH, MEDIUM, LOW
- Unique `ingestion_id` is generated for each request
- Status tracking of each ingestion via a REST endpoint

A worker thread runs in the background, fetching batches from a priority queue and processing them one at a time.

This solution is optimized for demonstration, lightweight testing, and assignment submission, and can be executed in Google Colab using ngrok for public access.

---

## Setup Instructions

### Requirements

- Python 3.7+
- Packages: fastapi, uvicorn, nest_asyncio, pyngrok

### Install Dependencies

```bash
pip install fastapi uvicorn nest_asyncio pyngrok
Running Locally
bash
Copy
Edit
uvicorn main:app --host 0.0.0.0 --port 8000
Navigate to: http://localhost:8000/docs

Running on Google Colab
Install required packages in Colab:

python
Copy
Edit
!pip install fastapi uvicorn nest_asyncio pyngrok
Uncomment and run the start function:

python
Copy
Edit
start()
Paste your ngrok auth token when prompted.

Access your public API URL shown in the output (e.g., https://xxxx.ngrok-free.app/docs)

Test Run Screenshot
Below is a screenshot showing a successful test run on Google Colab, with the API live and accessible via ngrok.


Replace screenshot.png with your actual uploaded screenshot in the repo.

Notes
This API supports concurrent ingestion tracking.

The rate limiter is set to 5 seconds between batch executions.

Useful for demonstrating concurrency, REST design, and lightweight background task handling.

vbnet
Copy
Edit

Let me know if you'd like the screenshot captured from your current Colab session and saved for upload to GitHub.









Tools



ChatGPT can make mistakes. Check important info. 
