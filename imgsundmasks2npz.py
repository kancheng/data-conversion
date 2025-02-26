

import os
import numpy as np
from PIL import Image
import glob
from sklearn.model_selection import train_test_split

def convert_to_npz(image_folder, mask_folder, output_path, image_size=(256, 256)):
    # 收集所有圖像文件
    image_paths = glob.glob(os.path.join(image_folder, "*.png"))  # 假設影像是 .png 格式
    mask_paths = [os.path.join(mask_folder, os.path.basename(img_path))
                  for img_path in image_paths]  # 掩模文件與影像文件同名

    print(f"Number of images: {len(image_paths)}")  # 檢查文件數量
    print(f"Number of masks: {len(mask_paths)}")  # 檢查文件數量

    if len(image_paths) == 0:
        raise ValueError("No images found. Please check your image folder path and file format.")

    images = []
    masks = []

    # 讀取影像和對應的掩模
    for img_path, mask_path in zip(image_paths, mask_paths):
        img = Image.open(img_path).convert("RGB")  # 讀取影像並轉換為 RGB
        mask = Image.open(mask_path).convert("L")  # 讀取掩模並轉換為灰階

        img = img.resize(image_size)  # 調整影像大小
        mask = mask.resize(image_size)  # 調整掩模大小

        img_array = np.array(img)
        mask_array = np.array(mask)

        images.append(img_array)
        masks.append(mask_array)

    images = np.array(images)
    masks = np.array(masks)

    # 分割訓練集和測試集
    x_train, x_test, y_train, y_test = train_test_split(images, masks, test_size=0.2, random_state=42)

    # 儲存為 .npz 文件
    np.savez(output_path, x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test)

# 設置數據路徑
image_folder = "D:/proj/dataset_masks/images"
mask_folder = "D:/proj/dataset_masks/masks"
output_path = "D:/proj/data.npz"  # 輸出的 .npz 文件路徑

# 開始轉換
convert_to_npz(image_folder, mask_folder, output_path)

