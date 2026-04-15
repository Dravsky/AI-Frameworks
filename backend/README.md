# Item Management API

A FastAPI-based REST API for managing items with CRUD operations.

## Installation

Install the required dependencies using pip:

```
pip install -r requirements.txt
```

## Running the Server

To run the server with auto-reload for development:

```
uvicorn main:app --reload
```

The server will start on `http://127.0.0.1:8000` by default.

## Available Endpoints

- `GET /` - Returns a hello world message
- `GET /items` - Returns all items
- `GET /items/{item_id}` - Returns a specific item by ID
- `POST /items` - Creates a new item (expects JSON with `name` and optional `description`)
- `PUT /items/{item_id}` - Updates an existing item by ID
- `DELETE /items/{item_id}` - Deletes an item by ID

> This README was written by GitHub Copilot (Raptor mini, Preview).