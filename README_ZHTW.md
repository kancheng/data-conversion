# 資料轉換

[English](README.md) · [简体中文 (Simplified Chinese)](README_ZHCN.md)

用於圖像分割與目標檢測的標註格式轉換工具：**Labelme**（JSON）、**YOLO**（txt + dataset.yaml）與**遮罩**圖像之間的互轉。

---

## 專案結構

| 路徑 | 說明 |
|------|------|
| **datasets/** | 放置來源資料：`labelme/labelme_dataset`、`mask/mask_dataset`、`yolo/yolo_dataset`。見 [datasets/README.md](datasets/README.md)。 |
| **function/** | 各腳本及 `init-*.py` 呼叫的轉換邏輯。 |
| **test/** | 範例與測試資料。 |
| **outputs/** | 預設輸出根目錄（如 init 腳本使用的 `outputs/default_data/`）。 |

### 主要轉換腳本

| 腳本 | 作用 |
|------|------|
| **labelme2mask.py** | Labelme JSON → 遮罩圖像 |
| **labelme2mask2.py** | Labelme JSON → 遮罩圖像（擴充版，含 train/val 劃分） |
| **labelme2yolov5.py** | Labelme JSON → YOLOv5 格式 |
| **labelme2yolov8.py** | Labelme JSON → YOLOv8 格式（偵測或加 `--seg` 分割） |
| **mask2labelme.py** | 遮罩圖像 → Labelme JSON |
| **mask2yolo.py** | 遮罩資料集 → YOLO 格式 |
| **yolo2labelme.py** | YOLO 資料集 → Labelme JSON |
| **yolo2labelme2.py** | YOLO → Labelme（另一實作） |
| **yolo2masks.py** | YOLO 標籤 + 圖像 → 遮罩圖像 |
| **ydataset2images.py** | YOLO 資料集 → 匯出圖像（raw/res） |

### 一鍵初始化腳本

| 腳本 | 行為 |
|------|------|
| **init-labelme.py** | 建立輸出目錄，將 `datasets/labelme/labelme_dataset` 複製到 `outputs/default_data/dataset_labelme`，再轉為 YOLO 與遮罩。 |
| **init-mask.py** | 複製遮罩資料集到 `dataset_masks`，再轉為 YOLO 與 Labelme。 |
| **init-yolo.py** | 複製 YOLO 資料集到 `dataset_yolo`，再轉為 Labelme 與遮罩。 |

在專案根目錄執行，例如：

```bash
python init-labelme.py
```

---

## 安裝

```bash
pip install -r requirements.txt
```

可選（YOLO ↔ Labelme 需解析 YAML）：`pip install pyyaml`

使用鏡像範例：

```bash
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

---

## 使用說明（命令列）

### Labelme → 遮罩

- **labelme2mask.py**：`--input_dir`、`--output_dir`
- **labelme2mask2.py**：`--input_dir`、`--output_dir`（輸出含 train/test 的 images 與 masks）

```bash
python labelme2mask.py --input_dir <labelme目錄> --output_dir <輸出目錄>
python labelme2mask2.py --input_dir <labelme目錄> --output_dir <輸出目錄>
```

### Labelme → YOLO

- **labelme2yolov5.py** / **labelme2yolov8.py**：`--json_dir`、`--val_size`（預設 0.1）、`--json_name`（可選，單檔）、`--seg`（分割格式）

輸出預設寫在 `json_dir` 下（如 `YOLODataset/` 或 `YOLODataset_seg/`），除非透過 function 版本指定其他路徑。

```bash
python labelme2yolov5.py --json_dir <labelme_json目錄> [--val_size 0.1] [--seg]
python labelme2yolov8.py --json_dir <labelme_json目錄> [--val_size 0.1] [--seg]
```

Labelme JSON 可含內嵌 `imageData` 或僅用外部 `imagePath`，兩種方式皆支援。

### 遮罩 → Labelme / YOLO

- **mask2labelme.py**：`--input`、`--output`（遮罩資料集根目錄 → Labelme 輸出目錄；需在腳本中設定 label_names）。
- **mask2yolo.py**：`--input`、`--output`（遮罩資料集根目錄 → YOLO 輸出根目錄）。

遮罩資料集結構：`train/images`、`train/masks`、`val/...` 或 `images/train`、`masks/train`、`images/val`、`masks/val`。

```bash
python mask2yolo.py --input <遮罩資料集根目錄> --output <yolo輸出根目錄>
python mask2labelme.py --input <遮罩資料集根目錄> --output <labelme輸出目錄>
```

### YOLO → Labelme / 遮罩

- **yolo2labelme.py**：`--input_dir`（含 `dataset.yaml` 的資料集根目錄）、`--out`（Labelme 輸出目錄）、`--skip`（可選）。
- **yolo2masks.py**：`--txt`（標籤目錄）、`--img`（圖像目錄）、`--out`（遮罩輸出根目錄）。需有 `labels/train`、`labels/val`、`images/train`、`images/val`。

```bash
python yolo2labelme.py --input_dir <yolo資料集根目錄> --out <labelme輸出目錄>
python yolo2masks.py --txt <labels路徑> --img <images路徑> --out <遮罩輸出目錄>
```

### YOLO 資料集 → 圖像匯出

- **ydataset2images.py**：`--ppath`（`dataset.yaml` 路徑）、`--output`（輸出目錄，含 raw/res）。

```bash
python ydataset2images.py --ppath <dataset.yaml路徑> --output <輸出目錄>
```

---

## 範例流程

1. 將 Labelme JSON（若用 `imagePath` 則需對應圖像）放入如 `datasets/labelme/labelme_dataset/`。
2. 執行 `python init-labelme.py`，會在 `outputs/default_data/` 下複製並轉換為 YOLO 與遮罩。
3. 或手動執行：先 `labelme2mask2` 或 `labelme2yolov8 --seg`，再依需求使用 `mask2yolo` 或 YOLO 輸出。
4. 在 `outputs/` 下檢視結果。

---

## 授權

MIT，詳見 [LICENSE](LICENSE)。

---

## 聯絡

[GitHub Issues](https://github.com/kancheng/data-conversion/issues)
