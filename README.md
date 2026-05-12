# Full Stack App with Docker

This project is a full-stack item manager built with an Express/EJS frontend, a FastAPI backend, MongoDB for persistence, a dedicated model-serving container, and Docker Compose for container orchestration.

## Architecture

```
Client
  │
  ▼
Frontend (Express/EJS) :3000
  │
  ▼
API (FastAPI) :8000
  │              │
  ▼              ▼
MongoDB       Model Service (FastAPI/PyTorch) :8001
:27017          │
                ▼
            Iris Classifier (SimpleClassifier)
```

- `frontend/`
  - Express server with EJS views
  - Renders the item list, forms for create/edit/delete, and the Iris predictor form
  - Calls the backend API from server-side `fetch()`
- `backend/`
  - FastAPI REST API
  - Uses a MongoDB data access layer in `data/dal.py`
  - Stores items in the `item_manager.items` collection
  - Proxies prediction requests to the model service
- `model_service/`
  - Standalone FastAPI app that loads and serves the trained PyTorch model
  - Exposes `/predict` and `/health` endpoints
  - Runs independently so the model can be updated without touching the main API
- `db`
  - MongoDB container from the official `mongo:latest` image
  - Persists data through the Docker volume `db-data`

## Features

- `GET /items` displays all saved items
- `POST /items` creates a new item
- `PUT /items/{item_id}` updates an existing item
- `DELETE /items/{item_id}` deletes an existing item
- `POST /predict` classifies an Iris flower — proxied from the API to the model service
- Data persists between restarts through MongoDB and the named Docker volume
- CORS middleware is enabled in the FastAPI backend

## Predict Endpoint

**`POST /predict`** (main API — proxies to model service)

Request body:
```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

The four values correspond to sepal length, sepal width, petal length, and petal width — all in centimeters. Exactly 4 values are required.

Response:
```json
{
  "prediction": "setosa",
  "confidence": 0.9981
}
```

- `prediction` — one of `"setosa"`, `"versicolor"`, or `"virginica"`
- `confidence` — the softmax probability (0–1) for the predicted class, rounded to 4 decimal places

The main API does not load PyTorch directly. It forwards the request to the model service at `http://model-service:8001/predict` and returns the response.

## Docker Model Runner

For Part 1 of Lab 5, the model `ai/gemma4:E2B` was pulled using Docker Model Runner.

- **Model pulled:** `ai/gemma4:E2B`
- **Endpoint exposed:** OpenAI-compatible HTTP API via llama.cpp at `http://localhost:12434/engines/llama.cpp/v1/chat/completions` (requires host-side TCP support enabled in Docker Desktop)
- **Test query:** "Explain what Docker is in one sentence."
- **Response:** A large JSON object containing metadata about the completion alongside the generated message content — not just the final text, but fields like `id`, `model`, `choices`, `usage`, etc.

## Project Structure

```text
AI-Frameworks/
├─ backend/
│  ├─ data/
│  │  └─ dal.py
│  ├─ Dockerfile
│  ├─ main.py
│  └─ requirements.txt
├─ frontend/
│  ├─ public/
│  ├─ views/
│  ├─ Dockerfile
│  ├─ index.js
│  └─ package.json
├─ model_service/
│  ├─ model/
│  │  ├─ model.py
│  │  └─ model.pth
│  ├─ Dockerfile
│  ├─ docker_model.py
│  ├─ pytorch_basics.py
│  ├─ requirements.txt
│  ├─ serve.py
│  └─ training.py
├─ docker-compose.yaml
└─ README.md
```

## Running with Docker

From the project root:

```bash
docker compose up --build
```

After startup:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Model Service: `http://localhost:8001`
- MongoDB: `mongodb://localhost:27017`

To stop the services:

```bash
docker compose down
```

To stop the services and remove the MongoDB volume:

```bash
docker compose down -v
```

## Docker Setup

`docker-compose.yaml` defines four services:

- `frontend`
  - builds from `./frontend`
  - maps port `3000:3000`
  - mounts `./frontend:/app`
  - uses `BACKEND_URL=http://api:8000`
- `api`
  - builds from `./backend`
  - maps port `8000:8000`
  - mounts `./backend:/app`
  - uses `MONGO_URL=mongodb://db:27017` and `MODEL_SERVICE_URL=http://model-service:8001`
  - waits for `db` to start and `model-service` to pass its healthcheck
- `model-service`
  - builds from `./model_service`
  - maps port `8001:8001`
  - mounts `./model_service:/app`
  - healthcheck hits `/health` every 10s
- `db`
  - uses `mongo:latest`
  - maps port `27017:27017`
  - mounts `db-data:/data/db`

## Local Development

The app also has fallback defaults for host-only runs:

- frontend backend target: `http://127.0.0.1:8000`
- backend Mongo target: `mongodb://localhost:27017`
- backend model service target: `http://localhost:8001`

Typical host-only startup:

```bash
# model service
uvicorn serve:app --reload --port 8001

# backend
uvicorn main:app --reload

# frontend
npm start
```

## API Response Models

The backend uses Pydantic models for:

- `ItemCreate`
- `ItemUpdate`
- `ItemRead`
- wrapper response models for single-item and list responses

MongoDB `_id` values are converted into string `id` values before the API returns data to the frontend.

## AI Disclaimer

The frontend implementation, styling, and Express-to-backend integration were developed with assistance from OpenAI GPT-5 through Codex. The generated work was reviewed, discussed, and iterated on during development. This README was also generated by the same model.

# Human Written
I choose to use MongoDB for this project. Frankly speaking, I did so because I am most familiar with it. However, I could still list the benefits of a flexible schema and good documentation. Since it's clear that our "item" database is a placeholder, using something like MongoDB is a good choice.
- Erik W.
