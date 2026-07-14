#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAVE1 = json.loads((ROOT / "tools" / "wave1_slugs.json").read_text(encoding="utf-8"))
DEST = "frolof@5.23.51.23:/home/f/frolof/psyholog/public_html/"
KEY = "C:/Users/Pavel/.ssh/id_ed25519"

files = [
    ROOT / "blog.html",
    ROOT / "sitemap.xml",
    ROOT / "index.html",
    ROOT / "psiholog-online.html",
    ROOT / "styles.css",
]
files += [ROOT / f"{slug}.html" for slug in WAVE1]

ok, fail = 0, 0
for f in files:
    if not f.exists():
        print("MISSING", f.name)
        fail += 1
        continue
    r = subprocess.run(["scp", "-i", KEY, "-o", "ConnectTimeout=20", str(f), DEST + f.name])
    if r.returncode == 0:
        print("OK", f.name)
        ok += 1
    else:
        print("FAIL", f.name)
        fail += 1
print(f"done ok={ok} fail={fail}")
raise SystemExit(1 if fail else 0)
