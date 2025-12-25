import numpy as np
import pandas as pd
from pathlib import Path
import kmapper as km
from sklearn.cluster import DBSCAN

# -------------------------
# Paths
# -------------------------
UMAP_DIR = Path("../data/umap")
EMB_DIR = Path("../data/embeddings")
OUT_DIR = Path("../data/mapper")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Load data
# -------------------------
X_umap = np.load(UMAP_DIR / "X_umap.npy")
meta = pd.read_csv(EMB_DIR / "meta.csv")

print("UMAP shape:", X_umap.shape)

# -------------------------
# Mapper
# -------------------------
mapper = km.KeplerMapper(verbose=1)

lens = X_umap  # 2D lens

cover = km.Cover(
    n_cubes=10,
    perc_overlap=0.3
)

clusterer = DBSCAN(
    eps=0.5,
    min_samples=3
)

graph = mapper.map(
    lens,
    X_umap,
    cover=cover,
    clusterer=clusterer
)

# -------------------------
# Visualization
# -------------------------
html_path = OUT_DIR / "mapper.html"
mapper.visualize(
    graph,
    path_html=html_path,
    title="Fingerprint Mapper (UMAP lens)"
)

print("Mapper graph saved to:", html_path)

# -------------------------
# Node purity (security analysis)
# -------------------------
rows = []

for node, indices in graph["nodes"].items():
    subjects = meta.iloc[indices]["subject"]
    purity = subjects.value_counts(normalize=True).iloc[0]
    dominant = subjects.value_counts().idxmax()

    rows.append({
        "node": node,
        "size": len(indices),
        "dominant_subject": dominant,
        "purity": purity
    })

purity_df = pd.DataFrame(rows)
purity_df.to_csv(OUT_DIR / "node_purity.csv", index=False)

print("Node purity saved.")
