from function.flabelme2yolov8 import *
from function.flabelme2mask2 import *

import os
import shutil

# 預設路徑：來源為 datasets/labelme/labelme_dataset，輸出至 outputs/default_data/
DEFAULT_BASE_PATH = "./outputs/default_data"
DEFAULT_LABELME_SRC = "./datasets/labelme/labelme_dataset"


def create_default_data_dirs(base_path=DEFAULT_BASE_PATH):
    dirs = [
        os.path.join(base_path, "dataset_labelme"),
        os.path.join(base_path, "dataset_masks"),
        os.path.join(base_path, "dataset_yolo"),
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory created: {directory}")


def copy_labelme_dataset(src=DEFAULT_LABELME_SRC, dest=None, base_path=DEFAULT_BASE_PATH):
    if dest is None:
        dest = os.path.join(base_path, "dataset_labelme")
    if not os.path.exists(src):
        print(f"Source directory '{src}' does not exist.")
        return False
    os.makedirs(os.path.dirname(dest) if os.path.dirname(dest) else ".", exist_ok=True)
    shutil.copytree(src, dest, dirs_exist_ok=True)
    print(f"Contents of '{src}' copied to '{dest}'")
    return True


if __name__ == "__main__":
    base_path = DEFAULT_BASE_PATH
    src_labelme = DEFAULT_LABELME_SRC
    dest_labelme = os.path.join(base_path, "dataset_labelme")
    dest_masks = os.path.join(base_path, "dataset_masks")
    dest_yolo = os.path.join(base_path, "dataset_yolo")

    create_default_data_dirs(base_path)
    if not copy_labelme_dataset(src=src_labelme, dest=dest_labelme, base_path=base_path):
        exit(1)

    # 從複製後的 labelme 目錄轉出 YOLO（輸出到 dataset_yolo），以及 mask（輸出到 dataset_masks）
    other_path = os.path.join("..", "dataset_yolo") + os.sep
    lme2yolov8(dest_labelme, seg=True, val_size=0.2, json_name=None, other_path=other_path)
    lme2mask2(dest_labelme, dest_masks)
