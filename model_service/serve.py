import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model.model import SimpleClassifier

app = FastAPI()

CLASSES = ('setosa', 'versicolor', 'virginica')

# This isn't actually needed for my implementation using Express, but I added it since it's in the assignment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float

# Load model at startup
classifier = None

@app.on_event("startup")
def load_model():
    global classifier
    classifier = SimpleClassifier(input_size=4, hidden_size=16, num_classes=3)
    classifier.load_state_dict(torch.load('model/model.pth', weights_only=True))
    classifier.eval()

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": classifier is not None}

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

# Run with uvicorn serve:app --reload --port 8001