import torch
from model import Autoencoder

model = Autoencoder()
model.load_state_dict(torch.load("ml/model.pth"))
model.eval()

def anomaly_score(angle, intensity):
    x = torch.tensor([[angle, intensity]], dtype=torch.float32)
    recon = model(x)
    loss = torch.mean((x - recon) ** 2)
    return loss.item()