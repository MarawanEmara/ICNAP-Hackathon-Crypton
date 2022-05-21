from data_getter import *
import json
import pandas as pd
import cv2
import numpy as np
from matplotlib import pyplot as plt


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
        temp_data = [machine['location']['x'], machine['location']['y']]
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

    for machine in machine_coordinate:
        machine[0] += shift_x_mag
        machine[0] /= x_difference
        machine[0] = int(machine[0])
        machine[1] -= shift_y_mag
        machine[1] /= y_difference
        machine[1] = int(machine[1])

    for belt in belt_coordinate:
        belt[0][0] += shift_x_mag
        belt[0][0] /= x_difference
        belt[0][0] = int(belt[0][0])
        belt[0][0] += int(size_x/25)

        belt[0][1] -= shift_y_mag
        belt[0][1] /= y_difference
        belt[0][1] = int(belt[0][1])
        belt[0][1] += int(size_y/25)

        belt[1][0] += shift_x_mag
        belt[1][0] /= x_difference
        belt[1][0] = int(belt[1][0])
        belt[1][0] += int(size_x/25)

        belt[1][1] -= shift_y_mag
        belt[1][1] /= y_difference
        belt[1][1] = int(belt[1][1])
        belt[1][1] += int(size_y/25)

    max_x, max_y = get_max_x_y(machine_coordinate)
    min_x, min_y = get_min_x_y(machine_coordinate)
    print(f"Max X: {max_x}, Max Y: {max_y}")
    print(f"Min X: {min_x}, Min Y: {min_y}")

    for machine in machine_coordinate:
        machine[0] += int(size_x/25)
        machine[0] += int(size_y/25)

    data = np.zeros((max_x + int(size_x/10) + thickness, max_y +
                    int(size_y/10) + thickness, 3), dtype=np.uint8)
    for machine in machine_coordinate:
        for coordinate in surrounding_coordinates(machine, thickness=thickness):
            data[coordinate[0], coordinate[1]] = [0, 255, 0]

    # Get all coordinates that form the shortest path two coordinates in belt_coordinates
    # and draw a line between them

    #print(belt_coordinate)

    for belt in belt_coordinate:
        data[belt[0][0], belt[0][1]] = [0, 0, 255]
        data[belt[1][0], belt[1][1]] = [0, 0, 255]
        """ cv2.line(data, (belt[0][0], belt[0][1]),
                 (belt[1][0], belt[1][1]), (0, 255, 255)) """

    plt.imshow(data)
    plt.show()


draw_map(500, 500, 2)
