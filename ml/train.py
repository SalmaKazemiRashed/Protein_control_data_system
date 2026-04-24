import torch
import numpy as np
from model import Autoencoder

model = Autoencoder()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.MSELoss()

data = []

# The 
for _ in range(2000):
    angle = np.random.uniform(0, 180)
    intensity = 1000 * np.exp(-((angle - 60) ** 2) / 400)
    data.append([angle, intensity])

data = torch.tensor(data, dtype=torch.float32)

for epoch in range(100):
    output = model(data)
    loss = criterion(output, data)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item()}")

torch.save(model.state_dict(), "ml/model.pth")