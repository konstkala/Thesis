# convert_tif_to_png.py
from PIL import Image
import os

# Φάκελος με .tif εικόνες
input_folder = "data/raw/subject002"
# Φάκελος όπου θα σώζονται τα .png
output_folder = "data/raw/subject002"
os.makedirs(output_folder, exist_ok=True)

# Διασχίζουμε όλα τα αρχεία στον φάκελο
for fname in os.listdir(input_folder):
    if fname.lower().endswith(".tif"):  # μόνο αρχεία .tif
        input_path = os.path.join(input_folder, fname)
        output_path = os.path.join(output_folder, fname.replace(".tif", ".png"))
        
        # Άνοιγμα .tif
        img = Image.open(input_path)
        # Αποθήκευση ως .png
        img.save(output_path)
        print(f"Μετατροπή: {fname} -> {os.path.basename(output_path)}")

print("Όλες οι εικόνες μετατράπηκαν σε .png!")
