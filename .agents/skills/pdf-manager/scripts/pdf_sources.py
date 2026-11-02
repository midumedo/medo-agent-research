"""Source metadata and PDF downloads for the portable PDF manager.

This module does not write files.  arXiv version identity is retained through
every lookup; a response for another version is never used as a substitute.
"""

from __future__ import annotations

import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


class SourceError(RuntimeError):
    """The requested source could not be read or resolved reliably."""


USER_AGENT = "PDFManager/1.0 (source metadata and PDF retrieval)"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_ID = re.compile(r"(?:\d{4}\.\d{4,5}|[a-z][a-z0-9.-]*/\d{7})(?:v[1-9]\d*)?", re.I)
VERSION = re.compile(r"v([1-9]\d*)$", re.I)
ARXIV_HOSTS = {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}


def arxiv_id(value: str) -> str | None:
    """Return an exact native arXiv id, including its requested version.

    Full filename stems are intentionally not guessed here: the library layer
    is responsible for resolving its records and their ids.
    """
    text = (value or "").strip()
    if text.lower().startswith("arxiv:"):
        text = text[6:].strip()
    elif text.lower().startswith("arxiv-"):
        text = text[6:]
        # Legacy native ids contain a slash. The library identity uses a
        # filename-safe hyphen, while source requests keep the native slash.
        legacy = re.fullmatch(r"([a-z][a-z0-9.-]*)-(\d{7}(?:v[1-9]\d*)?)", text, re.I)
        if legacy:
            text = legacy.group(1) + "/" + legacy.group(2)
    if ARXIV_ID.fullmatch(text):
        return text
    parsed = urllib.parse.urlsplit(text)
    if parsed.scheme.lower() not in {"http", "https"} or (parsed.hostname or "").lower() not in ARXIV_HOSTS:
        return None
    path = urllib.parse.unquote(parsed.path).strip("/")
    if not path.startswith(("abs/", "pdf/")):
        return None
    candidate = path.split("/", 1)[1]
    if candidate.lower().endswith(".pdf"):
        candidate = candidate[:-4]
    return candidate if ARXIV_ID.fullmatch(candidate) else None


def _base_id(value: str) -> str:
    return VERSION.sub("", value)


def _read_url(url: str, *, timeout: int = 60) -> tuple[bytes, str]:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise SourceError("A source must be an HTTP or HTTPS URL.")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read(), response.geturl()
    except urllib.error.HTTPError as error:
        raise SourceError(f"Source request failed (HTTP {error.code}).") from error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise SourceError(f"Source request failed ({type(error).__name__}).") from error


def _flat_text(value: str | None) -> str | None:
    if not value:
        return None
    return re.sub(r"\s+", " ", html.unescape(value)).strip() or None


def _abstract_text(value: str | None, *, html_source: bool = False) -> str | None:
    if not value:
        return None
    if html_source:
        # Keep explicit subscript/superscript markup and LaTeX intact.  Removing
        # every HTML tag would silently turn mathematical subscripts into text.
        value = re.sub(r"</?(?!(?:sub|sup)\b)[A-Za-z][^>]*>", " ", value, flags=re.I)
    value = _flat_text(value)
    if not value:
        return None
    value = re.sub(r"^(?:abstract|摘要)\s*[:：—–-]?\s*", "", value, flags=re.I)
    return value or None


class _ArxivPage(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, list[str]] = {}
        self.abstract_parts: list[str] = []
        self.abstract_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key and "content" in values:
                self.meta.setdefault(key.lower(), []).append(values["content"])
        if tag == "blockquote" and (self.abstract_depth or "abstract" in values.get("class", "").split()):
            self.abstract_depth += 1
        elif self.abstract_depth:
            self.abstract_parts.append(self.get_starttag_text())

    def handle_endtag(self, tag: str) -> None:
        if tag == "blockquote" and self.abstract_depth:
            self.abstract_depth -= 1
        elif self.abstract_depth:
            self.abstract_parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self.abstract_depth:
            self.abstract_parts.append(data)

    def first(self, name: str) -> str | None:
        return next(iter(self.meta.get(name, [])), None)


def _page_metadata(aid: str) -> dict:
    page_url = "https://arxiv.org/abs/" + aid
    payload, final_url = _read_url(page_url)
    text = payload.decode("utf-8", "replace")
    page = _ArxivPage()
    page.feed(text)
    title = _flat_text(page.first("citation_title"))
    if not title:
        return {}

    returned = arxiv_id(page.first("citation_pdf_url") or "")
    if not returned or not VERSION.search(returned):
        returned = arxiv_id(page.first("citation_arxiv_id") or "")
    if not returned or not VERSION.search(returned):
        identity = re.search(r'<span\b[^>]*class=[\'"][^\'"]*\barxivid\b[^\'"]*[\'"][^>]*>(.*?)</span>', text, re.I | re.S)
        visible = html.unescape(re.sub(r"<[^>]+>", " ", identity.group(1))) if identity else ""
        match = re.search(r"arXiv:\s*(" + re.escape(_base_id(aid)) + r"v[1-9]\d*)\b", visible, re.I)
        returned = match.group(1) if match else None
    if VERSION.search(aid):
        if returned and returned != aid:
            return {}
        # Explicitly addressed version pages can omit the version in their
        # citation metadata.  A redirect to another version is not accepted.
        final_id = arxiv_id(final_url)
        if final_id != aid:
            return {}
        returned = aid
    if returned and _base_id(returned) != _base_id(aid):
        return {}
    return {
        "versioned_id": returned if returned and VERSION.search(returned) else None,
        "title": title,
        "abstract": _abstract_text("".join(page.abstract_parts), html_source=True),
        "authors": [_flat_text(author) for author in page.meta.get("citation_author", [])],
        # citation_date commonly describes v1, so it is not reused as the
        # requested version's revision date.
        "published": _date(page.first("citation_date")),
    }


def _date(value: str | None) -> str | None:
    match = re.match(r"(\d{4})[-/](\d{2})[-/](\d{2})", value or "")
    return "-".join(match.groups()) if match else None


def _api_metadata(aid: str) -> dict:
    query = urllib.parse.urlencode({"id_list": aid, "max_results": 1})
    payload, _ = _read_url("https://export.arxiv.org/api/query?" + query)
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as error:
        raise SourceError("arXiv returned invalid metadata XML.") from error
    for entry in root.findall(ATOM + "entry"):
        returned = arxiv_id(entry.findtext(ATOM + "id", ""))
        if not returned or not VERSION.search(returned) or _base_id(returned) != _base_id(aid):
            continue
        if VERSION.search(aid) and returned != aid:
            continue
        return {
            "versioned_id": returned,
            "title": _flat_text(entry.findtext(ATOM + "title")),
            "abstract": _abstract_text(entry.findtext(ATOM + "summary")),
            "revised": _date(entry.findtext(ATOM + "updated")),
            "published": _date(entry.findtext(ATOM + "published")),
            "authors": [_flat_text(author.findtext(ATOM + "name")) for author in entry.findall(ATOM + "author")],
        }
    return {}


def _empty_metadata() -> dict:
    return {key: None for key in ("id", "title", "abstract", "revised", "source", "pdf_url", "version", "filename")}


def fetch_metadata(value: str) -> dict:
    """Fetch arXiv metadata or describe an explicitly supplied PDF URL.

    An unversioned arXiv input must resolve to an explicit version.  Once a
    version is chosen, metadata from another version cannot fill its blanks.
    """
    aid = arxiv_id(value)
    if not aid:
        parsed = urllib.parse.urlsplit((value or "").strip())
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            raise SourceError("Supply an arXiv id, arXiv URL, or an HTTP(S) PDF URL.")
        result = _empty_metadata()
        filename = urllib.parse.unquote(parsed.path.rsplit("/", 1)[-1]).strip()
        # An encoded slash must not become a new output directory.
        filename = filename.replace("/", ".").replace("\\", ".")
        result.update(source=value.strip(), pdf_url=value.strip(), filename=filename or "document.pdf")
        return result

    warnings = []
    try:
        page = _page_metadata(aid)
    except SourceError as error:
        page = {}
        warnings.append(str(error))
    chosen = aid if VERSION.search(aid) else page.get("versioned_id")

    # If the page resolves an unversioned input, query that exact version next.
    # This avoids combining a page from one revision with a newer API response.
    api_query = chosen or aid
    try:
        api = _api_metadata(api_query)
    except SourceError as error:
        api = {}
        warnings.append(str(error))
    chosen = chosen or api.get("versioned_id")
    if not chosen:
        raise SourceError("arXiv version unresolved; retry with an explicit versioned id.")

    if page.get("versioned_id") != chosen:
        # Fetch an explicit page when the unversioned page did not identify its
        # version.  Its potentially current text must not fill a pinned record.
        try:
            page = _page_metadata(chosen)
        except SourceError as error:
            page = {}
            warnings.append(str(error))
    if api.get("versioned_id") != chosen:
        api = {}
    result = _empty_metadata()
    result.update(
        id="arxiv-" + chosen.replace("/", "-"),
        native_id=_base_id(chosen),
        versioned_id=chosen,
        version="v" + VERSION.search(chosen).group(1),
        title=page.get("title") or api.get("title"),
        abstract=page.get("abstract") or api.get("abstract"),
        revised=api.get("revised"),
        published=api.get("published") or page.get("published"),
        authors=page.get("authors") or api.get("authors") or [],
        source="https://arxiv.org/abs/" + chosen,
        pdf_url="https://arxiv.org/pdf/" + chosen,
        filename="arxiv-" + chosen.replace("/", "-") + ".pdf",
    )
    if warnings:
        result["warnings"] = warnings
    return result


def download_pdf(url: str) -> bytes:
    """Read PDF bytes without imposing a paper-specific minimum file size."""
    payload, _ = _read_url(url, timeout=120)
    header = payload[:1024].lstrip(b"\xef\xbb\xbf \t\r\n")
    if not payload or not header.startswith(b"%PDF-"):
        raise SourceError("The source response is not a PDF.")
    return payload


def _front_scalars(text: str) -> tuple[dict, str]:
    match = re.match(r"\A\ufeff?---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", text, re.S)
    if not match:
        return {}, text
    fields = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator or key.strip() not in {"title", "abstract"}:
            continue
        value = value.strip()
        if value.startswith('"'):
            try:
                value = json.loads(value)
            except (ValueError, TypeError):
                continue
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
        if isinstance(value, str) and value.lower() not in {"", "null", "none", "~", "|", ">"}:
            fields[key.strip()] = value
    return fields, text[match.end():]


def extract_document_metadata(text: str) -> dict:
    """Read a source's title and labelled abstract from converted Markdown.

    No abstract label means no inferred abstract.  The actual text, including
    mathematical markup, is retained rather than summarized or rewritten.
    """
    fields, body = _front_scalars(text)
    title = fields.get("title")
    if not title:
        heading = re.search(r"^\s*#\s+(.+?)\s*#*\s*$", body, re.M)
        title = heading.group(1).strip() if heading else None
    abstract = fields.get("abstract")
    if abstract:
        return {"title": title, "abstract": abstract}

    lines = body.splitlines()
    marker = re.compile(
        r"^\s*(?:#{1,6}\s*)?(?:\d+(?:\.\d+)*\.?\s+)?"
        r"(?:\*\*|__)?(?:abstract|摘要)(?:\*\*|__)?"
        r"(?:\s*[:：—–-]\s*|\s*$)(.*)$", re.I
    )
    boundary = re.compile(
        r"^\s*(?:#{1,6}\s+|(?:\d+(?:\.\d+)*\.?\s+)?(?:introduction|引言|绪论)\b|"
        r"(?:\*\*|__)?(?:key\s*words|keywords|index\s+terms|关键词|关键字)(?:\*\*|__)?\s*[:：])", re.I
    )
    for start, line in enumerate(lines):
        matched = marker.match(line)
        if not matched:
            continue
        collected = [matched.group(1)] if matched.group(1).strip() else []
        for following in lines[start + 1:]:
            if boundary.match(following):
                break
            collected.append(following)
        abstract = _abstract_text("\n".join(collected))
        break
    return {"title": title, "abstract": abstract}
