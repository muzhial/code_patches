import argparse
import os

import torch
import torch.distributed as dist

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_rank', type=int, default=0)
    args = parser.parse_args()
    return args

def main():
    rank = int(os.environ['RANK'])
    args = parse_args()

    num_gpus = torch.cuda.device_count()
    torch.cuda.set_device(rank % num_gpus)

    dist.init_process_group(backend='nccl')

    print(torch.cuda.current_device())


if __name__ == '__main__':
    main()

