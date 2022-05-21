from data_getter import *
import json
import pandas as pd


def get_machine_coordinates_to_excel():
    # Get the overall factory data
    f = open('data.json')
    data = json.load(f)
    machine_data = []
    for machine in data:
        temp_data = [machine["building"], machine['location']
                     ['x'], machine['location']['y']]
        machine_data.append(temp_data)
    df = pd.DataFrame(machine_data, columns=['Building', 'X', 'Y'])
    df.to_excel('machine_coordinates.xlsx', index=False)


def factory_to_excel():
    f = open('data.json')
    data = json.load(f)
    df = pd.DataFrame(data)
    df.to_excel('factory.xlsx', index=False)
