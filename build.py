#!/usr/bin/env python3
"""
Builds the website into the folder dist/.

    python3 build.py                  # normal build (the same one GitHub runs)
    python3 build.py --preview        # links end in index.html, for opening the files locally
    python3 build.py --site-url URL   # public address used for search engines and link previews

Needs Python 3.9+ with PyYAML, Jinja2 and Pillow (pip install -r requirements.txt).

All texts live in content/. This script only reads them, checks them and turns them into pages.
If something is wrong in a content file, the build stops with a message that names the file and
the field, e.g.  content/erfahrung/gebrueder-fritz.yaml → start: use the format "YYYY-MM".
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

import yaml
from jinja2 import Environment, FileSystemLoader, Undefined, select_autoescape
from markupsafe import Markup, escape
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"
CACHE = ROOT / ".cache"
OG_FONTS = ROOT / "scripts" / "fonts"

IMAGE_WIDTHS = (480, 960, 1600)
RASTER = {".jpg", ".jpeg", ".png", ".webp"}
SOURCES = ("zeugnis", "screenshot", "linkedin", "zertifikat", "artikel", "forschung", "eigen")
PROOF_TYPES = ("zeugnis", "zertifikat", "forschung", "artikel")

MONTHS = {
    "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "it": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"],
}


# ---------------------------------------------------------------------------
# Reading and checking the content
# ---------------------------------------------------------------------------

class ContentError(Exception):
    pass


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_yaml(path: Path):
    try:
        with path.open(encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except yaml.YAMLError as error:
        raise ContentError(f"{rel(path)}: the file is not valid YAML.\n{error}\nTip: check quotes and indentation (2 spaces).")
    if data is None:
        raise ContentError(f"{rel(path)}: the file is empty.")
    return data


class Checker:
    """Collects all problems of one file and reports them together."""

    def __init__(self, path: Path, languages: list[str]):
        self.path = path
        self.languages = languages
        self.problems: list[str] = []

    def fail(self, field: str, message: str):
        self.problems.append(f"{rel(self.path)} → {field}: {message}")

    def text(self, data, field: str, required: bool = True):
        value = data.get(field) if isinstance(data, dict) else None
        if value is None or value == "":
            if required:
                self.fail(field, "missing text.")
            return
        self.text_value(value, field)

    def text_value(self, value, field: str):
        if isinstance(value, str):
            return
        if isinstance(value, dict):
            if "de" not in value or not isinstance(value.get("de"), str) or not value["de"].strip():
                self.fail(field, 'write the German text as  de: "…"  (en and it are optional).')
            for key, item in value.items():
                if key not in self.languages:
                    self.fail(field, f'unknown language "{key}" (use {", ".join(self.languages)}).')
                elif not isinstance(item, str):
                    self.fail(f"{field}.{key}", "must be text in quotes.")
            return
        self.fail(field, 'must be text in quotes, or one text per language (de / en / it).')

    def month(self, data, field: str, required: bool = True):
        value = data.get(field)
        if value is None:
            if required:
                self.fail(field, 'missing. Use the format "YYYY-MM", e.g. "2025-08".')
            return
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}", value):
            self.fail(field, 'use the format "YYYY-MM" in quotes, e.g. "2025-08".')

    def date(self, data, field: str):
        value = data.get(field)
        if isinstance(value, str) and re.fullmatch(r"\d{4}(-\d{2}){0,2}", value):
            return
        self.fail(field, 'use the format "YYYY-MM-DD" in quotes, e.g. "2026-06-30".')

    def number(self, data, field: str):
        if not isinstance(data.get(field), (int, float)):
            self.fail(field, "must be a number, e.g. 3.")

    def static_file(self, value, field: str):
        if not isinstance(value, str) or not value.startswith("/"):
            self.fail(field, 'write the path of a file in static/, starting with "/", e.g. "/images/…" or "/pdf/…".')
            return
        if not (STATIC / value.lstrip("/")).is_file():
            self.fail(field, f"file not found: static{value}")

    def image(self, value, field: str, required: bool = True):
        if value is None:
            if required:
                self.fail(field, "missing image.")
            return
        if isinstance(value, str):
            self.static_file(value, field)
            return
        if not isinstance(value, dict) or "src" not in value:
            self.fail(field, 'write  src: "/images/…"  and optionally alt, caption, position.')
            return
        self.static_file(value["src"], f"{field}.src")
        for key in ("alt", "caption"):
            if key in value:
                self.text_value(value[key], f"{field}.{key}")

    def url(self, value, field: str):
        if not isinstance(value, str) or not re.match(r"^(https?://|mailto:)", value):
            self.fail(field, 'must be a full address starting with "https://".')

    def link_or_file(self, value, field: str):
        if isinstance(value, str) and value.startswith("/"):
            self.static_file(value, field)
        else:
            self.url(value, field)

    def language_blocks(self, data, required_fields: list[str], optional_fields: list[str]):
        block = data.get("de")
        if not isinstance(block, dict):
            self.fail("de", "the German block (de:) is missing.")
            return
        for field in required_fields:
            if not block.get(field):
                self.fail(f"de.{field}", "missing.")
        allowed = set(required_fields) | set(optional_fields)
        for lang in self.languages:
            if lang == "de" or lang not in data:
                continue
            if not isinstance(data[lang], dict):
                self.fail(lang, f"must be a block with the same fields as de.")
                continue
            for key in data[lang]:
                if key not in allowed:
                    self.fail(f"{lang}.{key}", "unknown field.")
        for key in block:
            if key not in allowed:
                self.fail(f"de.{key}", "unknown field.")

    def done(self):
        if self.problems:
            raise ContentError("\n".join(self.problems))


def load_collection(folder: str) -> list[dict]:
    directory = CONTENT / folder
    entries = []
    for path in sorted(directory.glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        data = load_yaml(path)
        if not isinstance(data, dict):
            raise ContentError(f"{rel(path)}: the file must contain fields (name: value).")
        data["id"] = path.stem
        data["_path"] = path
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", path.stem):
            raise ContentError(f"{rel(path)}: use only lowercase letters, numbers and hyphens in the file name (it becomes the address).")
        entries.append(data)
    return entries


def load_content(site: dict) -> dict:
    languages = site["languages"]
    areas = site["areas"]
    problems: list[str] = []

    def guard(check: Checker):
        try:
            check.done()
        except ContentError as error:
            problems.append(str(error))

    ui = load_yaml(CONTENT / "ui.yaml")
    for lang in languages:
        if lang not in ui:
            problems.append(f"content/ui.yaml → {lang}: the block for this language is missing.")

    home = load_yaml(CONTENT / "home.yaml")
    proofs = load_collection("nachweise")
    posts = load_collection("linkedin")
    works = load_collection("erfahrung")
    education = load_collection("ausbildung")
    references = load_collection("referenzen")

    proof_ids = {p["id"] for p in proofs}
    post_ids = {p["id"] for p in posts}
    work_ids = {w["id"] for w in works}

    # home.yaml
    c = Checker(CONTENT / "home.yaml", languages)
    c.text(home, "name")
    contact = home.get("contact") or {}
    if not isinstance(contact.get("email"), str) or "@" not in contact.get("email", ""):
        c.fail("contact.email", "write a valid e-mail address.")
    c.url(contact.get("linkedin"), "contact.linkedin")
    if contact.get("cv"):
        c.static_file(contact["cv"], "contact.cv")
    c.image(home.get("portrait"), "portrait")
    for key in ("title", "description"):
        c.text(home.get("seo") or {}, key)
    c.text(home.get("hero") or {}, "lead")
    for i, fact in enumerate(home.get("facts") or []):
        c.text(fact, "label")
        c.text(fact, "value")
    focus = home.get("focus") or {}
    c.text(focus, "intro")
    seen_areas = []
    for i, area in enumerate(focus.get("areas") or []):
        name = f"focus.areas[{i + 1}]"
        if area.get("id") not in areas:
            c.fail(f"{name}.id", f'must be one of {", ".join(areas)}.')
        seen_areas.append(area.get("id"))
        for key in ("word", "title", "intro"):
            c.text(area, key)
        for j, item in enumerate(area.get("evidence") or []):
            iname = f"{name}.evidence[{j + 1}]"
            c.text(item, "text")
            if item.get("work") and item["work"] not in work_ids:
                c.fail(f"{iname}.work", f'no experience called "{item["work"]}" in content/erfahrung/.')
            if not item.get("work"):
                c.text(item, "org")
            if item.get("source") not in SOURCES:
                c.fail(f"{iname}.source", f'must be one of {", ".join(SOURCES)}.')
            if item.get("href"):
                c.link_or_file(item["href"], f"{iname}.href")
        roles = area.get("roles") or {}
        if not isinstance(roles, dict) or not isinstance(roles.get("de"), list):
            c.fail(f"{name}.roles", "write the roles as lists per language: de: [\"…\", \"…\"].")
    if sorted(seen_areas) != sorted(areas):
        c.fail("focus.areas", f'needs exactly one block for each area: {", ".join(areas)}.')
    for key in ("experience", "references", "education", "proof", "contact"):
        c.text(home.get("sections") or {}, key)
    skills = home.get("skills") or {}
    for i, entry in enumerate(skills.get("languages") or []):
        c.text(entry, "name")
        c.text(entry, "level")
    for i, group in enumerate(skills.get("tool_groups") or []):
        c.text(group, "name")
        for j, item in enumerate(group.get("items") or []):
            c.text_value(item, f"skills.tool_groups[{i + 1}].items[{j + 1}]")
    for i, item in enumerate(skills.get("interests") or []):
        c.text_value(item, f"skills.interests[{i + 1}]")
    guard(c)

    # experiences
    work_fields = ["title", "role", "summary", "context", "contribution"]
    work_optional = ["tasks", "outputs", "highlights", "transfer", "learnings"]
    for work in works:
        c = Checker(work["_path"], languages)
        c.number(work, "order")
        c.text(work, "company")
        c.text(work, "location")
        c.month(work, "start")
        c.month(work, "end", required=False)
        if work.get("website"):
            c.url(work["website"], "website")
        work_areas = work.get("areas") or []
        if not work_areas or any(a not in areas for a in work_areas):
            c.fail("areas", f'list one or more of: {", ".join(areas)}.')
        c.image(work.get("cover"), "cover")
        for i, image in enumerate(work.get("gallery") or []):
            c.image(image, f"gallery[{i + 1}]")
        for ref in work.get("documents") or []:
            if ref not in proof_ids:
                c.fail("documents", f'no document called "{ref}" in content/nachweise/.')
        for ref in work.get("posts") or []:
            if ref not in post_ids:
                c.fail("posts", f'no post called "{ref}" in content/linkedin/.')
        for i, link in enumerate(work.get("links") or []):
            c.text(link, "label")
            c.url(link.get("url"), f"links[{i + 1}].url")
        c.language_blocks(work, work_fields, work_optional)
        for lang in languages:
            block = work.get(lang) or {}
            transfer = block.get("transfer") or {}
            for key in transfer:
                if key not in areas:
                    c.fail(f"{lang}.transfer.{key}", f'use one of {", ".join(areas)}.')
        guard(c)

    # education
    for entry in education:
        c = Checker(entry["_path"], languages)
        c.number(entry, "order")
        c.text(entry, "institution")
        c.text(entry, "location")
        c.month(entry, "start")
        c.month(entry, "end", required=False)
        c.image(entry.get("image"), "image", required=False)
        c.language_blocks(entry, ["title", "explain"], ["focus", "points"])
        guard(c)

    # documents
    for entry in proofs:
        c = Checker(entry["_path"], languages)
        c.number(entry, "order")
        if entry.get("type") not in PROOF_TYPES:
            c.fail("type", f'must be one of {", ".join(PROOF_TYPES)}.')
        c.date(entry, "date")
        c.text(entry, "source")
        if entry.get("pdf"):
            c.static_file(entry["pdf"], "pdf")
        if entry.get("url"):
            c.url(entry["url"], "url")
        if not entry.get("pdf") and not entry.get("url"):
            c.fail("pdf", 'add  pdf: "/pdf/…"  or  url: "https://…".')
        c.image(entry.get("image"), "image", required=False)
        c.language_blocks(entry, ["title", "summary"], [])
        guard(c)

    # posts
    for entry in posts:
        c = Checker(entry["_path"], languages)
        c.number(entry, "order")
        c.date(entry, "date")
        c.url(entry.get("url"), "url")
        c.image(entry.get("image"), "image")
        c.language_blocks(entry, ["title", "excerpt"], [])
        guard(c)

    # references
    featured = 0
    for entry in references:
        c = Checker(entry["_path"], languages)
        c.number(entry, "order")
        c.text(entry, "name")
        c.text(entry, "role")
        c.text(entry, "source")
        c.date(entry, "date")
        c.image(entry.get("image"), "image", required=False)
        if entry.get("pdf"):
            c.static_file(entry["pdf"], "pdf")
        if entry.get("url"):
            c.url(entry["url"], "url")
        featured += 1 if entry.get("featured") else 0
        c.language_blocks(entry, ["quote"], ["full"])
        guard(c)
    if featured > 1:
        problems.append("content/referenzen: only one reference can have  featured: true.")

    if problems:
        raise ContentError("\n".join(problems))

    by_order = lambda item: (item.get("order", 0), item["id"])
    return {
        "ui": ui,
        "home": home,
        "works": sorted(works, key=by_order),
        "education": sorted(education, key=by_order),
        "proofs": sorted(proofs, key=by_order),
        "posts": sorted(posts, key=by_order),
        "references": sorted(references, key=by_order),
    }


# ---------------------------------------------------------------------------
# Language helpers
# ---------------------------------------------------------------------------

def tr(value, lang: str) -> str:
    """Picks one language of a text field (falls back to German)."""
    if value is None:
        return ""
    if isinstance(value, dict):
        return value.get(lang) or value.get("de") or ""
    return str(value)


def localized(entry: dict, lang: str) -> dict:
    """German block merged with the block of another language (missing fields fall back to German)."""
    merged = dict(entry.get("de") or {})
    if lang != "de":
        for key, value in (entry.get(lang) or {}).items():
            if value in (None, "", [], {}):
                continue
            merged[key] = value
    return merged


def format_month(value: str) -> str:
    year, month = value.split("-")
    return f"{month}/{year}"


def format_period(start: str, end: str | None, ui: dict) -> str:
    if not end:
        return f'{ui["period"]["since"]} {format_month(start)}'
    return f"{format_month(start)} – {format_month(end)}"


def format_date(value: str, lang: str) -> str:
    parts = [int(p) for p in value.split("-")]
    if len(parts) == 1:
        return str(parts[0])
    month = MONTHS[lang][parts[1] - 1]
    if len(parts) == 2:
        return f"{month} {parts[0]}"
    if lang == "de":
        return f"{parts[2]}. {month} {parts[0]}"
    return f"{parts[2]} {month} {parts[0]}"


def paragraphs(value: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", value or "") if p.strip()]


# ---------------------------------------------------------------------------
# Images: smaller WebP versions + social preview images
# ---------------------------------------------------------------------------

def build_images(dist: Path) -> dict:
    manifest: dict[str, dict] = {}
    cache_dir = CACHE / "img"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for source in sorted((STATIC / "images").rglob("*")):
        if source.suffix.lower() not in RASTER or not source.is_file():
            continue
        public = "/" + source.relative_to(STATIC).as_posix()
        try:
            with Image.open(source) as image:
                image = ImageOps.exif_transpose(image)
                width, height = image.size
                variants = []
                for target in IMAGE_WIDTHS:
                    if target >= width * 0.9:
                        continue
                    stem = source.relative_to(STATIC / "images").with_suffix("").as_posix()
                    out_rel = f"generated/img/{stem}-{target}.webp"
                    key = hashlib.sha1(f"{public}:{source.stat().st_mtime_ns}:{target}".encode()).hexdigest()
                    cached = cache_dir / f"{key}.webp"
                    if not cached.exists():
                        resized = image.convert("RGBA" if image.mode in ("RGBA", "LA", "P") else "RGB")
                        resized = resized.resize((target, round(height * target / width)), Image.LANCZOS)
                        resized.save(cached, "WEBP", quality=76, method=6)
                    out = dist / out_rel
                    out.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(cached, out)
                    variants.append({"w": target, "src": "/" + out_rel})
                manifest[public] = {"width": width, "height": height, "variants": variants}
        except Exception as error:  # an image problem never stops the build
            print(f"[images] skipped {public}: {error}")
    return manifest


def og_font(bold: bool, size: int):
    name = "texgyreadventor-bold.otf" if bold else "texgyreadventor-regular.otf"
    try:
        return ImageFont.truetype(str(OG_FONTS / name), size)
    except OSError:
        return ImageFont.load_default()


def cover_crop(image: Image.Image, width: int, height: int, position: str | None) -> Image.Image:
    named = {"left": 0.0, "top": 0.0, "center": 0.5, "right": 1.0, "bottom": 1.0}
    values = []
    tokens = (position or "center center").lower().split()
    for token in tokens:
        if token in named:
            values.append(named[token])
        elif token.endswith("%"):
            try:
                values.append(float(token[:-1]) / 100)
            except ValueError:
                values.append(0.5)
    x, y = (values + [0.5, 0.5])[:2]
    if tokens and tokens[0] in ("top", "bottom"):
        x, y = y, x
    return ImageOps.fit(image, (width, height), Image.LANCZOS, centering=(min(max(x, 0), 1), min(max(y, 0), 1)))


def build_og_images(dist: Path, data: dict, site: dict) -> dict:
    """1200×630 images for link previews (LinkedIn, WhatsApp, e-mail)."""
    out_dir = dist / "generated" / "og"
    out_dir.mkdir(parents=True, exist_ok=True)
    home = data["home"]
    result = {}
    sand, caramel, ink, ochre, mist = (241, 226, 206), (196, 163, 129), (30, 27, 22), (126, 93, 43), (238, 242, 241)
    W, H = 1200, 630

    def base_canvas():
        canvas = Image.new("RGB", (W, H), mist)
        column = Image.new("RGB", (430, H))
        draw = ImageDraw.Draw(column)
        for y in range(H):
            t = y / (H - 1)
            draw.line([(0, y), (430, y)], fill=tuple(round(caramel[i] + (sand[i] - caramel[i]) * t) for i in range(3)))
        canvas.paste(column, (0, 0))
        return canvas

    portrait_info = home["portrait"]
    try:
        with Image.open(STATIC / portrait_info["src"].lstrip("/")) as portrait:
            portrait = cover_crop(portrait.convert("RGB"), 320, 400, portrait_info.get("position"))
    except OSError:
        portrait = None

    for lang in site["languages"]:
        canvas = base_canvas()
        draw = ImageDraw.Draw(canvas)
        if portrait is not None:
            frame = Image.new("RGB", (336, 416), (255, 255, 255))
            canvas.paste(frame, (47, 107))
            canvas.paste(portrait, (55, 115))
        draw.text((500, 120), tr(home["name"], lang).upper(), font=og_font(True, 50), fill=ink)
        y = 210
        for area in home["focus"]["areas"]:
            draw.text((500, y), tr(area["word"], lang) + ".", font=og_font(True, 64), fill=ink)
            draw.text((500, y + 74), tr(area["title"], lang), font=og_font(False, 22), fill=ochre)
            y += 118
        path = out_dir / f"home-{lang}.jpg"
        canvas.save(path, "JPEG", quality=86, optimize=True)
        result[f"home-{lang}"] = "/" + path.relative_to(dist).as_posix()

    for work in data["works"]:
        cover = work["cover"] if isinstance(work["cover"], dict) else {"src": work["cover"]}
        try:
            with Image.open(STATIC / cover["src"].lstrip("/")) as image:
                photo = cover_crop(image.convert("RGB"), W, 470, cover.get("position"))
        except OSError:
            continue
        for lang in site["languages"]:
            canvas = Image.new("RGB", (W, H), sand)
            canvas.paste(photo, (0, 0))
            draw = ImageDraw.Draw(canvas)
            draw.rectangle([0, 470, W, H], fill=sand)
            draw.text((48, 498), tr(work["company"], lang), font=og_font(True, 44), fill=ink)
            draw.text((48, 562), f'{tr(home["name"], lang)}, {localized(work, lang)["role"]}', font=og_font(False, 24), fill=ochre)
            path = out_dir / f'{work["id"]}-{lang}.jpg'
            canvas.save(path, "JPEG", quality=84, optimize=True)
            result[f'{work["id"]}-{lang}'] = "/" + path.relative_to(dist).as_posix()
    return result


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

class Page:
    """Knows where a page is written, so every link can be relative (works under any base path)."""

    def __init__(self, path: str, site_url: str, preview: bool, manifest: dict):
        self.path = path  # e.g. "de/erfahrung/gebrueder-fritz/index.html"
        self.depth = path.count("/")
        self.site_url = site_url
        self.preview = preview
        self.manifest = manifest

    def url(self, target: str) -> str:
        """Link to a page or file, given relative to the site root ("de/", "images/x.webp", "/pdf/a.pdf")."""
        if re.match(r"^(https?:|mailto:|tel:|#)", target):
            return target
        target = target.lstrip("/")
        hash_part = ""
        if "#" in target:
            target, hash_part = target.split("#", 1)
            hash_part = "#" + hash_part
        query = ""
        if "?" in target:
            target, query = target.split("?", 1)
            query = "?" + query
        if (target == "" or target.endswith("/")) and self.preview:
            target += "index.html"
        prefix = "../" * self.depth
        result = prefix + target
        if result == "":
            result = "./"
        return quote(result, safe="/._-~%:#?=&") + query + hash_part

    def absolute(self, target: str) -> str:
        if re.match(r"^https?:", target):
            return target
        return self.site_url + target.lstrip("/")

    def img(self, src: str, alt: str = "", sizes: str = "100vw", loading: str = "lazy", position: str | None = None,
            css_class: str = "", fetchpriority: str | None = None) -> Markup:
        info = self.manifest.get(src)
        attrs = [f'src="{escape(self.url(src))}"', f'alt="{escape(alt)}"']
        if info:
            attrs.append(f'width="{info["width"]}" height="{info["height"]}"')
            if info["variants"]:
                srcset = ", ".join([f'{self.url(v["src"])} {v["w"]}w' for v in info["variants"]] + [f'{self.url(src)} {info["width"]}w'])
                attrs.append(f'srcset="{escape(srcset)}" sizes="{escape(sizes)}"')
        attrs.append(f'loading="{loading}" decoding="async"')
        if fetchpriority:
            attrs.append(f'fetchpriority="{fetchpriority}"')
        if css_class:
            attrs.append(f'class="{escape(css_class)}"')
        if position:
            attrs.append(f'style="object-position: {escape(position)}"')
        return Markup(f"<img {' '.join(attrs)}>")


def person_jsonld(home: dict, data: dict, page: "Page", lang: str) -> dict:
    """Structured data for search engines (schema.org Person)."""
    languages = {"Italienisch": "it", "Deutsch": "de", "Englisch": "en", "Französisch": "fr"}
    known = [languages.get(tr(item["name"], "de"), tr(item["name"], "de")) for item in home["skills"]["languages"]]
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": tr(home["name"], lang),
        "url": page.absolute(f"{lang}/"),
        "image": page.absolute(home["portrait"]["src"]),
        "email": f'mailto:{home["contact"]["email"]}',
        "sameAs": [home["contact"]["linkedin"]],
        "address": {"@type": "PostalAddress", "addressCountry": "CH"},
        "knowsLanguage": known,
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": tr(entry["institution"], lang)} for entry in data["education"]],
        "description": tr(home["seo"]["description"], lang),
    }


def write(dist: Path, path: str, html: str):
    target = dist / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


def build(site_url: str, preview: bool, out: Path) -> None:
    site = load_yaml(ROOT / "site.yaml")
    data = load_content(site)
    languages = site["languages"]
    segments = site["segments"]
    if not site_url.endswith("/"):
        site_url += "/"

    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(STATIC, out)

    manifest = build_images(out)
    og = build_og_images(out, data, site)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=Undefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["tr"] = tr
    env.filters["month"] = format_month
    env.filters["paragraphs"] = paragraphs
    env.globals["localized"] = localized
    env.globals["format_period"] = format_period
    env.globals["format_date"] = format_date

    home = data["home"]
    works = data["works"]
    proofs_by_id = {p["id"]: p for p in data["proofs"]}
    posts_by_id = {p["id"]: p for p in data["posts"]}
    works_by_id = {w["id"]: w for w in works}
    version = hashlib.sha1((STATIC / "css" / "site.css").read_bytes() + (STATIC / "js" / "site.js").read_bytes()).hexdigest()[:8]

    def home_path(lang):
        return f"{lang}/"

    def work_path(lang, work_id):
        return f"{lang}/{segments[lang]}/{work_id}/"

    common = {
        "site": site,
        "languages": languages,
        "home": home,
        "works": works,
        "works_by_id": works_by_id,
        "education": data["education"],
        "proofs": data["proofs"],
        "proofs_by_id": proofs_by_id,
        "posts": data["posts"],
        "posts_by_id": posts_by_id,
        "references": data["references"],
        "all_ui": data["ui"],
        "segments": segments,
        "work_path": work_path,
        "home_path": home_path,
        "version": version,
        "proof_types": PROOF_TYPES,
        "areas_by_id": {area["id"]: area for area in home["focus"]["areas"]},
        "build_year": datetime.date.today().year,
        "person_jsonld": lambda page, lang: person_jsonld(home, data, page, lang),
    }

    sitemap = []

    # Start pages
    for lang in languages:
        targets = [f"{lang}/index.html"] + (["index.html"] if lang == languages[0] else [])
        for target in targets:
            page = Page(target, site_url, preview, manifest)
            html = env.get_template("home.html").render(
                **common,
                lang=lang,
                ui=data["ui"][lang],
                page=page,
                canonical=home_path(lang),
                alternates={l: home_path(l) for l in languages},
                og_image=og.get(f"home-{lang}", "/images/profile/luca-portrait.webp"),
            )
            write(out, target, html)
        sitemap.append(home_path(lang))

    # Experience pages
    for index, work in enumerate(works):
        previous_work = works[index - 1] if index > 0 else None
        next_work = works[index + 1] if index + 1 < len(works) else None
        for lang in languages:
            target = work_path(lang, work["id"]) + "index.html"
            page = Page(target, site_url, preview, manifest)
            html = env.get_template("station.html").render(
                **common,
                lang=lang,
                ui=data["ui"][lang],
                page=page,
                work=work,
                text=localized(work, lang),
                previous_work=previous_work,
                next_work=next_work,
                canonical=work_path(lang, work["id"]),
                alternates={l: work_path(l, work["id"]) for l in languages},
                og_image=og.get(f'{work["id"]}-{lang}', og.get(f"home-{lang}", "")),
            )
            write(out, target, html)
            sitemap.append(work_path(lang, work["id"]))

    # 404
    lang = languages[0]
    page = Page("404.html", site_url, preview, manifest)
    html = env.get_template("404.html").render(
        **common, lang=lang, ui=data["ui"][lang], page=page, canonical=None,
        alternates={l: home_path(l) for l in languages}, og_image=og.get(f"home-{lang}", ""),
    )
    write(out, "404.html", html)

    # sitemap.xml and robots.txt
    urls = "\n".join(f"  <url><loc>{escape(site_url + path)}</loc></url>" for path in sitemap)
    write(out, "sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    write(out, "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {site_url}sitemap.xml\n")
    write(out, ".nojekyll", "")

    pages = len(sitemap) + 2
    print(f"Built {pages} pages into {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out} "
          f"({len(manifest)} images, {len(og)} preview images){' – preview links' if preview else ''}.")


def main():
    parser = argparse.ArgumentParser(description="Build the portfolio website into dist/.")
    parser.add_argument("--site-url", default=None, help="public address, e.g. https://invernizziluca.github.io/profile/")
    parser.add_argument("--preview", action="store_true", help="link to index.html files (for opening the pages locally)")
    parser.add_argument("--out", default=str(ROOT / "dist"), help="output folder (default: dist)")
    args = parser.parse_args()
    site = load_yaml(ROOT / "site.yaml")
    try:
        build(args.site_url or site["site_url"], args.preview, Path(args.out).resolve())
    except ContentError as error:
        print("\nThe site was NOT built. Please fix the following:\n", file=sys.stderr)
        print(str(error), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
