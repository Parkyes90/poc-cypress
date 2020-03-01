import os

import requests
import time
import matplotlib.pyplot as plt
from multiprocessing import Pool

pages = 100

if __name__ == "__main__":
    result = []
    before = time.time()

    def get_data(n):
        p_result = []
        url = (
            f"https://bitnodes.earn.com/api/v1/snapshots/"
            f"?limit=100&page={n}"
        )
        res = requests.get(url)
        data = res.json()
        print(f"page {n} loaded")
        for item in data["results"]:
            ts = item["timestamp"]
            p_result.append((ts, item["total_nodes"]))

        return p_result

    p = Pool(processes=os.cpu_count() * 2 if os.cpu_count() else 1)
    process_result = p.map(get_data, (range(1, pages)))
    for pr in process_result:
        for r in pr:
            result.append(r)
    result.sort(key=lambda x: x[0])
    nodes = list(map(lambda x: x[1], result))
    dates = list(
        map(
            lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(x[0])),
            result,
        )
    )
    print(time.time() - before)
    plt.figure(figsize=(8, 6))
    plt.plot(nodes, color="red", linewidth=0.7)
    plt.title(f"Bitcoin Nodes {dates[0]} ~ {dates[-1]}")
    plt.grid(color="green", alpha=0.2)
    plt.show()
