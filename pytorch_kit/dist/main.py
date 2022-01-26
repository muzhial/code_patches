import argparse
import random
import warnings
from loguru import logger
import time

import torch
import torch.backends.cudnn as cudnn

from launch import launch
from dist_utils import (
    configure_nccl, configure_omp, get_num_devices, get_local_rank)


def make_parser():
    parser = argparse.ArgumentParser()
    # distributed
    parser.add_argument(
        "--dist-backend",
        default="nccl",
        type=str,
        help="distributed backend"
    )
    parser.add_argument(
        "--dist-url",
        default=None,
        type=str,
        help="url used to set up distributed training",
    )
    parser.add_argument(
        "-d", "--devices", default=None, type=int, help="device for training"
    )
    parser.add_argument(
        "--num_machines", default=1, type=int, help="num of node for training"
    )
    parser.add_argument(
        "--machine_rank",
        default=0,
        type=int,
        help="node rank for multi-node training"
    )
    parser.add_argument(
        "--fp16",
        dest="fp16",
        default=False,
        action="store_true",
        help="Adopting mix precision training.",
    )
    parser.add_argument(
        "--cache",
        dest="cache",
        default=False,
        action="store_true",
        help="Caching imgs to RAM for fast training.",
    )
    parser.add_argument(
        "-o",
        "--occupy",
        dest="occupy",
        default=False,
        action="store_true",
        help="occupy GPU memory first for training.",
    )
    parser.add_argument(
        "--seed",
        default=0,
        help="set seed"
    )
    return parser


@logger.catch
def main(args):
    if args.seed is not None:
        random.seed(args.seed)
        torch.manual_seed(args.seed)
        cudnn.deterministic = True
        warnings.warn(
            "You have chosen to seed training. This will turn on the CUDNN deterministic setting, "
            "which can slow down your training considerably! You may see unexpected behavior "
            "when restarting from checkpoints."
        )

    # set environment variables for distributed training
    configure_nccl()
    configure_omp()
    cudnn.benchmark = True

    calc()


def calc():
    a = torch.randn(3, 64, 1024, 2048)
    b = torch.randint(16, size=(1024, 2048))
    a = a.to('cuda')
    b = b.to('cuda')
    print(f"rank-{get_local_rank()} GPU occupied now ...")
    while True:
        # a[:, :, :, :] = b
        time.sleep(0.05)
        a = a * b


if __name__ == "__main__":
    args = make_parser().parse_args()

    num_gpu = get_num_devices() if args.devices is None else args.devices
    assert num_gpu <= get_num_devices()

    dist_url = "auto" if args.dist_url is None else args.dist_url
    launch(
        main,
        num_gpu,
        args.num_machines,
        args.machine_rank,
        backend=args.dist_backend,
        dist_url=dist_url,
        args=(args,),
    )
