import sys
sys.path.append('/home/wzx/dl3')
from codebase.enseg.startup import startup_train

args = dict(
    interpreter="/home/wzx/.conda/envs/enseg/bin/python",
    gpus="6,7",
    config="/home/wzx/weizhixiang/ensegment/configs/segmaeh256w256bs4/segmaneh256w256_bs4_convnext_segmae1.py",
    port="11123",
    cache_dir="/home/wzx/dl3/.cache/test_enseg",
    log_dir="/home/wzx/weizhixiang/ensegment/work_dirs/test_enseg",
)
startup_train(**args)
