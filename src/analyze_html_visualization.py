"""
KeplerMapper HTML Parser
Extracts visualization metadata and graph structure from mapper.html
"""

import json
import re
from pathlib import Path

HTML_FILE = Path("../data/mapper/mapper.html")
RESULTS_DIR = Path("../results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("ANALYZING MAPPER.HTML VISUALIZATION")
print("=" * 70)
print()

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract metadata from HTML
print("1. VISUALIZATION METADATA")
print("-" * 70)

# Find title
title_match = re.search(r'<title>(.*?)</title>', html_content)
if title_match:
    print(f"Title: {title_match.group(1)}")

# Find generator
generator_match = re.search(r'content="(.*?KeplerMapper.*?)"', html_content)
if generator_match:
    print(f"Generator: {generator_match.group(1)}")

# Find meta information
meta_match = re.search(r'<div id="meta_content">(.*?)</div>', html_content, re.DOTALL)
if meta_match:
    meta_text = re.sub(r'<[^>]+>', '', meta_match.group(1))
    meta_text = re.sub(r'\s+', ' ', meta_text).strip()
    print(f"Meta: {meta_text[:200]}...")

print()

# Extract graph statistics from the HTML
print("2. GRAPH STRUCTURE FROM VISUALIZATION")
print("-" * 70)

# Find all node references in the HTML
node_pattern = r'"node_id":\s*"([^"]+)"'
node_refs = re.findall(node_pattern, html_content)
print(f"Total nodes in visualization: {len(set(node_refs))}")

# Find all edge references
edge_pattern = r'"source":\s*"([^"]+)".*?"target":\s*"([^"]+)"'
edges = re.findall(edge_pattern, html_content, re.DOTALL)
print(f"Total edges in graph: {len(edges)}")

# Extract custom data if present
print()
print("3. INTERACTIVE FEATURES DETECTED")
print("-" * 70)

features = []

if 'hover' in html_content.lower():
    features.append("✓ Hover tooltips enabled")
if 'click' in html_content.lower():
    features.append("✓ Click interactions available")
if 'zoom' in html_content.lower() or 'd3' in html_content.lower():
    features.append("✓ Zoom/Pan capabilities")
if 'legend' in html_content.lower():
    features.append("✓ Legend included")
if 'color' in html_content.lower():
    features.append("✓ Color-coded visualization")

for feature in features:
    print(feature)

print()
print("4. VISUALIZATION SUMMARY")
print("-" * 70)
print()
print("The mapper.html is an interactive topological visualization that shows:")
print("  • How fingerprint samples cluster in embedding space")
print("  • Overlapping regions (cubes) with UMAP lens")
print("  • Connections between topologically similar samples")
print("  • Node coloring representing subject/cluster assignments")
print()
print("To view: Open mapper.html in a web browser to interact with the graph")
print()

# Save analysis summary
summary = {
    "file": str(HTML_FILE),
    "analysis": {
        "nodes_detected": len(set(node_refs)),
        "edges_detected": len(edges),
        "features": features,
        "visualization_type": "KeplerMapper - Topological Data Analysis",
        "lens": "UMAP 2D projection",
        "clustering_method": "DBSCAN"
    },
    "interpretation": {
        "what_it_shows": "How fingerprint embeddings organize topologically in the feature space",
        "node_meaning": "A cluster of fingerprints in a local region of embedding space",
        "edge_meaning": "Topological connectivity between clusters (persistence)",
        "color_meaning": "Different subjects/clusters for identification",
        "size_meaning": "Number of samples in each topological region"
    }
}

json_path = RESULTS_DIR / "html_visualization_metadata.json"
with open(json_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"✓ HTML analysis saved to: {json_path}")
print()
print("=" * 70)
