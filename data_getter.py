import requests
import json
import datetime
import pandas as pd
import io
import os
import time


def get_current_oee():
    data = requests.get("http://192.168.178.132:8090/getFactory").json()
    totalEfficiency = 0
    countOfMachines = 0
    for machine in data:
        # print(machine['building'])
        # print(machine["production"][0]["ProdPercent"])
        totalEfficiency += float(machine["production"][0]["ProdPercent"])
        countOfMachines += 1
    #timestamp = datetime.datetime.now()
    #print(f"OEE is: {str(oee)} at {str(timestamp)}")

    return totalEfficiency/countOfMachines


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


def get_current_production_of(product):
    data = get_current_factory_data()
    return sum(machine['production'][0]['CurrentProd'] for machine in data if machine["Recipe"] == product)


# sourcery skip: avoid-builtin-shadow
def get_current_consumption_of(product):
    data = get_current_factory_data()
    sum = 0
    for machine in data:
        for ingredient in machine['ingredients']:
            if ingredient['Name'] == product:
                sum += ingredient['CurrentConsumed']
    return sum

def get_current_consumption_of(product):
    data = get_current_factory_data()
    sum = 0
    for machine in data:
        for ingredient in machine['ingredients']:
            if ingredient['Name'] == product:
                sum += ingredient['CurrentConsumed']
    return sum


def get_ingredients():
    data = get_current_factory_data()
    ingredients = []
    for machine in data:
        if machine['Recipe'] not in ingredients:
            ingredients.append(machine['Recipe'])
    return ingredients

def get_overall_consumption_percentage():
    items = get_ingredients()

    counter = 0
    total = 0

    for item in items:
        name = item.split(" ")

        if item not in ['Automated Wiring', 'Versatile Framework', 'Modular Frame', 'Smart Plating'] or len(name) > 1 and name[1] != 'Ore':
            production = get_current_production_of(item)
            if production > 0:
                total += (get_current_consumption_of(item)/production)*100
                counter += 1
    
    return total/counter

#print(get_overall_consumption_percentage())

# print(get_resource_node())

# print(get_current_factory_data())
