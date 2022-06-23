import torch
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.dataloader import default_collate


class MyDataset(Dataset):

    def __init__(self):
        super().__init__()

        self.x = torch.randn(256, 3, 64, 64)
        self.y = torch.randint(2, size=(256, ))

    def __len__(self):
        return self.x.size(0)

    def __getitem__(self, index):
        data = {}
        data['x'] = self.x[index]
        data['y'] = self.y[index]
        return data


def collate(batch):
    """
    batch is `list` type
    batch: [{'x': tensor(B, H, W), 'y': tensor(B, )}, ...]
    """
    print(f'==> {type(batch)}, {batch[0]["x"].size()}')
    return default_collate(batch)

def main():
    dataset = MyDataset()
    dataloader = DataLoader(
        dataset,
        collate_fn=collate,
        batch_size=30,
        num_workers=0,
        drop_last=False)

    for i, data in enumerate(dataloader):
        print(i, type(data), data['x'].size(), data['y'].size())


if __name__ == '__main__':
    main()
