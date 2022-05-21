import requests
import json
import datetime
import pandas as pd
import io
import os


def get_current_oee():
    data = requests.get("http://192.168.178.132:8090/getFactory").json()
    totalEfficiency = 0
    countOfMachines = 0
    for machine in data:
        # print(machine['building'])
        # print(machine["production"][0]["ProdPercent"])
        totalEfficiency += float(machine["production"][0]["ProdPercent"])
        countOfMachines += 1
    oee = totalEfficiency/countOfMachines
    timestamp = datetime.datetime.now()
    print(f"OEE is: {str(oee)} at {str(timestamp)}")

    return oee, timestamp


def get_current_factory_data():
    data = requests.get("http://192.168.178.132:8090/getFactory").json()
    # with io.open()
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return(data)


def get_current_belt_data():
    belt_data = requests.get("http://192.168.178.132:8090/getBelts").json()
    with open('belt_data.json', 'w', encoding='utf-8') as f:
        json.dump(belt_data, f, ensure_ascii=False, indent=4)

    return(belt_data)


def get_resource_node():
    return requests.get("http://192.168.178.132:8090/getResourceNode").json()

#get_current_oee()
#print(get_resource_node())