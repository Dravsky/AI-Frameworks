import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from data.dal import ItemDAL
from model import SimpleClassifier

item_dal = ItemDAL()

CLASSES = ('setosa', 'versicolor', 'virginica')
classifier = SimpleClassifier(input_size=4, hidden_size=16, num_classes=3)
classifier.load_state_dict(torch.load('model.pth', weights_only=True))
classifier.eval()

app = FastAPI()

# This isn't actually needed for my implementation using Express, but I added it since it's in the assignment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models here
class ItemCreate(BaseModel):
    name: str
    description: str = None

class ItemUpdate(BaseModel):
    name: str
    description: str = None

class ItemRead(BaseModel):
    id: str
    name: str
    description: str = None

class SingleItemResponse(BaseModel):
    item: ItemRead

class ItemReadAll(BaseModel):
    items: list[ItemRead]

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float

# API Endpoints
@app.get("/")
def read_root():
    return ItemReadAll(items=item_dal.get_all_items())

@app.get("/items")
def read_items():
    return ItemReadAll(items=item_dal.get_all_items())

@app.get("/items/{item_id}")
def read_item(item_id: str):
    item = item_dal.get_item(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="404 - Item not found")
    
    return SingleItemResponse(item=item)

# This outputs 200 by default; changed so it outputs the right status code.
@app.post("/items", status_code=201)
def create_item(created_item: ItemCreate):
    new_item = item_dal.create_item(created_item.model_dump())

    return SingleItemResponse(item=new_item)

@app.post("/predict")
def predict(req: PredictionRequest):
    if len(req.features) != 4:
        raise HTTPException(status_code=422, detail="Expected exactly 4 features")
    tensor = torch.tensor([req.features], dtype=torch.float32)
    with torch.no_grad():
        output = classifier(tensor)
        probabilities = F.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    return PredictionResponse(
        prediction=CLASSES[predicted.item()],
        confidence=round(confidence.item(), 4)
    )

@app.put("/items/{item_id}")
def update_item(item_id: str, update_item: ItemUpdate):
    item = item_dal.update_item(item_id, update_item.model_dump())

    if item is None:
        raise HTTPException(status_code=404, detail="404 - Item not found")

    return SingleItemResponse(item=item)

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    deleted_item = item_dal.delete_item(item_id)

    if deleted_item is None:
        raise HTTPException(status_code=404, detail="404 - Item not found")

    return SingleItemResponse(item=deleted_item)

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