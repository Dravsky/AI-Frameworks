import torch
import torch.nn as nn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
import torch.optim as optim
import numpy as np
from model import SimpleClassifier

# Load the iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split 80/20 into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test  = torch.tensor(X_test,  dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)
y_test  = torch.tensor(y_test,  dtype=torch.long)

# Wrap in TensorDataset so each batch contains (features, labels)
trainloader = DataLoader(TensorDataset(X_train, y_train), batch_size=16, shuffle=True)
testloader  = DataLoader(TensorDataset(X_test,  y_test),  batch_size=16, shuffle=False)

classes = ('setosa', 'versicolor', 'virginica')

# Define the model
model = SimpleClassifier(input_size=4, hidden_size=16, num_classes=3)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

train_losses = []
train_accuracies = []

for epoch in range(50):
    running_loss = 0.0
    correct = 0
    total = 0

    model.train()
    for iris_data, labels in trainloader:
        optimizer.zero_grad()
        outputs = model(iris_data)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    epoch_loss = running_loss / len(trainloader)
    epoch_acc = 100 * correct / total
    train_losses.append(epoch_loss)
    train_accuracies.append(epoch_acc)

    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch + 1}: Loss={epoch_loss:.4f}, Accuracy={epoch_acc:.1f}%")

model.eval()
correct = 0
total = 0
class_correct = [0] * len(classes)
class_total = [0] * len(classes)

with torch.no_grad():
    for iris_data, labels in testloader:
        outputs = model(iris_data)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

        # Per-class accuracy tracking
        for label, prediction in zip(labels, predicted):
            class_total[label] += 1
            if label == prediction:
                class_correct[label] += 1

print(f"\nFinal Test Accuracy: {100 * correct / total:.1f}%\n")
print("Per-class accuracy:")
for i in range(len(classes)):
    print(f"  {classes[i]:<12} {100 * class_correct[i] / class_total[i]:.1f}%")

torch.save(model.state_dict(), 'model.pth')