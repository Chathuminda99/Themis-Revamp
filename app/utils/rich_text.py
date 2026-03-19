"""Helpers for storing and rendering limited rich text safely."""

from __future__ import annotations

import re
from html import escape, unescape
from html.parser import HTMLParser

from markupsafe import Markup


_HTML_TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")
_PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n+")
_ALLOWED_TAGS = {"p", "br", "strong", "em", "u", "ul", "ol", "li"}
_TAG_ALIASES = {"b": "strong", "i": "em", "div": "p"}
_DROP_CONTENT_TAGS = {"script", "style"}


def _normalize_text(value: str | None) -> str:
    """Normalize line endings and whitespace from user input."""
    if value is None:
        return ""
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\xa0", " ").strip()


def _looks_like_html(value: str) -> bool:
    """Return True when the value already contains HTML tags."""
    return bool(_HTML_TAG_RE.search(value))


def plain_text_to_html(value: str | None) -> str:
    """Convert legacy plain text into simple paragraph-based HTML."""
    normalized = _normalize_text(value)
    if not normalized:
        return ""

    paragraphs = [paragraph.strip() for paragraph in _PARAGRAPH_SPLIT_RE.split(normalized) if paragraph.strip()]
    html_parts: list[str] = []
    for paragraph in paragraphs:
        lines = [escape(line) for line in paragraph.split("\n")]
        html_parts.append(f"<p>{'<br>'.join(lines)}</p>")
    return "".join(html_parts)


class _RichTextSanitizer(HTMLParser):
    """Very small allowlist sanitizer for editor-generated HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._drop_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        normalized_tag = _TAG_ALIASES.get(tag.lower(), tag.lower())
        if normalized_tag in _DROP_CONTENT_TAGS:
            self._drop_depth += 1
            return
        if self._drop_depth:
            return
        if normalized_tag in _ALLOWED_TAGS:
            self.parts.append(f"<{normalized_tag}>")

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = _TAG_ALIASES.get(tag.lower(), tag.lower())
        if normalized_tag in _DROP_CONTENT_TAGS:
            self._drop_depth = max(0, self._drop_depth - 1)
            return
        if self._drop_depth:
            return
        if normalized_tag in _ALLOWED_TAGS and normalized_tag != "br":
            self.parts.append(f"</{normalized_tag}>")

    def handle_startendtag(self, tag: str, attrs) -> None:
        normalized_tag = _TAG_ALIASES.get(tag.lower(), tag.lower())
        if self._drop_depth:
            return
        if normalized_tag == "br":
            self.parts.append("<br>")

    def handle_data(self, data: str) -> None:
        if self._drop_depth or not data:
            return
        self.parts.append(escape(data))

    def handle_entityref(self, name: str) -> None:
        if self._drop_depth:
            return
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self._drop_depth:
            return
        self.parts.append(f"&#{name};")

    def get_html(self) -> str:
        html = "".join(self.parts).strip()
        html = re.sub(r"<p>\s*(?:<br>\s*)*</p>", "", html)
        html = re.sub(r"(?:<br>\s*){3,}", "<br><br>", html)
        return html.strip()


def sanitize_rich_text(value: str | None) -> str | None:
    """Normalize editor input into safe limited HTML for storage."""
    normalized = _normalize_text(value)
    if not normalized:
        return None

    if not _looks_like_html(normalized):
        return plain_text_to_html(normalized) or None

    sanitizer = _RichTextSanitizer()
    sanitizer.feed(normalized)
    sanitizer.close()
    sanitized = sanitizer.get_html()
    if not sanitized:
        return None
    if not _looks_like_html(sanitized):
        return plain_text_to_html(unescape(sanitized)) or None
    return sanitized


def render_rich_text(value: str | None) -> Markup:
    """Render stored rich text or legacy plain text as safe HTML."""
    return Markup(sanitize_rich_text(value) or "")
