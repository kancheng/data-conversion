from function.fmask2yolo import *
from function.fmask2labelme import *

import os
import shutil

# 預設路徑：來源為 datasets/mask/mask_dataset，輸出至 outputs/default_data/
# mask 資料集需含 train/val 下的 images 與 masks（或 images/train、masks/train 等）
DEFAULT_BASE_PATH = "./outputs/default_data"
DEFAULT_MASK_SRC = "./datasets/mask/mask_dataset"


def create_default_data_dirs(base_path=DEFAULT_BASE_PATH):
    dirs = [
        os.path.join(base_path, "dataset_labelme"),
        os.path.join(base_path, "dataset_masks"),
        os.path.join(base_path, "dataset_yolo"),
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory created: {directory}")


def copy_mask_dataset(src=DEFAULT_MASK_SRC, dest=None, base_path=DEFAULT_BASE_PATH):
    if dest is None:
        dest = os.path.join(base_path, "dataset_masks")
    if not os.path.exists(src):
        print(f"Source directory '{src}' does not exist.")
        return False
    os.makedirs(os.path.dirname(dest) if os.path.dirname(dest) else ".", exist_ok=True)
    shutil.copytree(src, dest, dirs_exist_ok=True)
    print(f"Contents of '{src}' copied to '{dest}'")
    return True


# 依實際資料集類別修改；key 為 mask 灰度值，value 為 labelme 類別名稱
DEFAULT_LABEL_NAMES = {0: "object1", 1: "object2"}


if __name__ == "__main__":
    base_path = DEFAULT_BASE_PATH
    src_mask = DEFAULT_MASK_SRC
    dest_labelme = os.path.join(base_path, "dataset_labelme")
    dest_masks = os.path.join(base_path, "dataset_masks")
    dest_yolo = os.path.join(base_path, "dataset_yolo")

    create_default_data_dirs(base_path)
    if not copy_mask_dataset(src=src_mask, dest=dest_masks, base_path=base_path):
        exit(1)

    # 從複製後的 mask 目錄轉出 YOLO 與 labelme
    label_names = DEFAULT_LABEL_NAMES
    mask2yolo(dest_masks, dest_yolo)
    mask2labelme(dest_masks, dest_labelme, label_names)
