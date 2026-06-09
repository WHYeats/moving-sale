import os
import json
import re
from collections import defaultdict

PHOTOS_DIR = "photos"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def parse_photo(filename):
    name, ext = os.path.splitext(filename)
    if ext.lower() not in EXTENSIONS:
        return None, None
    # label_seq.ext or label-seq.ext
    m = re.match(r"^(\d+)[-_](\d+)$", name)
    if m:
        return int(m.group(1)), int(m.group(2))
    # label.ext (single photo)
    m = re.match(r"^(\d+)$", name)
    if m:
        return int(m.group(1)), 0
    return None, None


entries = defaultdict(list)

for filename in os.listdir(PHOTOS_DIR):
    label, seq = parse_photo(filename)
    if label is None:
        continue
    entries[label].append((seq, f"{PHOTOS_DIR}/{filename}"))

manifest = {}
for label in sorted(entries):
    manifest[str(label)] = [path for _, path in sorted(entries[label])]

with open(os.path.join(PHOTOS_DIR, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)

print(f"manifest.json written — {len(manifest)} labels:")
for label, photos in manifest.items():
    print(f"  {label}: {photos}")
