"""Télécharge une couverture pour chaque livre de books.json et mahe.json.

Lancé par GitHub Actions (.github/workflows/covers.yml). Les images sont
enregistrées dans covers/<id>.jpg et listées dans covers/index.json, que les
pages lisent en premier. Un livre déjà couvert n'est jamais retéléchargé.
"""
import io, json, os, re, sys, time, urllib.parse
import requests
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "covers")
INDEX = os.path.join(OUT, "index.json")
UA = {"User-Agent": "Mozilla/5.0 (MyBookWishlist cover fetcher)"}

def load_books():
    books = []
    for name in ("books.json", "mahe.json"):
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            continue
        data = json.load(open(path, encoding="utf-8"))
        books += data if isinstance(data, list) else data.get("books", [])
    return [b for b in books if not b.get("noCover")]

def isbn10(i):
    if not i or len(i) != 13 or not i.startswith("978"):
        return ""
    c = i[3:12]
    t = sum((10 - k) * int(c[k]) for k in range(9))
    d = (11 - t % 11) % 11
    return c + ("X" if d == 10 else str(d))

def gbooks(q):
    try:
        r = requests.get("https://www.googleapis.com/books/v1/volumes",
                         params={"q": q, "maxResults": 10}, headers=UA, timeout=20)
        for it in r.json().get("items", []):
            links = it.get("volumeInfo", {}).get("imageLinks", {})
            u = links.get("thumbnail") or links.get("smallThumbnail")
            if u:
                return u.replace("http://", "https://").replace("&edge=curl", "")
    except Exception:
        pass
    return ""

def olsearch(q):
    try:
        r = requests.get("https://openlibrary.org/search.json",
                         params={"q": q, "limit": 5, "fields": "cover_i"}, headers=UA, timeout=20)
        for d in r.json().get("docs", []):
            if d.get("cover_i"):
                return f"https://covers.openlibrary.org/b/id/{d['cover_i']}-L.jpg"
    except Exception:
        pass
    return ""

def og_image(page):
    try:
        r = requests.get(page, headers=UA, timeout=25, allow_redirects=True)
        m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', r.text) or \
            re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', r.text)
        return m.group(1) if m else ""
    except Exception:
        return ""

def candidates(b):
    isbn = b.get("isbn") or ""
    urls = list(b.get("covers") or [])
    if b.get("cover"):
        urls.append(re.sub(r"fife=w\d+-h\d+", "fife=w600-h900", b["cover"]))
    if isbn10(isbn):
        urls.append(f"https://images-na.ssl-images-amazon.com/images/P/{isbn10(isbn)}.01.LZZZZZZZ.jpg")
    if isbn:
        urls.append(f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg?default=false")
        urls.append(f"https://media.e.leclerc/{isbn}_1?fit=fit&fmt=jpg&qlt=85&wid=600&hei=600")
        urls.append(f"https://ssr.fidelio.ca/Public/img/catalog/cover/{isbn}.jpg")
        urls.append(("page", f"https://www.decitre.fr/rechercher/result?q={isbn}"))
        urls.append(("page", f"https://www.placedeslibraires.fr/livre/{isbn}"))
        urls.append(("lazy", f"isbn:{isbn}"))
    q = b.get("coverQuery") or f"{b.get('title','')} {(b.get('authors') or '').split(',')[0]}"
    urls.append(("lazy", q))
    urls.append(("ol", q))
    return urls

# empreintes d'images génériques (« visuel à venir »…) à refuser
BAD_HASHES = ["0000000011001000110101001001010011011100111100001100110000000000"]

def dhash(im, n=8):
    g = im.convert("L").resize((n + 1, n))
    px = list(g.getdata())
    return "".join("1" if px[r*(n+1)+c] > px[r*(n+1)+c+1] else "0" for r in range(n) for c in range(n))

def is_placeholder(im):
    h = dhash(im)
    return any(sum(a != b for a, b in zip(h, bad)) <= 8 for bad in BAD_HASHES)

def trim(im):
    """Retire les bandes unies (noires ou blanches) autour de la couverture."""
    corner = im.getpixel((0, 0))
    if sum(corner) / 3 > 40:  # seulement les bandes noires (format « letterbox »)
        return im
    bg = Image.new(im.mode, im.size, corner)
    diff = ImageChops.add(ImageChops.difference(im, bg), ImageChops.difference(im, bg), 2.0, -30)
    box = diff.getbbox()
    if box and (box[2] - box[0]) > im.size[0] * 0.4 and (box[3] - box[1]) > im.size[1] * 0.4:
        return im.crop(box)
    return im

def fetch_image(url):
    try:
        r = requests.get(url, headers=UA, timeout=25)
        if r.status_code != 200 or len(r.content) < 1500:
            return None
        im = Image.open(io.BytesIO(r.content))
        im.load()
        w, h = im.size
        # rejette les pixels vides, les vignettes minuscules et les formats non « livre »
        if w < 80 or h < 80 or h < w * 0.5:
            return None
        im = trim(im.convert("RGB"))
        w, h = im.size
        if is_placeholder(im):
            return None
        # rejette les images quasi unies (pages « image non disponible »)
        small = im.resize((24, 24))
        px = list(small.getdata())
        spread = max(max(c) for c in zip(*px)) - min(min(c) for c in zip(*px))
        if spread < 40:
            return None
        if w > 400:
            im = im.resize((400, round(h * 400 / w)), Image.LANCZOS)
        out = io.BytesIO()
        im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
        return out.getvalue()
    except Exception:
        return None

def safe(id_):
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", id_)[:80]

def main():
    os.makedirs(OUT, exist_ok=True)
    index = json.load(open(INDEX)) if os.path.exists(INDEX) else {}
    books = load_books()
    ids = {b["id"] for b in books}
    for bid in [k for k in index if k not in ids]:
        path = os.path.join(ROOT, index.pop(bid))
        if os.path.exists(path):
            os.remove(path)
    for bid, rel in list(index.items()):
        path = os.path.join(ROOT, rel)
        try:
            if is_placeholder(Image.open(path)):
                os.remove(path); index.pop(bid)
        except Exception:
            index.pop(bid, None)
    added, missing = [], []
    for b in books:
        bid = b["id"]
        if bid in index and os.path.exists(os.path.join(ROOT, index[bid])):
            continue
        data = None
        for c in candidates(b):
            url = c
            if isinstance(c, tuple):
                url = gbooks(c[1]) if c[0] == "lazy" else olsearch(c[1]) if c[0] == "ol" else og_image(c[1])
                time.sleep(0.4)
            if not url:
                continue
            data = fetch_image(url)
            if data:
                break
        if data:
            rel = f"covers/{safe(bid)}.jpg"
            open(os.path.join(ROOT, rel), "wb").write(data)
            index[bid] = rel
            added.append(b["title"])
        else:
            missing.append(b["title"])
    json.dump(dict(sorted(index.items())), open(INDEX, "w"), ensure_ascii=False, indent=0)
    print(f"Ajoutées : {len(added)}")
    for t in added:
        print("  +", t)
    print(f"Sans couverture : {len(missing)}")
    for t in missing:
        print("  -", t)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"### Couvertures\n\nAjoutées : {len(added)}\n\nSans couverture : {len(missing)}\n\n")
            f.writelines(f"- {t}\n" for t in missing)

if __name__ == "__main__":
    main()
