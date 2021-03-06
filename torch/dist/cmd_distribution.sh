GPUS=$1
PORT=${PORT:-29500}

python -m torch.distributed.launch --nproc_per_node=$GPUS --master_port=$PORT \
    cmd_distribution.py
