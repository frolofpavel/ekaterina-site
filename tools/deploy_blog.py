#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "tools" / "articles_manifest.json"
DEST = "frolof@5.23.51.23:/home/f/frolof/psyholog/public_html/"
KEY = "C:/Users/Pavel/.ssh/id_ed25519"

articles = json.loads(MANIFEST.read_text(encoding="utf-8"))
files = [ROOT / "blog.html", ROOT / "sitemap.xml", ROOT / "styles.css"]
files += [ROOT / f"{a['slug']}.html" for a in articles if (ROOT / f"{a['slug']}.html").exists()]

for f in files:
    if not f.exists():
        print("skip missing", f.name)
        continue
    cmd = ["scp", "-i", KEY, str(f), DEST + f.name]
    r = subprocess.run(cmd)
    if r.returncode == 0:
        print("ok", f.name)
    else:
        print("FAIL", f.name, r.returncode)

print(f"deployed {len(files)} files")
