import os
import re
import shutil
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ── Config ──────────────────────────────────────────────────────────────────
TRANSLATED_DIR = Path("2_translated")
MERGED_DIR     = Path("2_translated_merged")
SIMILARITY_THRESHOLD = 0.92   # 0.0–1.0, higher = stricter match
# ────────────────────────────────────────────────────────────────────────────

MERGED_DIR.mkdir(exist_ok=True)

print("Loading sentence model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Collect all .md files recursively
files = list(TRANSLATED_DIR.rglob("*.md"))
print(f"Found {len(files)} files.")

# Read content of each file
contents = []
for f in files:
    try:
        contents.append(f.read_text(encoding="utf-8"))
    except:
        contents.append("")

# Generate embeddings from file content
print("Generating embeddings...")
embeddings = model.encode(contents, show_progress_bar=True, batch_size=32)

# Compare all pairs and group duplicates
print("Finding duplicates...")
n = len(files)
visited = [False] * n
groups  = []

for i in range(n):
    if visited[i]:
        continue
    group = [i]
    visited[i] = True
    for j in range(i + 1, n):
        if visited[j]:
            continue
        sim = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
        if sim >= SIMILARITY_THRESHOLD:
            group.append(j)
            visited[j] = True
    groups.append(group)

print(f"\nTotal unique groups: {len(groups)}")
dup_count = sum(len(g) - 1 for g in groups if len(g) > 1)
print(f"Duplicate files to be removed: {dup_count}")

# Merge: keep the longest file in each group, copy to MERGED_DIR
kept = 0
skipped = 0
log_lines = []

for group in groups:
    # Pick the file with the most content as the "best" version
    best_idx = max(group, key=lambda i: len(contents[i]))
    best_file = files[best_idx]

    # Clean destination filename
    dest_name = best_file.name
    dest_path = MERGED_DIR / dest_name

    # Avoid filename collisions
    counter = 1
    while dest_path.exists():
        dest_path = MERGED_DIR / f"{best_file.stem}_{counter}{best_file.suffix}"
        counter += 1

    shutil.copy2(best_file, dest_path)
    kept += 1

    if len(group) > 1:
        dupes = [files[i].name for i in group if i != best_idx]
        log_lines.append(f"MERGED → kept: {best_file.name} | removed: {dupes}")
        skipped += len(dupes)

# Write log
log_path = MERGED_DIR / "_dedup_log.txt"
log_path.write_text("\n".join(log_lines), encoding="utf-8")

print(f"\n✅ Done!")
print(f"   Kept:    {kept} unique files")
print(f"   Removed: {skipped} duplicates")
print(f"   Output:  {MERGED_DIR}/")
print(f"   Log:     {log_path}")
