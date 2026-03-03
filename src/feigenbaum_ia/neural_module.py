import torch
import torch.nn as nn


class FeigenbaumModule(nn.Module):
    def __init__(self, input_dim=64, r=3.5699):
        super().__init__()
        self.fc = nn.Linear(input_dim, input_dim)
        self.r = r  # parâmetro de bifurcação

    def forward(self, x):
        x = torch.sigmoid(self.fc(x))
        # dinâmica logistica simplificada
        return self.r * x * (1 - x)
