import http.client
import time
import urllib.error
import urllib.request

_USER_AGENT = "constant-table/1.0 (+https://github.com/Qman11010101/constant-table)"
_MAX_ATTEMPTS = 3
_BACKOFF_SECONDS = (2, 4)


def _http_error_excerpt(exc: urllib.error.HTTPError) -> str:
    try:
        raw = exc.read()
    except Exception:
        return ""
    finally:
        try:
            exc.close()
        except Exception:
            pass
    if not raw:
        return ""
    return raw.decode("utf-8-sig", errors="replace")[:200]


def easy_get(url: str) -> str:
    for attempt in range(_MAX_ATTEMPTS):
        request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
        try:
            with urllib.request.urlopen(request) as response:
                return response.read().decode("utf-8-sig")
        except urllib.error.HTTPError as e:
            reason = e.reason
            excerpt = _http_error_excerpt(e)
            e.msg = f"{reason}: {excerpt}"
            retryable = e.code == 403 or 500 <= e.code <= 599
            if retryable and attempt + 1 < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_SECONDS[attempt])
                continue
            raise
        except (
            urllib.error.URLError,
            TimeoutError,
            ConnectionError,
            http.client.IncompleteRead,
        ):
            if attempt + 1 < _MAX_ATTEMPTS:
                time.sleep(_BACKOFF_SECONDS[attempt])
                continue
            raise


def html_levblock(items_str: str) -> str:
    return f'<div class="levblock">{items_str}</div>'


def html_p(s: str) -> str:
    return f"<p>{s}</p>"


def html_span(s: str) -> str:
    return f"<span>{s}</span>"


def html_div(s: str) -> str:
    return f"<div>{s}</div>"
