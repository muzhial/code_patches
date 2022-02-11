import torch
import torch.nn as nn


# stack
y, x = torch.meshgrid([torch.arange(3), torch.arange(2)])
print(y)
print(x)
z = torch.stack((x, y), dim=2)
print(z)
