import urllib.request


def easy_get(url: str):
    try:
        with urllib.request.urlopen(url) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset)
    except urllib.error.URLError as e:
        return f"Error: {e.reason}"
    except Exception as e:
        return f"Unexpected Error: {e}"


def html_levblock(items_str: str) -> str:
    return f'<div class="levblock">{items_str}</div>'


def html_p(s: str) -> str:
    return f'<p>{s}</p>'


def html_span(s: str) -> str:
    return f'<span>{s}</span>'


def html_div(s: str) -> str:
    return f'<div>{s}</div>'