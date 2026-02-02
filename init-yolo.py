from function.fyolo2labelme import *
from function.fyolo2masks import *

import os
import shutil

# 預設路徑：來源為 datasets/yolo/yolo_dataset，輸出至 outputs/default_data/
# YOLO 來源需含 dataset.yaml 及 images/train、images/val、labels/train、labels/val
# Reference: https://github.com/kadapallaNithin/yolo2labelme/blob/main/yolo2labelme.py
DEFAULT_BASE_PATH = "./outputs/default_data"
DEFAULT_YOLO_SRC = "./datasets/yolo/yolo_dataset"


def create_default_data_dirs(base_path=DEFAULT_BASE_PATH):
    dirs = [
        os.path.join(base_path, "dataset_labelme"),
        os.path.join(base_path, "dataset_masks"),
        os.path.join(base_path, "dataset_yolo"),
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory created: {directory}")


def copy_yolo_dataset(src=DEFAULT_YOLO_SRC, dest=None, base_path=DEFAULT_BASE_PATH):
    if dest is None:
        dest = os.path.join(base_path, "dataset_yolo")
    if not os.path.exists(src):
        print(f"Source directory '{src}' does not exist.")
        return False
    os.makedirs(os.path.dirname(dest) if os.path.dirname(dest) else ".", exist_ok=True)
    shutil.copytree(src, dest, dirs_exist_ok=True)
    print(f"Contents of '{src}' copied to '{dest}'")
    return True


if __name__ == "__main__":
    base_path = DEFAULT_BASE_PATH
    src_yolo = DEFAULT_YOLO_SRC
    dest_labelme = os.path.join(base_path, "dataset_labelme")
    dest_masks = os.path.join(base_path, "dataset_masks")
    dest_yolo = os.path.join(base_path, "dataset_yolo")

    create_default_data_dirs(base_path)
    if not copy_yolo_dataset(src=src_yolo, dest=dest_yolo, base_path=base_path):
        exit(1)

    # 從複製後的 yolo 目錄轉出 labelme 與 mask
    yolo2labelme(dest_yolo, dest_labelme)
    yolo2masks(
        os.path.join(dest_yolo, "labels"),
        os.path.join(dest_yolo, "images"),
        dest_masks,
    )
