#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests

def get_cost_time():
    resp = requests.get("http://127.0.0.1:8000/")
    return int(resp.elapsed.total_seconds() * 1000)

if __name__ == "__main__":
    cost_result = {}
    cost_result["0ms"] = 0
    cost_result["0~2ms"] = 0
    cost_result["2~5ms"] = 0
    cost_result["5~10ms"] = 0
    cost_result[">=10ms"] = 0
    
    for i in range(1, 10000):
        cost_time = get_cost_time()

        if cost_time == 0:
            cost_result["0ms"] += 1

        elif cost_time >= 0 and cost_time < 2:
            cost_result["0~2ms"] += 1
        
        elif cost_time >= 2 and cost_time < 5:
            cost_result["2~5ms"] += 1

        elif cost_time >= 5 and cost_time < 10:
            cost_result["5~10ms"] += 1

        elif cost_time >= 10:
            cost_result[">=10ms"] += 1

        if cost_time > 10:
            print("cost: {}ms".format(cost_time))
    

    cost_result_sort = sorted(cost_result.items(),
                                      key=lambda x: x[1],
                                      reverse=True)   

    print("Latency stats:")
    for i in cost_result_sort:
        print("{}: {}".format(i[0], i[1]))
