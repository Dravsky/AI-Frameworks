import torch

x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x + 1    # y = x^2 + 2x + 1
y.backward()                # dy/dx = 2x + 2
print(f"x = {x.item()}, dy/dx = {x.grad.item()}")  # x = 3.0, dy/dx = 8.0

import torch.nn as nn

class SimpleClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.layer2(x)
        return x