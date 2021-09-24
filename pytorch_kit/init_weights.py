import torch
import torch.nn as nn


"""
init weights
"""
model = nn.Module()
for m in model.modules():
    if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
    elif isinstance(m, nn.BatchNorm2d):
        nn.init.constant_(m.weight, 1)
        nn.init.constant_(m.bias, 0)


class Neti(nn.Module):
    
    def __init__(self):
        super(Neti, self).__init__()
        
        self.fc1 = nn.Linear(2, 2)
        self.fc2 = nn.Linear(2, 2, bias=False)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.fc2(out)
        
        return out

def _init_weight(m):
    if isinstance(m, nn.Linear):
        nn.init.xavier_normal_(m.weight)
        if m.bias is not None:
            nn.init.constant_(m.bias, 0)
    elif isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
    elif isinstance(m, nn.BatchNorm2d):
        nn.init.constant_(m.weight, 1)
        if m.bias is not None:
            nn.init.constant_(m.bias, 0)


neti = Neti()

print("===> hasattr:")
for chld_name, chld in neti.named_children():
        print(f'{chld_name} -->', hasattr(chld, "bias"))
        
print("===> apply fn:")
neti.apply(_init_weight)
for para in neti.parameters():
    print(para)
