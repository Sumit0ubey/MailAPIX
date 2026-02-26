import re
import html as _html
from typing import List


_URL_RE = re.compile(r"https?://[^\s<>()\"']+")
_TRAILING_PUNCT_RE = re.compile(r"[)\].,!?;:]+$")

def _auto_link_text(text: str) -> str:

    def repl(m: re.Match) -> str:
        url = m.group(0)
        trailing = ""
        stripped = _TRAILING_PUNCT_RE.search(url)
        if stripped:
            trailing = stripped.group(0)
            url = url[: -len(trailing)]

        return (
            f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
            + trailing
        )

    return _URL_RE.sub(repl, text)


def _flush_list(list_type: str, items: List[str]) -> str:
    if not items:
        return ""
    tag = "ul" if list_type == "ul" else "ol"
    li = "".join(f"<li>{item}</li>" for item in items)
    return f"<{tag}>{li}</{tag}>"


def plain_text_to_advanced_html(text: str) -> str:
    if text is None:
        return ""

    escaped = _html.escape(text).replace("\r\n", "\n").replace("\r", "\n")

    paragraphs = re.split(r"\n{2,}", escaped)

    out: List[str] = []
    list_type = None  # "ul" or "ol"
    list_items: List[str] = []

    for para in paragraphs:
        lines = para.split("\n")

        normal_lines: List[str] = []

        for line in lines:
            ul_m = re.match(r"^\s*[-*]\s+(.*)$", line)
            ol_m = re.match(r"^\s*\d+\.\s+(.*)$", line)

            if ul_m:
                if normal_lines:
                    joined = "<br/>".join(normal_lines)
                    out.append(f"<p>{_auto_link_text(joined)}</p>")
                    normal_lines = []

                if list_type and list_type != "ul":
                    out.append(_flush_list(list_type, list_items))
                    list_items = []
                list_type = "ul"

                list_items.append(_auto_link_text(ul_m.group(1).strip()))
                continue

            if ol_m:
                if normal_lines:
                    joined = "<br/>".join(normal_lines)
                    out.append(f"<p>{_auto_link_text(joined)}</p>")
                    normal_lines = []

                if list_type and list_type != "ol":
                    out.append(_flush_list(list_type, list_items))
                    list_items = []
                list_type = "ol"

                list_items.append(_auto_link_text(ol_m.group(1).strip()))
                continue

            if list_items:
                out.append(_flush_list(list_type or "ul", list_items))
                list_items = []
                list_type = None

            normal_lines.append(line)

        if list_items:
            out.append(_flush_list(list_type or "ul", list_items))
            list_items = []
            list_type = None

        if normal_lines:
            joined = "<br/>".join(normal_lines)
            out.append(f"<p>{_auto_link_text(joined)}</p>")

    return '<div style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5;">' + "".join(out) + "</div>"
