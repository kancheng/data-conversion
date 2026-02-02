# 数据转换

[English](README.md) · [繁體中文 (Traditional Chinese)](README_ZHTW.md)

用于图像分割与目标检测的标注格式转换工具：**Labelme**（JSON）、**YOLO**（txt + dataset.yaml）与**掩码**图像之间的互转。

---

## 项目结构

| 路径 | 说明 |
|------|------|
| **datasets/** | 放置源数据：`labelme/labelme_dataset`、`mask/mask_dataset`、`yolo/yolo_dataset`。见 [datasets/README.md](datasets/README.md)。 |
| **function/** | 各脚本及 `init-*.py` 调用的转换逻辑。 |
| **test/** | 示例与测试数据。 |
| **outputs/** | 默认输出根目录（如 init 脚本使用的 `outputs/default_data/`）。 |

### 主要转换脚本

| 脚本 | 作用 |
|------|------|
| **labelme2mask.py** | Labelme JSON → 掩码图像 |
| **labelme2mask2.py** | Labelme JSON → 掩码图像（扩展版，含 train/val 划分） |
| **labelme2yolov5.py** | Labelme JSON → YOLOv5 格式 |
| **labelme2yolov8.py** | Labelme JSON → YOLOv8 格式（检测或加 `--seg` 分割） |
| **mask2labelme.py** | 掩码图像 → Labelme JSON |
| **mask2yolo.py** | 掩码数据集 → YOLO 格式 |
| **yolo2labelme.py** | YOLO 数据集 → Labelme JSON |
| **yolo2labelme2.py** | YOLO → Labelme（另一实现） |
| **yolo2masks.py** | YOLO 标签 + 图像 → 掩码图像 |
| **ydataset2images.py** | YOLO 数据集 → 导出图像（raw/res） |

### 一键初始化脚本

| 脚本 | 行为 |
|------|------|
| **init-labelme.py** | 创建输出目录，将 `datasets/labelme/labelme_dataset` 复制到 `outputs/default_data/dataset_labelme`，再转为 YOLO 与掩码。 |
| **init-mask.py** | 复制掩码数据集到 `dataset_masks`，再转为 YOLO 与 Labelme。 |
| **init-yolo.py** | 复制 YOLO 数据集到 `dataset_yolo`，再转为 Labelme 与掩码。 |

在项目根目录执行，例如：

```bash
python init-labelme.py
```

---

## 安装

```bash
pip install -r requirements.txt
```

可选（YOLO ↔ Labelme 需解析 YAML）：`pip install pyyaml`

使用国内镜像示例：

```bash
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

---

## 使用说明（命令行）

### Labelme → 掩码

- **labelme2mask.py**：`--input_dir`、`--output_dir`
- **labelme2mask2.py**：`--input_dir`、`--output_dir`（输出含 train/test 的 images 与 masks）

```bash
python labelme2mask.py --input_dir <labelme目录> --output_dir <输出目录>
python labelme2mask2.py --input_dir <labelme目录> --output_dir <输出目录>
```

### Labelme → YOLO

- **labelme2yolov5.py** / **labelme2yolov8.py**：`--json_dir`、`--val_size`（默认 0.1）、`--json_name`（可选，单文件）、`--seg`（分割格式）

输出默认写在 `json_dir` 下（如 `YOLODataset/` 或 `YOLODataset_seg/`），除非通过 function 版本指定其他路径。

```bash
python labelme2yolov5.py --json_dir <labelme_json目录> [--val_size 0.1] [--seg]
python labelme2yolov8.py --json_dir <labelme_json目录> [--val_size 0.1] [--seg]
```

Labelme JSON 可含内嵌 `imageData` 或仅用外部 `imagePath`，两种方式均支持。

### 掩码 → Labelme / YOLO

- **mask2labelme.py**：`--input`、`--output`（掩码数据集根目录 → Labelme 输出目录；需在脚本中配置 label_names）。
- **mask2yolo.py**：`--input`、`--output`（掩码数据集根目录 → YOLO 输出根目录）。

掩码数据集结构：`train/images`、`train/masks`、`val/...` 或 `images/train`、`masks/train`、`images/val`、`masks/val`。

```bash
python mask2yolo.py --input <掩码数据集根目录> --output <yolo输出根目录>
python mask2labelme.py --input <掩码数据集根目录> --output <labelme输出目录>
```

### YOLO → Labelme / 掩码

- **yolo2labelme.py**：`--input_dir`（含 `dataset.yaml` 的数据集根目录）、`--out`（Labelme 输出目录）、`--skip`（可选）。
- **yolo2masks.py**：`--txt`（标签目录）、`--img`（图像目录）、`--out`（掩码输出根目录）。需有 `labels/train`、`labels/val`、`images/train`、`images/val`。

```bash
python yolo2labelme.py --input_dir <yolo数据集根目录> --out <labelme输出目录>
python yolo2masks.py --txt <labels路径> --img <images路径> --out <掩码输出目录>
```

### YOLO 数据集 → 图像导出

- **ydataset2images.py**：`--ppath`（`dataset.yaml` 路径）、`--output`（输出目录，含 raw/res）。

```bash
python ydataset2images.py --ppath <dataset.yaml路径> --output <输出目录>
```

---

## 示例流程

1. 将 Labelme JSON（若用 `imagePath` 则需对应图像）放入如 `datasets/labelme/labelme_dataset/`。
2. 执行 `python init-labelme.py`，会在 `outputs/default_data/` 下复制并转换为 YOLO 与掩码。
3. 或手动执行：先 `labelme2mask2` 或 `labelme2yolov8 --seg`，再按需使用 `mask2yolo` 或 YOLO 输出。
4. 在 `outputs/` 下查看结果。

---

## 许可证

MIT，详见 [LICENSE](LICENSE)。

---

## 联系

[GitHub Issues](https://github.com/kancheng/data-conversion/issues)
