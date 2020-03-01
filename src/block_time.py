import requests
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool


def get_block_info(t):
    header = []
    ts = time.gmtime(t)
    date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    print(f"{date} 생성된 블록을 읽어옵니다.")
    url = f"https://blockchain.info/blocks/{t}000?format=json"
    res = requests.get(url)
    data = res.json()
    blocks = data["blocks"]
    for block in blocks:
        height = block["height"]
        btime = block["time"]
        bhash = block["hash"]
        header.append([height, btime, bhash])
    return header


def iter_fuc():
    now = int(time.time())
    for n in range(10):
        yield now - n * 86400


if __name__ == "__main__":
    print("loading...")
    result = []
    p = Pool(processes=32)
    process_result = p.map(get_block_info, iter_fuc())
    for pr in process_result:
        for r in pr:
            result.append(r)
    df = pd.DataFrame(result, columns=["Height", "Time", "Hash"])
    sdf = df.sort_values("Time")
    sdf = sdf.reset_index()
    print(f"총 {len(df)}개 헤더를 읽어옴.")
    mtime = sdf["Time"].diff().values
    mtime = mtime[np.logical_not(np.isnan(mtime))]
    print(f"평균 Mining 시간 = {np.mean(mtime)} (초)")
    print(f"표준편차 = {np.std(mtime)}")

    plt.figure(figsize=(8, 4))
    n, bins, patches = plt.hist(
        mtime, 30, facecolor="red", edgecolor="black", linewidth=0.5, alpha=0.5
    )
    plt.title("Mining Time Distribution")
    plt.show()

    s = 60 * 5
    p = 1 - np.exp(-s / np.mean(mtime))
    print(f"5분 이내에 내 거래가 Mining 될 확률 {p * 100} %")
