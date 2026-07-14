#!/usr/bin/env python3
"""Wave 1: blog.html + sitemap.xml для 15 приоритетных SEO-статей."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAVE1 = json.loads((ROOT / "tools" / "wave1_slugs.json").read_text(encoding="utf-8"))
TODAY = "2026-07-14"

spec = importlib.util.spec_from_file_location("gen", ROOT / "tools" / "generate_seo_blog.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

manifest = json.loads((ROOT / "tools" / "articles_manifest.json").read_text(encoding="utf-8"))
by_slug = {a["slug"]: a for a in manifest}
wave = [by_slug[s] for s in WAVE1 if s in by_slug]
missing = [s for s in WAVE1 if s not in by_slug]
if missing:
    raise SystemExit(f"missing slugs in manifest: {missing}")
if len(wave) != 15:
    raise SystemExit(f"expected 15 articles, got {len(wave)}")

gen.TODAY = TODAY
html = gen.render_blog(wave)
html = html.replace("Более 50 статей", "15 статей")
html = html.replace("Пsycholog", "Психолог").replace("Психolog", "Психолог").replace("психolog", "психолог")
(ROOT / "blog.html").write_text(html, encoding="utf-8")

LANDINGS = [
    ("", "weekly", "1.0"),
    ("psiholog-novosibirsk.html", "monthly", "0.9"),
    ("psiholog-online.html", "monthly", "0.9"),
    ("contacts.html", "yearly", "0.8"),
    ("blog.html", "weekly", "0.7"),
]
lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, freq, pri in LANDINGS:
    loc = gen.SITE + ("/" + path if path else "/")
    lines.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
for a in sorted(wave, key=lambda x: x["slug"]):
    lines.append(
        f"  <url><loc>{gen.SITE}/{a['slug']}.html</loc><lastmod>{a.get('date', TODAY)}</lastmod>"
        f"<changefreq>yearly</changefreq><priority>0.6</priority></url>"
    )
lines.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
(ROOT / "tools" / "wave1_manifest.json").write_text(
    json.dumps(wave, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"wave1: {len(wave)} articles, blog.html + sitemap.xml updated ({TODAY})")
