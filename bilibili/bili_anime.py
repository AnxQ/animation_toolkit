import requests
import re
import json
import tkinter as tk
import subprocess
import sys
import re
import os
from tools import curl, arch_bit, arch_sys
from hashlib import sha1

print(arch_bit, arch_sys, curl)

api_servers = [
    [r"^((?!僅).)*$", "https://api.bilibili.com/"],
    [r"僅.*港.*地區", "https://bilibili-hk-api.kghost.info/"],
    [r"僅.*台.*地區", "https://bilibili-tw-api.kghost.info/"]
]

tmp_dir = "D:\\BiliDown\\temp"
down_dir = "D:\\BiliDown"

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'
}

proxies = {
    "http": "socks5://localhost:1080/",
    "https": "socks5://localhost:1080/"
}

cookies = {
    "CURRENT_FNVAL": "16",
    "DedeUserID": "4834780",
    "DedeUserID__ckMd5": "31c462862902665b",
    "LIVE_BUVID": "AUTO3515632748010172",
    "SESSDATA": "bc4ae8cf%2C1565866792%2C2cb45671",
    "_uuid": "80433CF7-D881-951C-8FD9-97C55C754C0901026infoc",
    "bili_jct": "71e03e0e3ae4f1a962477ae16aaebabf",
    "buvid3": "20EC86E8-0695-482F-8A4D-9917675320E1110236infoc",
    "sid": "4i99biko"
}


def get_bangumi(ss_id: int = None, md_id: int = None):
    sess = requests.session()
    res = sess.get(f"https://www.bilibili.com/bangumi/play/ss{md_id}").content.decode()
    patt = re.compile(r"window.__INITIAL_STATE__=(.*?);", re.MULTILINE | re.DOTALL)
    initial_state = re.findall(patt, res)
    initial_state_obj = json.loads(initial_state[0])

    current_api = ""

    bangumi_name = initial_state_obj["h1Title"]
    bangumi_down_dir = os.path.join(down_dir, bangumi_name)

    for server in api_servers:
        if re.search(server[0], bangumi_name):
            current_api = server[1]

    bangumi_data = []

    for ep in initial_state_obj["epList"]:
        title = f"{ep['titleFormat']} {ep['longTitle']}"
        aid = ep["aid"]
        cid = ep["cid"]
        try:
            res = json.loads(
                sess.get(f"{current_api}pgc/player/web/playurl?avid={aid}&cid={cid}&otype=json&qn=116&fnval=16",
                         headers=headers)
                    .content
                    .decode()
            )

            res = res["result"]
            video_addr = max(res["dash"]["video"], key=lambda x: x["bandwidth"])["baseUrl"]
            audio_addr = max(res["dash"]["audio"], key=lambda x: x["bandwidth"])["baseUrl"]

            bangumi_data.append({'title': title, 'video': video_addr, 'audio': audio_addr})
            print(bangumi_data[-1])
        except KeyError:
            print(res)
    if not os.path.exists(bangumi_down_dir):
        os.makedirs(bangumi_down_dir)
    for ep in bangumi_data:
        v_fn = os.path.join(tmp_dir, sha1(ep["title"].encode()).hexdigest() + ".mp4")
        a_fn = os.path.join(tmp_dir, sha1(ep["title"].encode()).hexdigest() + ".aac")
        m_fn = os.path.join(bangumi_down_dir, re.sub(r'[\/:*?"<>|]', '-', ep["title"]) + ".mp4")
        dl_process = subprocess.Popen([curl,
                                       '-H', 'Origin: https://www.bilibili.com',
                                       '-H', 'Referer: https://www.bilibili.com/bangumi/play/ep118488',
                                       '-H', 'Sec-Fetch-Mode: cors',
                                       '-H',
                                       'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit',
                                       ep['video'], '--progress',
                                       '-o', v_fn],
                                      stdout=subprocess.PIPE)
        while dl_process.poll() is None:
            out = dl_process.stdout.readline()
            if out:
                print(out)
        print(f"{ep['title']} -> Video -> {v_fn}")

        dl_process = subprocess.Popen([curl,
                                       '-H', 'Origin: https://www.bilibili.com',
                                       '-H', 'Referer: https://www.bilibili.com/bangumi/play/ep118488',
                                       '-H', 'Sec-Fetch-Mode: cors',
                                       '-H',
                                       'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit',
                                       ep['audio'], '--progress',
                                       '-o', a_fn],
                                      stdout=subprocess.PIPE)
        while dl_process.poll() is None:
            out = dl_process.stdout.readline()
            if out:
                print(out)
        print(f"{ep['title']} -> Audio -> {a_fn}")

        merge_process = subprocess.run(["D:\\MarukoToolbox\\tools\\ffmpeg.exe", "-y",
                                        "-i", v_fn, "-i", a_fn,
                                        "-map", "0:v", "-c:v", "copy", "-map", "1:0", "-c:a", "copy",
                                        m_fn], capture_output=True)

        print(f"{ep['title']} -> Merge -> {m_fn}")

        os.remove(v_fn)
        os.remove(a_fn)


class App:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack()
        tk.Label(master, text="GLHF").pack()


if __name__ == "__main__":
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    # root = tk.Tk()
    # root.geometry("500x300")
    # root.resizable(width=False, height=False)
    # app = App(root)
    # root.mainloop()
    get_bangumi(ss_id=28011)
