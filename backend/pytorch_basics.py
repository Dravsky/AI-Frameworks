import torch

# Creating tensors
from_list = torch.tensor([1.0, 2.0, 3.0])
random = torch.randn(3, 3)
print("From list:", from_list)
print("Random 3x3:\n", random)

# Basic operations
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])
print("Addition:", a + b)

m1 = torch.randn(2, 3)
m2 = torch.randn(3, 2)
print("Matrix multiplication:\n", torch.matmul(m1, m2))

# Autograd
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x + 1    # y = x^2 + 2x + 1
y.backward()                # dy/dx = 2x + 2
print(f"x = {x.item()}, dy/dx = {x.grad.item()}")  # x = 3.0, dy/dx = 8.0
