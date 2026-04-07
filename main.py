from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Your Pydantic model(s) here
class Item(BaseModel):
    name: str
    description: str = None

# In-memory storage
items_db: dict[int, dict] = {}
next_id: int = 1

items_db[next_id] = {"name": "First Sample Item", "description": "This is the first sample item."}
next_id += 1
items_db[next_id] = {"name": "Second Sample Item", "description": "This is the second sample item."}
next_id += 1
items_db[next_id] = {"name": "Third Sample Item", "description": "This is the third sample item."}
next_id += 1

# API Endpoints
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items")
def read_items():
    return {"items": items_db}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = items_db.get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="404 - Item not found")
    
    return {"item": item}

# This outputs 200 by default; changed so it outputs the right status code.
@app.post("/items", status_code=201)
def create_item(created_item: Item):
    global next_id
    items_db[next_id] = created_item.model_dump()
    next_id = next_id + 1

    return {"new_item": items_db[next_id-1]}

@app.put("/items/{item_id}")
def update_item(item_id: int, update_item: Item):
    item = items_db.get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="404 - Item not found")
    
    items_db[item_id] = update_item.model_dump()

    return {"updated_item": items_db[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global next_id

    item = items_db.get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="404 - Item not found")
    
    deleted_item = items_db.pop(item_id)

    # This code should be deleted later; I just don't like when indexes become inaccurate.
    # This issue will go away when we switch to a database.
    next_id = 1
    new_item_db = {}
    for item in items_db.values():
        new_item_db[next_id] = item
        next_id = next_id + 1

    items_db.clear()
    items_db.update(new_item_db)

    return {"deleted_item": deleted_item}

# docker build -t my-awesome-api .
# docker run -p8000:8000 my-awesome-api

# Run with: uvicorn main:app --reload

# Copy/paste for POST/PUT method bodies
"""
{
    "name": "Test", "description": "Test description."
}
"""

# AI DISCLAIMER: ChatGPT 5.2 (Thinking) was used to consult for syntax within methods.
# I'm familiar with Node and Express so I'm used to the concepts but not the specific implementation in python.
# This code is written by me minus that. I basically used ChatGPT 5.2 like an interactive search engine (i.e. "How do I do 'x'?" or "What does 'x' mean?")