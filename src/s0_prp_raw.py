from pathlib import Path
from PIL import Image
from collections import defaultdict

# Paths
RAW_DIR = Path("../data/raw/DB1_B")
OUT_DIR = Path("../data/processed")

OUT_DIR.mkdir(parents=True, exist_ok=True)

# Ομαδοποίηση εικόνων ανά subject (π.χ. 101, 102, ...)
subjects = defaultdict(list)

for img_path in RAW_DIR.glob("*.tif"):
    subject_id = img_path.stem.split("_")[0]  # "101"
    subjects[subject_id].append(img_path)

# Δημιουργία processed structure
for idx, (subject, images) in enumerate(sorted(subjects.items()), start=1):
    subject_dir = OUT_DIR / f"subject{idx:03d}"
    subject_dir.mkdir(exist_ok=True)

    for j, img_path in enumerate(sorted(images), start=1):
        img = Image.open(img_path).convert("L")  # grayscale
        out_path = subject_dir / f"img_{j:03d}.png"
        img.save(out_path)

    print(f"{subject_dir.name}: {len(images)} images")

print("Dataset preparation completed successfully.")
