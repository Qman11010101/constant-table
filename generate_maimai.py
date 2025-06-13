import hashlib
import json
import os
import sys

from commonlib import easy_get, html_levblock, html_span


def html_items(song_str: str, is_remaster: bool = False) -> str:
    remaster_str = ""
    if is_remaster:
        remaster_str = " style=\"background-image: url('remaster.png');\""
    return f'<div class="items"{remaster_str}>{song_str}</div>'


DATA_URL = "https://reiwa.f5.si/maimai_record.json"
IMAGE_URL_BASE = "https://reiwa.f5.si/musicjackets/maimai/"
TEMPLATE_PATH = "./templates/maimai-template.html"

GAME_VERSION_PLACEHOLDER = "{{ GAME_VERSION }}"
OUT_FIELD_PLACEHOLDER = "{{ OUT_FIELD }}"
COPYRIGHT_PLACEHOLDER = "{{ COPYRIGHT }}"

GAME_VERSION = "PRiSM PLUS"

# fmt: off
constlist = [
    15.9, 15.8, 15.7, 15.6, 15.5, 15.4, 15.3, 15.2, 15.1, 15.0,
    14.9, 14.8, 14.7, 14.6, 14.5, 14.4, 14.3, 14.2, 14.1, 14.0,
    13.9, 13.8, 13.7, 13.6, 13.5, 13.4, 13.3, 13.2, 13.1, 13.0,
    12.9, 12.8, 12.7, 12.6, 12.5, 12.4, 12.3, 12.2, 12.1, 12.0,
    11.9, 11.8, 11.7, 11.6, 11.5, 11.4, 11.3, 11.2, 11.1, 11.0,
    10.9, 10.8, 10.7, 10.6, 10.5, 10.4, 10.3, 10.2, 10.1, 10.0,
    9.7,  9.0,  8.7,  8.0,  7.7,  7.0,  6.0,  5.0,  4.0,  3.0,
    2.0,  1.0,  0.0,
]
# fmt: on

raw_data = easy_get(DATA_URL)
if ord(raw_data[0]) == 65279:
    raw_data = raw_data[1:]  # BOM除去

data: dict = json.loads(raw_data)

# check if data is renewed (force = False)
if len(sys.argv) > 1 and sys.argv[1] != "force":
    if os.path.isfile("./maimai_record.json"):
        with open("./maimai_record.json", "r", encoding="utf-8_sig") as f:
            old_data = json.load(f)
        if old_data == data:
            print("No update")
            sys.exit()
        else:
            print("Data updated")
            with open("./maimai_record.json", "w", encoding="utf-8_sig") as f:
                json.dump(data, f, ensure_ascii=False)
    else:
        with open("./maimai_record.json", "w", encoding="utf-8_sig") as f:
            json.dump(data, f, ensure_ascii=False)
else:
    print("Force update")

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
    items.append(html_items(f'<div class="levconst">{html_span(const_formatted)}</div>'))
    songs = data_classified[const]
    for song in songs:
        title: str = song["title"]
        artist: str = song["artist"]
        diff: str = song["diff"]

        imgsrc = hashlib.md5((title + artist).encode("utf-8")).hexdigest()
        html_img_str = f'<img src="{IMAGE_URL_BASE}{imgsrc}.webp" class="{diff.lower()}" loading="lazy">'
        html_titleblock_str = f'<div class="titleblock">{html_span(title)}</div>'
        makrers_str = ""
        if song.get("is_unknown", False):
            makrers_str = '<div class="unknown-marker"></div>'
        if song.get("is_dx", False):
            makrers_str += '<div class="dx-marker"></div>'
        items.append(html_items(html_img_str + html_titleblock_str + makrers_str, diff == "REMAS"))

    html_outfield += html_levblock("".join(items))

with open(TEMPLATE_PATH, "r", encoding="utf-8_sig") as f:
    template_str = f.read()

template_str = template_str.replace(GAME_VERSION_PLACEHOLDER, GAME_VERSION).replace(OUT_FIELD_PLACEHOLDER, html_outfield)

with open("./docs/maimai.html", "w", encoding="utf-8_sig") as f:
    f.write(template_str)
