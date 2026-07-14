import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
p = ROOT / "generate_seo_blog.py"
t = p.read_text(encoding="utf-8")

for line in [
    '    ("psiholog-novosibirsk-rayony", "Психолог в Новосибирске: очно и онлайн", "Как выбрать формат, частые запросы и запись к психологу в НСК.", "geo", "Новосибирск"),\n',
    '    ("psiholog-akademgorodok", "Психолог для жителей Академгородка", "Онлайн и очные консультации для Академгородка и научного сообщества.", "geo", "Новосибирsk"),\n',
]:
    t = t.replace(line, "")

t = t.replace("gruppovaya-i-lich\u043d\u0430\u044f-terapiya", "gruppovaya-i-lichnaya-terapiya")
t = t.replace("П\u0441ycholog", "Психолог")
t = t.replace("Сtereotipy", "Сtereotipy")
t = t.replace("психolog", "психolog")
t = t.replace("психoanалитик", "психоanалитик")

t = re.sub(
    r"\n# fix typos in tuples.*?assert len\(NEW_ARTICLES\) == 50, len\(NEW_ARTICLES\)\n",
    "\nassert len(NEW_ARTICLES) == 50, len(NEW_ARTICLES)\n",
    t,
    flags=re.S,
)

p.write_text(t, encoding="utf-8")

spec = importlib.util.spec_from_file_location("gen", p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print("articles:", len(mod.NEW_ARTICLES))
mod.main()
