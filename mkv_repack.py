import os
import sys
import re
from typing import List
import subprocess
from tools import mkvmerge, mkvextract

if sys.argv.__len__() < 2:
    raise Exception("Give me the animation download dir as parameter >_<")


video_list = []
sub_list = []


def mkv_merge(root, video, subs: List[str], ):
    output = os.path.join(root, os.path.splitext(video)[0]+".mkv")
    chapter = ""
    if os.path.isfile(output):
        os.makedirs(os.path.join(root, "tmp"), exist_ok=True)
        chapter = os.path.join(root, "tmp", video+".xml")
        chapter_byte: bytes = subprocess.run([mkvextract, "chapters", output], capture_output=True).stdout
        chapter_str = chapter_byte.decode("utf-8-sig").replace("\r\n", "\n")
        if chapter_str:
            with open(chapter, 'w') as chapter_xml:
                chapter_xml.write(chapter_str)
        else:
            chapter = ""
        output = os.path.join(root, "Merged", os.path.splitext(video)[0]+".mkv")
    subprocess.run([mkvmerge, "-o", output] +
                   (["--chapters", chapter] if chapter else []) +
                   subs +
                   [os.path.join(root, video)])


for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        file_name = os.path.splitext(file)[0]
        ext_name = os.path.splitext(file)[1]
        if ext_name in [".mp4"]:
            video_list.append((root, file))
        elif ext_name in [".ass", ".srt", ".sub"]:
            lang = ""
            if re.match(r'\.sc\.', re.I):
                lang = "简体中文"
            elif re.match(r'\.tc\.', re.I):
                lang = "繁体中文"
            sub_list.append((root, file, lang))

default_lang = "简体中文"

for v_root, v_name in video_list:
    subs = list(
        map(
            lambda s: ("--default-track 0 " if s[2] == default_lang else "") + f"--language 0:chi --title '{s[2]}'" + " " + os.path.join(s[0], s[1]),
            filter(lambda s: os.path.splitext(v_name)[0] in s[1], sub_list)
        )
    )
    mkv_merge(v_root, v_name, subs)

if os.path.isdir(os.path.join(sys.argv[1], "tmp")):
    os.rmdir(os.path.join(sys.argv[1], "tmp"))

