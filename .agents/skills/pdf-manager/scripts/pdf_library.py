"""Portable PDF/Markdown/assets layout and an optional four-column ledger."""

from __future__ import annotations

import csv
import html
import io
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from pdf_markdown import rewrite_links

INDEX_FIELDS = ("id", "name", "keywords", "revised")
FRONT_FIELDS = ("stem", "id", "title", "keywords", "abstract", "revised", "source", "parser")
FRONT_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)
ARXIV_PREFIX = re.compile(r"^(arxiv-(?:\d{4}\.\d{4,5}|[a-z][a-z0-9.-]*-\d{7})(?:v[1-9]\d*)?)(?=\.|$)", re.I)
ASSET_KIND = r"(?:fig|chart|table|eq|img)\d+[a-z]?(?:-\d+)?"


class LibraryError(ValueError):
    pass


def clean_name(value: str) -> str:
    """Clean a filename component, preserving its readable case and Unicode."""
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', ".", value.strip())
    value = re.sub(r"\.{2,}", ".", value).strip(". ")
    if not value:
        raise LibraryError("文件名不能为空。")
    if re.match(r"^(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", value, re.I):
        value = "_" + value
    return value


def name_stem(value: str) -> str:
    if value.lower().endswith(".pdf"):
        return value[:-4]
    if value.lower().endswith(".md"):
        return value[:-3]
    return value


def identity_from_name(value: str) -> str | None:
    match = ARXIV_PREFIX.match(value)
    return match.group(1) if match else None


def stem_of(row: dict) -> str:
    ident, name = row.get("id") or "", row.get("name") or ""
    return f"{ident}.{name}" if ident and name else ident or name


def split_keywords(value) -> list[str]:
    values = value if isinstance(value, list) else re.split(r"[;,]", value or "")
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


def read_markdown(path: Path) -> tuple[dict, str]:
    if not path.is_file():
        return {}, ""
    text = path.read_text(encoding="utf-8-sig")
    match = FRONT_RE.match(text)
    if not match:
        return {}, text
    return _parse_front_matter(match.group(1)), text[match.end():].lstrip("\r\n")


def _parse_front_matter(text: str) -> dict:
    fields = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if not key or key.startswith("#"):
            continue
        try:
            parsed = json.loads(value)
        except (ValueError, TypeError):
            if value.startswith("[") and value.endswith("]"):
                parsed = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
            elif value.startswith("'") and value.endswith("'"):
                parsed = value[1:-1].replace("''", "'")
            else:
                parsed = None if value.lower() in ("null", "none", "~", "") else value
        fields[key] = parsed
    return fields


def read_front_matter(path: Path) -> dict:
    """Identity/index operations need only the register, not the paper body."""
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8-sig") as handle:
        if handle.readline().strip() != "---":
            return {}
        lines = []
        for line in handle:
            if line.strip() == "---":
                return _parse_front_matter("".join(lines))
            lines.append(line)
    return {}


def render_markdown(fields: dict, body: str) -> str:
    keys = list(FRONT_FIELDS) + [k for k in fields if k not in FRONT_FIELDS]
    lines = ["---"]
    for key in keys:
        if key == "title" and key not in fields:
            continue
        value = fields.get(key)
        if key == "keywords":
            value = split_keywords(value)
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    return "\n".join(lines) + "\n---\n\n" + body.rstrip() + "\n"


def atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".pdf-manager-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_text(path: Path, text: str) -> None:
    atomic_bytes(path, text.encode("utf-8"))


def asset_references(text: str) -> list[str]:
    paths = []
    def collect(value):
        parsed = urlsplit(html.unescape(value))
        path = unquote(parsed.path)
        if not parsed.scheme and not parsed.netloc and path.startswith("../assets/"):
            name = path.removeprefix("../assets/")
            if name and name not in paths:
                paths.append(name)
        return None
    rewrite_links(text, collect)
    return paths


def rewrite_asset_names(text: str, mapping: dict[str, str]) -> str:
    def replace(raw):
        parsed = urlsplit(html.unescape(raw))
        path = unquote(parsed.path)
        if parsed.scheme or parsed.netloc or not path.startswith("../assets/"):
            return None
        old = path.removeprefix("../assets/")
        if old not in mapping:
            return None
        new = "../assets/" + quote(mapping[old], safe="-._~")
        if parsed.query:
            new += "?" + parsed.query
        if parsed.fragment:
            new += "#" + parsed.fragment
        return new
    return rewrite_links(text, replace)


def local_image_references(text: str) -> list[str]:
    paths = []
    def collect(value):
        parsed = urlsplit(html.unescape(value))
        path = unquote(parsed.path)
        if not parsed.scheme and not parsed.netloc and path and path not in paths:
            paths.append(path)
        return None
    rewrite_links(text, collect, images_only=True)
    return paths


@dataclass
class Document:
    root: Path
    stem: str

    def file(self, kind: str) -> Path:
        expected = self.root / kind / f"{self.stem}.{kind}"
        if not expected.exists() and expected.parent.is_dir():
            for candidate in expected.parent.iterdir():
                if candidate.stem == self.stem and candidate.suffix.lower() == f".{kind}":
                    return candidate
        return expected

    @property
    def pdf(self) -> Path:
        return self.file("pdf")

    @property
    def md(self) -> Path:
        return self.file("md")

    @property
    def front(self) -> dict:
        return read_front_matter(self.md)

    @property
    def record(self) -> dict:
        return next((r for r in Library(self.root).read_index() if stem_of(r) == self.stem), {})

    @property
    def ident(self) -> str | None:
        return self.front.get("id") or self.record.get("id") or identity_from_name(self.stem)

    @property
    def prefix(self) -> str:
        return clean_name(self.ident or self.stem)


class Library:
    def __init__(self, root):
        self.root = Path(root).expanduser().resolve()
        self.index = self.root / "index.csv"

    def read_index(self) -> list[dict]:
        if not self.index.is_file():
            return []
        with self.index.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            row["keywords"] = split_keywords(row.get("keywords"))
        return rows

    @staticmethod
    def render_index(rows: list[dict]) -> str:
        out = io.StringIO(newline="")
        writer = csv.DictWriter(out, fieldnames=INDEX_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in sorted(rows, key=stem_of):
            values = {key: row.get(key) or "" for key in INDEX_FIELDS}
            values["keywords"] = ";".join(split_keywords(row.get("keywords")))
            writer.writerow(values)
        return out.getvalue()

    def write_index(self, rows: list[dict]) -> None:
        atomic_text(self.index, self.render_index(rows))

    def documents(self, include_ledger=True) -> list[Document]:
        names = {stem_of(row) for row in self.read_index()} if include_ledger else set()
        for kind in ("pdf", "md"):
            folder = self.root / kind
            if folder.is_dir():
                names.update(p.stem for p in folder.iterdir() if p.is_file() and p.suffix.lower() == f".{kind}")
        return [Document(self.root, name) for name in sorted(names) if name]

    def resolve(self, token: str) -> Document:
        raw = name_stem(Path(token).name if Path(token).suffix.lower() in (".pdf", ".md") else token.strip())
        direct = Document(self.root, raw)
        if direct.pdf.is_file() or direct.md.is_file():
            return direct
        rows = [{**row, "_stem": stem_of(row)} for row in self.read_index()]
        known_names = {stem_of(row) for row in rows}
        # The optional ledger must not be necessary to locate a cached paper
        # by its id. Read identities from filenames/front matter when absent.
        for doc in self.documents(include_ledger=False):
            if doc.stem in known_names:
                continue
            ident = doc.front.get("id") or identity_from_name(doc.stem) or ""
            name = doc.stem.removeprefix(ident + ".") if ident else doc.stem
            if name == ident:
                name = ""
            rows.append({"id": ident, "name": name, "_stem": doc.stem})
        exact = [r for r in rows if token in (stem_of(r), r.get("id"), r.get("name")) or raw == stem_of(r)]
        if not exact:
            native = token.removeprefix("arxiv-").replace("/", "-")
            exact = [r for r in rows if (r.get("id") or "").removeprefix("arxiv-") == native]
            if not exact and re.fullmatch(r"\d{4}\.\d{4,5}", native):
                exact = [r for r in rows if re.sub(r"v\d+$", "", (r.get("id") or "").removeprefix("arxiv-")) == native]
        if len(exact) > 1:
            raise LibraryError(f"{token} 匹配多份资料，请指定具体文件路径：" + ", ".join(r["_stem"] for r in exact))
        if exact:
            return Document(self.root, exact[0]["_stem"])
        if raw != clean_name(raw):
            raise LibraryError(f"无法将 {token!r} 识别为本目录资料；请提供 PDF 路径或完整文件名。")
        return direct

    def rebuilt_index(self, documents=None, prune=False) -> list[dict]:
        rows = self.read_index()
        selected = self.documents(include_ledger=False) if documents is None else documents
        by_key = {(r.get("id") or "name:" + (r.get("name") or "")): dict(r) for r in rows}
        for doc in selected:
            front = doc.front
            old = next((r for r in rows if stem_of(r) == doc.stem), {})
            ident = front.get("id") or old.get("id") or identity_from_name(doc.stem) or ""
            if ident and doc.stem != ident and not doc.stem.startswith(ident + "."):
                raise LibraryError(f"{doc.stem} 的来源编号为 {ident}；建立四列索引前请用 rename 将名称调整为 {ident}.<名称>。")
            name = doc.stem.removeprefix(ident + ".") if ident else doc.stem
            if doc.stem == ident:
                name = ""
            key = ident or "name:" + name
            previous = by_key.get(key, old)
            by_key[key] = {
                "id": ident, "name": name,
                "keywords": previous.get("keywords") if previous else split_keywords(front.get("keywords")),
                "revised": previous.get("revised") or front.get("revised") or "",
            }
        if prune:
            present = {doc.stem for doc in self.documents(include_ledger=False)}
            by_key = {k: r for k, r in by_key.items() if stem_of(r) in present}
        return sorted(by_key.values(), key=stem_of)

    def update_existing_index(self, doc: Document) -> None:
        if self.index.is_file():
            self.write_index(self.rebuilt_index([doc]))

    def validate_conversion(self, doc: Document) -> None:
        prefix = doc.prefix.casefold()
        owners = [other.stem for other in self.documents(include_ledger=False)
                  if other.stem != doc.stem and other.prefix.casefold() == prefix]
        if owners:
            raise LibraryError(f"{doc.stem} 与 {', '.join(owners)} 使用同一资产前缀；请先整理重复身份，避免覆盖另一篇的图片。")
        if self.index.is_file():
            self.rebuilt_index([doc])  # Check filename/identity compatibility before writing.


def resolve_document(token: str, root=None) -> tuple[Document, Path | None]:
    path = Path(token).expanduser()
    native_old = re.fullmatch(r"(?:arxiv-)?[a-z][a-z0-9.-]*/\d{7}(?:v[1-9]\d*)?", token, re.I)
    explicit_path = not native_old and (path.is_absolute() or "/" in token or "\\" in token)
    if explicit_path and (not path.is_file() or path.suffix.lower() not in (".pdf", ".md")):
        raise LibraryError(f"指定的 PDF/MD 路径不存在或格式不符：{token}")
    source = path.resolve() if (explicit_path or root is None) and path.is_file() and path.suffix.lower() in (".pdf", ".md") else None
    if root is None:
        if source is None or source.parent.name.lower() not in ("pdf", "md"):
            raise LibraryError("请指定 --root 资料目录，或提供 a/pdf/文件.pdf（也可 a/md/文件.md）路径。")
        root = source.parent.parent
    lib = Library(root)
    doc = Document(lib.root, source.stem) if source else lib.resolve(token)
    return doc, source


def check_document(doc: Document, *, audit=None) -> dict:
    _, body = read_markdown(doc.md)
    missing = []
    if doc.md.is_file():
        for name in asset_references(body):
            path = (doc.root / "assets" / name).resolve()
            if not path.is_relative_to((doc.root / "assets").resolve()) or not path.is_file():
                missing.append(name)
        for reference in local_image_references(body):
            if not reference.startswith("../assets/") and not (doc.md.parent / reference).is_file():
                missing.append(reference)
    return {"root": str(doc.root), "stem": doc.stem, "pdf": doc.pdf.is_file(),
            "md": doc.md.is_file(), "md_body": bool(body.strip()), "missing_images": missing,
            "quality": audit,
            "complete": doc.pdf.is_file() and doc.pdf.stat().st_size > 0 and bool(body.strip()) and not missing}


def write_conversion(doc: Document, parsed: dict, metadata=None) -> None:
    if not parsed.get("body", "").strip():
        raise LibraryError("解析结果没有正文，未覆盖已有转换件。")
    Library(doc.root).validate_conversion(doc)
    front, _ = read_markdown(doc.md)
    info = metadata or {}
    for key in ("id", "title", "abstract", "revised", "source"):
        if not front.get(key) and info.get(key):
            front[key] = info[key]
    row = doc.record
    front["stem"] = doc.stem
    front["id"] = doc.ident or front.get("id")
    front["keywords"] = row.get("keywords", front.get("keywords", []))
    front["revised"] = row.get("revised") or front.get("revised")
    front["parser"] = parsed["parser"]
    # Check the complete in-memory result before touching an existing conversion.
    assets = parsed["assets"]
    absent = [p for p in asset_references(parsed["body"]) if p not in assets]
    if absent:
        raise LibraryError("MinerU 正文引用的图片未出现在结果包中：" + ", ".join(absent[:5]))
    for filename, payload in assets.items():
        if Path(filename).name != filename or not filename:
            raise LibraryError(f"无效资产文件名：{filename}")
        atomic_bytes(doc.root / "assets" / filename, payload)
    atomic_text(doc.md, render_markdown(front, parsed["body"]))
    Library(doc.root).update_existing_index(doc)


def rename_document(doc: Document, new_name: str) -> Document:
    new_name = clean_name(name_stem(new_name))
    target = Document(doc.root, new_name)
    if new_name == doc.stem:
        return target
    if not doc.pdf.is_file() and not doc.md.is_file():
        raise LibraryError(f"资料不存在：{doc.stem}")
    ident = doc.ident
    if ident and new_name != ident and not new_name.startswith(ident + "."):
        raise LibraryError(f"改名需保留来源编号 {ident}；新名应为 {ident}.<类型>.<简称>。")
    new_ident = ident or identity_from_name(new_name)
    front, body = read_markdown(doc.md)
    original_md = doc.md.read_bytes() if doc.md.is_file() else None
    pairs = ((doc.pdf, target.pdf), (doc.md, target.md))
    # A partial document still owns its whole name: do not pair its remaining
    # PDF or MD with the other half of an unrelated document at the target.
    for source, destination in pairs:
        if destination.exists() and not (source.exists() and source.samefile(destination)):
            raise LibraryError(f"目标已存在，未改名：{destination}")
    moves = [(source, destination) for source, destination in pairs if source.exists()]
    mapping = {}
    if not ident and (doc.root / "assets").is_dir():
        pattern = re.compile(r"^" + re.escape(doc.stem) + "-" + ASSET_KIND + r"\.[^.]+$", re.I)
        for asset in (doc.root / "assets").iterdir():
            if asset.is_file() and pattern.fullmatch(asset.name):
                new_file = clean_name(new_ident or new_name) + asset.name[len(doc.stem):]
                mapping[asset.name] = new_file
                moves.append((asset, asset.with_name(new_file)))
    for source, destination in moves:
        if destination.exists() and not source.samefile(destination):
            raise LibraryError(f"目标已存在，未改名：{destination}")
    lib = Library(doc.root)
    rows = lib.read_index()
    if any(stem_of(r) == new_name for r in rows):
        raise LibraryError(f"目标名称已在索引中，未改名：{new_name}")
    applied = []
    try:
        for source, destination in moves:
            source.rename(destination)
            applied.append((source, destination))
        if original_md is not None:
            front["stem"] = new_name
            if new_ident:
                front["id"] = new_ident
            atomic_text(target.md, render_markdown(front, rewrite_asset_names(body, mapping)))
        if lib.index.is_file():
            for row in rows:
                if stem_of(row) == doc.stem:
                    row["id"] = new_ident or ""
                    row["name"] = new_name.removeprefix(new_ident + ".") if new_ident else new_name
                    if new_name == new_ident:
                        row["name"] = ""
            lib.write_index(rows)
    except Exception:
        for source, destination in reversed(applied):
            if destination.exists() and not source.exists():
                destination.rename(source)
        if original_md is not None:
            atomic_bytes(doc.md, original_md)
        raise
    return target
