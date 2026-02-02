# Data Conversion

[繁體中文 (Traditional Chinese)](README_ZHTW.md) · [简体中文 (Simplified Chinese)](README_ZHCN.md)

Tools for converting annotation formats used in image segmentation and object detection: **Labelme** (JSON), **YOLO** (txt + dataset.yaml), and **mask** images.

---

## Project Structure

| Path | Description |
|------|-------------|
| **datasets/** | Place source data here: `labelme/labelme_dataset`, `mask/mask_dataset`, `yolo/yolo_dataset`. See [datasets/README.md](datasets/README.md). |
| **function/** | Reusable conversion logic used by the scripts and by the `init-*.py` runners. |
| **test/** | Sample files for quick tests. |
| **outputs/** | Default output root (e.g. `outputs/default_data/` used by init scripts). |

### Main conversion scripts

| Script | Role |
|--------|------|
| **labelme2mask.py** | Labelme JSON → mask images |
| **labelme2mask2.py** | Labelme JSON → mask images (extended, train/val split) |
| **labelme2yolov5.py** | Labelme JSON → YOLOv5 format |
| **labelme2yolov8.py** | Labelme JSON → YOLOv8 format (detection or segmentation with `--seg`) |
| **mask2labelme.py** | Mask images → Labelme JSON |
| **mask2yolo.py** | Mask dataset → YOLO format |
| **yolo2labelme.py** | YOLO dataset → Labelme JSON |
| **yolo2labelme2.py** | YOLO → Labelme (alternative) |
| **yolo2masks.py** | YOLO labels + images → mask images |
| **ydataset2images.py** | YOLO dataset → extracted images (raw/res) |

### Init scripts (one‑click pipeline)

| Script | Action |
|--------|--------|
| **init-labelme.py** | Create output dirs, copy `datasets/labelme/labelme_dataset` → `outputs/default_data/dataset_labelme`, then convert to YOLO and masks. |
| **init-mask.py** | Copy mask dataset → `dataset_masks`, then convert to YOLO and Labelme. |
| **init-yolo.py** | Copy YOLO dataset → `dataset_yolo`, then convert to Labelme and masks. |

Run from project root, e.g.:

```bash
python init-labelme.py
```

---

## Install

```bash
pip install -r requirements.txt
```

Optional (for YOLO ↔ Labelme): `pip install pyyaml`

Using a mirror (e.g. China):

```bash
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

---

## Usage (CLI)

### Labelme → Mask

- **labelme2mask.py**: `--input_dir`, `--output_dir`
- **labelme2mask2.py**: `--input_dir`, `--output_dir` (output has train/test images + masks)

```bash
python labelme2mask.py --input_dir <labelme_dir> --output_dir <output_dir>
python labelme2mask2.py --input_dir <labelme_dir> --output_dir <output_dir>
```

### Labelme → YOLO

- **labelme2yolov5.py** / **labelme2yolov8.py**: `--json_dir`, `--val_size` (default 0.1), `--json_name` (optional, single file), `--seg` (segmentation format)

Output is written under `json_dir` (e.g. `YOLODataset/` or `YOLODataset_seg/`) unless the function version is used with a custom path.

```bash
python labelme2yolov5.py --json_dir <path_to_labelme_jsons> [--val_size 0.1] [--seg]
python labelme2yolov8.py --json_dir <path_to_labelme_jsons> [--val_size 0.1] [--seg]
```

Labelme JSON can use either embedded `imageData` or external `imagePath`; both are supported.

### Mask → Labelme / YOLO

- **mask2labelme.py**: `--input`, `--output` (mask dataset dir → labelme output dir; requires label_names in script).
- **mask2yolo.py**: `--input`, `--output` (mask dataset root → yolo output root).

Mask dataset layout: either `train/images`, `train/masks`, `val/...` or `images/train`, `masks/train`, `images/val`, `masks/val`.

```bash
python mask2yolo.py --input <mask_dataset_root> --output <yolo_output_root>
python mask2labelme.py --input <mask_dataset_root> --output <labelme_output_dir>
```

### YOLO → Labelme / Masks

- **yolo2labelme.py**: `--input_dir` (dataset root containing `dataset.yaml`), `--out` (labelme output dir), `--skip` (optional).
- **yolo2masks.py**: `--txt` (labels dir), `--img` (images dir), `--out` (mask output root). Expects `labels/train`, `labels/val`, `images/train`, `images/val`.

```bash
python yolo2labelme.py --input_dir <yolo_dataset_root> --out <labelme_output_dir>
python yolo2masks.py --txt <path_to_labels> --img <path_to_images> --out <mask_output_dir>
```

### YOLO dataset → images

- **ydataset2images.py**: `--ppath` (path to `dataset.yaml`), `--output` (output dir for raw/res images).

```bash
python ydataset2images.py --ppath <path_to_dataset.yaml> --output <output_dir>
```

---

## Example workflow

1. Put Labelme JSONs (and images if using `imagePath`) in e.g. `datasets/labelme/labelme_dataset/`.
2. Run `python init-labelme.py` to copy and convert to YOLO + masks under `outputs/default_data/`.
3. Or run conversions manually:  
   `labelme2mask2` / `labelme2yolov8 --seg` → then `mask2yolo` or use YOLO output as needed.
4. Check `outputs/` for results.

---

## License

MIT. See [LICENSE](LICENSE).

---

## Contact

[GitHub Issues](https://github.com/kancheng/data-conversion/issues)
