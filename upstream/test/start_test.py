#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests

def get_cost_time():
    resp = requests.get("http://127.0.0.1:9080/")
    return int(resp.elapsed.total_seconds() * 1000)

if __name__ == "__main__":
    for i in range(1, 10000):
        ngate_cost = get_cost_time()
        # print("cost: {}ms".format(ngate_cost))
        if ngate_cost > 10:
            print("cost: {}ms".format(ngate_cost))
