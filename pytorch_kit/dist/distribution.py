import argparse
import os

import torch
import torch.distributed as dist


LOCAL_RANK = int(os.getenv('LOCAL_RANK', -1))
RANK = int(os.getenv('RANK', -1))
WORLD_SIZE = int(os.getenv('WORLD_SIZE', 1))
print(f'{LOCAL_RANK}: {RANK} / {WORLD_SIZE}')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_rank', type=int, default=0)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    num_gpus = torch.cuda.device_count()
    torch.cuda.set_device(LOCAL_RANK)

    dist.init_process_group(backend='nccl')

    # print(torch.cuda.current_device())
    x = torch.rand(1, 3, 224, 224)
    x = x.to('cuda')
    print('===>', x.device)


if __name__ == '__main__':
    main()

