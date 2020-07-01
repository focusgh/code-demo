#!/usr/bin/env python
# coding: utf-8
# __author__ = 'wang tao'

import json
from locust import (
    HttpLocust,
    TaskSet,
    task,
    between
)


class WebsiteTasks(TaskSet):
    @task
    def get_workflow_info(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "id": "1",
            "method": "GetWorkflowInfo",
            "params": {
                "game": "master",
                "condition": {
                    "id": 39427
                }
            }
        })

        headers = {
            "Date": "2020-03-20T15:32:19+08:00",
            "Authorization": "PLAYCRAB test:ac5e9bcdaf0e8ae3d69d732f25efb964",
            "content-type": "application/json-rpc"
        }
        # self.client.request('POST', '/json', data=data, headers=headers)
        self.client.post('/json', data=data, headers=headers)


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://10.2.24.183:8000"
    # host = "http://127.0.0.1:8008"
    wait_time = between(1, 5)