import requests
import re
import json
import time

callback = ""
login_id = "393189"
login_token = "9a18ebcaf77940fc8a999916ced3bd6b"
timestamp = "1560868562353"

answer_link = "http://m.mnw.cn/keji/shouyou/gonglue/2170262.html"
res = requests.get(answer_link)
page = res.content.decode()
secrets = []

for i in range(ord('A'), ord('E')):
    for j in range(1, 6):
        exp = f"{chr(i)}{j}\[(.*)\]"
        search_obj = re.search(exp, page, re.M | re.I)
        secrets.append(search_obj.group(1))

submit_link = "https://g37secret.webapp.163.com/submit"
for secret in secrets:
    res = requests.get(submit_link, params={
        'callback': callback,
        'login_id': login_id,
        'login_token': login_token,
        'secret': secret,
        '_': timestamp
    })

    res_json = json.loads(res.content.decode())
    if not res_json["success"]:
        print(f"Error when submit {secret}: " + res_json["msg"])

    time.sleep(2)
