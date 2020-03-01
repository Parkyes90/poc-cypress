import os
from multiprocessing import Pool

import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

data = requests.get("https://blockchain.info/latestblock").json()
l_height = data["height"]


def get_miners(n):
    print(n)
    ret = []
    url = f"https://blockchain.info/block-height/{n}?format=json"
    res = requests.get(url)
    d = res.json()
    block = d["blocks"][0]
    print(block)
    stime = block["time"]
    try:
        addr = block["tx"][0]["out"][0]["addr"]
        value = block["tx"][0]["out"][0]["value"]
    except KeyError:
        addr = ""
        value = 0

    ts = time.gmtime(stime)
    date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    ret.append((date, addr, value))
    print(f"{n} {date} {addr} {value * 1e-8}")
    return ret


if __name__ == "__main__":
    result = []
    p = Pool(processes=os.cpu_count() * 2 if os.cpu_count() else 1)
    process_result = p.map(get_miners, range(l_height, l_height - 24, -1))
    for pr in process_result:
        for r in pr:
            result.append(r)
    df = pd.DataFrame(result, columns=["Date", "Address", "Reward"])
    grp = df.groupby("Address").Address.count()
    print(grp)

    plt.figure(figsize=(6, 3))
    plt.title("Miner's Address")
    x = list(range(1, len(grp.values) + 1))
    plt.bar(
        x,
        grp.values,
        width=1,
        color="red",
        edgecolor="black",
        linewidth=0.5,
        alpha=0.5,
    )
    plt.show()
