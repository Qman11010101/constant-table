import hashlib
import json
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

def html_items(song_str: str, is_ultima: bool = False) -> str:
    return f'<div class="items"{'''style="background-image: url('ultima.png');"''' if is_ultima else ""}>{song_str}</div>'

def html_p(s: str) -> str:
    return f'<p>{s}</p>'

DATA_URL = "https://reiwa.f5.si/chunithm_record.json"
COPYRIGHT_URL = "https://reiwa.f5.si/chunithm_right.json"
IMAGE_URL_BASE = "https://reiwa.f5.si/musicjackets/chunithm/"
TEMPLATE_PATH = "./templates/chunithm-template.html"

GAME_VERSION_PLACEHOLDER = "{{ GAME_VERSION }}"
OUT_FIELD_PLACEHOLDER = "{{ OUT_FIELD }}"
COPYRIGHT_PLACEHOLDER = "{{ COPYRIGHT }}"

GAME_VERSION = "LUMINOUS PLUS"

constlist = [
    15.9, 15.8, 15.7, 15.6, 15.5, 15.4, 15.3, 15.2, 15.1, 15,
    14.9, 14.8, 14.7, 14.6, 14.5, 14.4, 14.3, 14.2, 14.1, 14,
    13.9, 13.8, 13.7, 13.6, 13.5, 13.4, 13.3, 13.2, 13.1, 13,
    12.9, 12.8, 12.7, 12.6, 12.5, 12.4, 12.3, 12.2, 12.1, 12,
    11.9, 11.8, 11.7, 11.6, 11.5, 11.4, 11.3, 11.2, 11.1, 11,
    10.9, 10.8, 10.7, 10.6, 10.5, 10.4, 10.3, 10.2, 10.1, 10,
    9.5, 9, 8.5, 8, 7.5, 7, 6, 5, 4, 3, 2, 1
]

raw_data = easy_get(DATA_URL)
if ord(raw_data[0]) == 65279:
    raw_data = raw_data[1:]  # BOM除去

raw_rights = easy_get(COPYRIGHT_URL)
if ord(raw_rights[0]) == 65279:
    raw_rights = raw_rights[1:]  # BOM除去
rights = json.loads(raw_rights)

data: dict = json.loads(raw_data)
data.sort(key=lambda x: (x["const"], x["release"] * -1), reverse=True)

current_const = constlist[0]
data_classified = {}

for music in data:
    if music["const"] != current_const:
        current_const = music["const"]
        data_classified[str(current_const)] = []
    data_classified[str(current_const)].append(music)

html_outfield = ""
for const_block in constlist:
    const = str(const_block)
    const_formatted = "{:.1f}".format(const_block)
    if const not in data_classified:
        continue
    items = []
    items.append(html_items(f'<div class="levconst">{const_formatted}</div>'))
    songs = data_classified[const]
    for song in songs:
        title: str = song["title"]
        artist: str = song["artist"]
        diff: str = song["diff"]
        html_img_str = f'<img src="{IMAGE_URL_BASE}{hashlib.md5(f"{title}{artist}".encode("utf-8")).hexdigest()}.webp" class="{diff.lower()}" loading="lazy">'
        html_titleblock_str = f'<div class="titleblock">{title}</div>'
        items.append(html_items(
            html_img_str + html_titleblock_str,
            diff == "ULT"
        ))
    html_outfield += html_levblock("".join(items))

html_copyrights = ""
for right in rights:
    html_copyrights += html_p(right)

with open(TEMPLATE_PATH, "r", encoding="utf-8_sig") as f:
    template_str = f.read()

template_str = template_str \
.replace(GAME_VERSION_PLACEHOLDER, GAME_VERSION) \
.replace(OUT_FIELD_PLACEHOLDER, html_outfield) \
.replace(COPYRIGHT_PLACEHOLDER, html_copyrights)

with open("./root/chunithm.html", "w", encoding="utf-8_sig") as f:
    f.write(template_str)