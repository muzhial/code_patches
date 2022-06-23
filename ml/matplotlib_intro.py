import numpy as np
import matplotlib.pyplot as plt
import cv2
import torch
import torch.nn.functional as F
from torchvision import transforms


def feat_visz(frame, m):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((512, 512)),
        transforms.ToTensor()
    ])
    img = np.array(img)
    img = transform(img)
    plt.axis('off')
    plt.imshow(img.numpy().transpose((1, 2, 0)))
    plt.savefig('./src.png')
    img = img.unsqueeze(0)

    o = m(img)
    for x in o:
        print(x.shape)

    for l in range(len(o) - 1):
        plt.figure(figsize=(30, 30))
        l_viz = o[l][0, :, :, :]
        l_viz = l_viz.detach().numpy()
        for i, ffeat in enumerate(l_viz):
            if i == 4:
                break
            plt.subplot(2, 2, i + 1)
            plt.imshow(ffeat, cmap='gray')
            plt.axis('off')
        plt.savefig(f'./layer_{l}.png')
        plt.close()

# def tmp():
#     img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     transform = transforms.Compose([
#         transforms.ToPILImage(),
#         transforms.Resize(args.img_size),
#         transforms.ToTensor()
#     ])
#     img = np.array(img)
#     img = transform(img)
#     img = img.numpy().transpose((1, 2, 0))
#     img = img * 255
#     img = img.astype(np.uint8)
#     out.write(img)
