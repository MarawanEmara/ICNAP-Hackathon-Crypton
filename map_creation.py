from data_getter import *
import json
import pandas as pd
import cv2
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import pyimgur

CLIENT_ID = "2925471fc486adc"


def get_belt_coordinates():
    belt_data = get_current_belt_data()
    """ f = open('belt_data.json')
    belt_data = json.load(f) """
    data = []
    for belt in belt_data:
        temp_data = []
        temp_data.extend(([belt["location0"]["x"], belt["location0"]["y"]], [
            belt["location1"]["x"], belt["location1"]["y"]]))

        data.append(temp_data)

    return data


def get_machine_coordinates():
    data = get_current_factory_data()
    """ f = open('data.json')
    data = json.load(f) """
    machine_data = []
    for machine in data:
        temp_data = [machine['location']['x'],
                     machine['location']['y'], machine['building'], machine['production'][0]]
        machine_data.append(temp_data)
    return machine_data


def get_max_x_y(list):
    max_x = list[0][0]
    max_y = list[0][1]
    for machine in list:
        if(machine[0] > max_x):
            max_x = machine[0]
        if(machine[1] > max_y):
            max_y = machine[1]
    return max_x, max_y


def get_min_x_y(list):
    min_x = list[0][0]
    min_y = list[0][1]
    for machine in list:
        if(machine[0] < min_x):
            min_x = machine[0]
        if(machine[1] < min_y):
            min_y = machine[1]
    return min_x, min_y


def get_mining_coordinates():
    resources = get_resource_node()
    miners = []
    for node in resources:
        if node["Exploited"]:
            miners.append([node['location']['x'], node['location']['y']])

    return miners


def surrounding_coordinates(coordinate, thickness=0):
    # Get all the x, y coordinates surrounding a coordinate
    x = coordinate[0]
    y = coordinate[1]
    coordinates = []
    for i in range(x - thickness, x + thickness + 1):
        for j in range(y - thickness, y + thickness + 1):
            coordinates.append([i, j])
    return coordinates


def draw_map(size_x=1024, size_y=1024, thickness=0):
    colors = {
        "Foundry": [0, 200, 200],
        "Smelter": [200, 200, 0],
        "Assembler": [200, 0, 200],
        "Constructor": [250, 200, 0]
    }
    miners = get_mining_coordinates()
    # Get the overall factory data
    machine_coordinate = get_machine_coordinates()
    belt_coordinate = get_belt_coordinates()
    # Normalise the max and min x and y values
    max_x, max_y = get_max_x_y(machine_coordinate)
    min_x, min_y = get_min_x_y(machine_coordinate)

    x_difference = abs((abs(max_x) - abs(min_x)))/size_x
    y_difference = abs((abs(max_y) - abs(min_y)))/size_y

    shift_x_mag = abs(min_x)
    shift_y_mag = abs(min_y)

    belt_max = get_max_x_y(belt_coordinate)
    belt_max_x, belt_max_y = belt_max[1]

    belt_diff_x = abs(abs(belt_max_x) - abs(max_x))
    belt_diff_y = abs(abs(belt_max_y) - abs(max_y))

    for machine in machine_coordinate:
        normalise_x(x_difference, shift_x_mag, machine)
        normalise_y(y_difference, shift_y_mag, machine)

    for belt in belt_coordinate:
        normalise_x(x_difference, shift_x_mag + belt_diff_x, belt[0])
        belt[0][0] += int(size_x/25)
        normalise_y(y_difference, shift_y_mag, belt[0])
        belt[0][1] += int(size_y/25)

        normalise_x(x_difference, shift_x_mag + belt_diff_x, belt[1])
        belt[1][0] += int(size_x/25)
        normalise_y(y_difference, shift_y_mag, belt[1])
        belt[1][1] += int(size_y/25)

    for miner in miners:
        normalise_x(x_difference, shift_x_mag, miner)
        miner[0] += int(size_x/25)

        normalise_y(y_difference, shift_y_mag, miner)
        miner[1] += int(size_y/25)

    max_x, max_y = get_max_x_y(machine_coordinate)
    min_x, min_y = get_min_x_y(machine_coordinate)
    print(f"Max X: {max_x}, Max Y: {max_y}")
    print(f"Min X: {min_x}, Min Y: {min_y}")

    for machine in machine_coordinate:
        machine[0] += int(size_x/25)
        machine[0] += int(size_y/25)

    data = np.zeros((max_x + int(size_x/10) + thickness, max_y +
                    int(size_y/10) + thickness, 3), dtype=np.uint8)

    """ for i in range(size_x + int(size_x/10)):
        for j in range(size_y+ int(size_y/9)):
            data[i, j] = (255,255,255) """

    for machine in machine_coordinate:
        # print(machine)
        for coordinate in surrounding_coordinates(machine, thickness=thickness):
            """ if machine[2] == 'Smelter' and machine[3]['Name'] == 'Iron Ingot' and machine[3]['CurrentProd'] < 25:
                 data[coordinate[0], coordinate[1]] = (255, 0, 0)
            else:
                 data[coordinate[0], coordinate[1]] = colors[machine[2]] """
            data[coordinate[0], coordinate[1]] = colors[machine[2]]

    for miner in miners:
        for coordinate in surrounding_coordinates(miner, thickness=thickness):
            data[coordinate[0], coordinate[1]] = (255, 255, 255)
    # Get all coordinates that form the shortest path two coordinates in belt_coordinates
    # and draw a line between them

    # print(belt_coordinate)

    for belt in belt_coordinate:
        """ data[belt[0][0], belt[0][1]] = [255, 255, 255]
        data[belt[1][0], belt[1][1]] = [255, 255, 255] """
        cv2.line(data, (belt[0][1], belt[0][0]),
                 (belt[1][1], belt[1][0]), (0, 255, 255))

    fig, ax = plt.subplots()
    ax.set_facecolor('#ffffff')
    ax.axis('off')
    fig.set_facecolor('#ffffff')
    plt.imshow(data)
    plt.savefig(os.path.join('assets', 'map.png'), bbox_inches='tight')
    return 'map.png'
    # plt.show()


def save_map(x, y, delta):
    PATH = draw_map(x, y, delta)
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    print(uploaded_image.link)


def normalise_y(y_difference, shift_y_mag, item):
    item[1] -= shift_y_mag
    item[1] /= y_difference
    item[1] = int(item[1])


def normalise_x(x_difference, shift_x_mag, item):
    item[0] += shift_x_mag
    item[0] /= x_difference
    item[0] = int(item[0])


def get_dependencies():
    #data = get_current_factory_data()
    # Open the JSON file 'data.json' and assign it to variable data
    with open('data.json', 'r') as f:
        data = json.load(f)
    dependencies = []
    G = nx.Graph()
    counter = {}
    for machine in data:
        name = []

        for product in machine["production"]:
            name.extend(word[0] for word in product["Name"].split(" "))
        name = ''.join(name)

        if machine["building"] not in counter:
            counter[machine["building"]] = 0
        else:
            counter[machine["building"]] += 1

        # print(counter)
        """ machinetemp = {"building": machine["building"] +
                       name + str(counter[machine["building"]]), "output": []} """
        machinetemp = {"building": machine["building"] +
                       name, "output": []}

        for product in machine["production"]:
            machinetemp["output"].append(product["Name"])

        machinetemp["input"] = []
        for ingredient in machine["ingredients"]:
            machinetemp["input"].append(ingredient["Name"])
        dependencies.append(machinetemp)

    with open('dependencies.json', 'w', encoding='utf-8') as f:
        json.dump(dependencies, f, ensure_ascii=False, indent=4)

    # Example JSON: {'building': 'Assembler', 'output': ['Reinforced Iron Plate'], 'input': ['Iron Plate', 'Screw']}, {'building': 'Assembler', 'output': ['Rotor'], 'input': ['Iron Rod', 'Screw']}, {'building': 'Assembler', 'output': ['Smart Plating'], 'input': ['Reinforced Iron Plate', 'Rotor']}, {'building': 'Assembler', 'output': ['Smart Plating'], 'input': ['Reinforced Iron Plate', 'Rotor']}
    # Parse pairwise through the JSON and add edges to the graph if the output of one machine is the input of another
    for machine in dependencies:
        for machine2 in dependencies:
            for output in machine["output"]:
                if output in machine2["input"]:
                    G.add_edge(machine["building"],
                               machine2["building"], length=100)

    #fig = plt.figure()
    nx.draw_networkx(G, arrows=True, font_size=8)
    # fig.set_facecolor('#000000')
    # Draw the graph
    plt.savefig(os.path.join('assets', 'dependencies.png'),
                bbox_inches='tight')
    # plt.show()

    # print(counter)
    # print(dependencies)

    return(dependencies)


#get_dependencies()


#draw_map(1000, 1000, 3)
#save_map(500, 500, 2)
