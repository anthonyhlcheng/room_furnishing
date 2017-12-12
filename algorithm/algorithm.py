#!/usr/bin/python3

import math
import os
from shapely.geometry import Polygon
from matplotlib import pyplot

PLOT_EACH_PROBLEM = False
SAVE_PROBLEM = True
VISUALISATION_FOLDER = os.path.join(os.path.dirname(__file__), "../output_visualisations_{}/")
VISUALISATION_FILENAME = "{}.jpg"

# Parameters:
#   counter: integer
#   version: integer
#   problem: (room, furniture)
#       where room: [coordinates]
#             furniture: [(cost, [coordinates])]
#             cost: integer
#             coordinates: (double, double)
# Returns string
def solve_problem(counter, version, problem):
    return format_answer(solve(counter, version, problem[0], problem[1]))

# Parameters:
#   count: integer
#   version: integer
#   room: [coordinates]
#   furniture: [(cost, [coordinates])]
#       where cost: integer
#             coordinates: (double, double)
# Returns [[coordinates]]
def solve(count, version, room, furniture):
    furniture.sort(key=lambda x: x[0], reverse=True)
    furniture_in_room = []
    furniture_in_room_polygons = []
    room_polygon = Polygon(room)
    counter = 1
    for f in furniture:
        print("Problem {}, {}/{}".format(count, counter, len(furniture)), end="\r")
        coords = fits_in_room(room, room_polygon, furniture_in_room_polygons, f[1])
        if coords:
            furniture_in_room.append(coords)
            furniture_in_room_polygons.append(Polygon(coords))
        counter += 1
    if PLOT_EACH_PROBLEM or SAVE_PROBLEM:
        plot(count, version, room, [room_polygon] + furniture_in_room_polygons)
    return furniture_in_room

# Parameters:
#   room: [coordinates]
#   room_polygon: Polygon
#   furniture_in_room_polygons: [Polygon]
#   f: [coordinates]
# Returns None or [coordinates]
def fits_in_room(room, room_polygon, furniture_in_room_polygons, f):
    xs, ys = zip(*room)
    for i in transformations(f, min(xs), max(xs), min(ys), max(ys)):
        for j in rotations(i):
            if check_with_coords(room_polygon, furniture_in_room_polygons, j):
                return j
    return None

# Parameters:
#   room: Polygon
#   furniture_in_room: [Polygon]
#   f: [coordinates]
# Returns True or False
def check_with_coords(room, furniture_in_room, f):
    if is_inside(room, f):
        for room_f in furniture_in_room:
            if not no_overlap(room_f, f):
                return False
        return True
    return False

# Parameters:
#   room: Polygon
#   f: [coordinates]
# Returns True or False
def is_inside(room, f):
    return Polygon(f).within(room)

# Parameters:
#   f: [coordinates]
#   min_x: double
#   max_x: double
#   min_y: double
#   max_y: double
# Returns [coordinates]
def transformations(f, min_x, max_x, min_y, max_y):
    step = 1
    for i in range(int(min_x), int(max_x) + 1, step):
        for j in range(int(min_y), int(max_y), step):
            yield [(x + i, y + i) for x,y in f]

# Parameters:
#   f: [coordinates]
# Returns [coordinates]
def rotations(f):
    theta = 0
    step = 0.1
    end = 2 * math.pi
    while theta < end:
        yield [(x * math.cos(theta) + y * math.sin(theta), y * math.cos(theta) - x * math.sin(theta)) for x,y in f]
        theta += step

# Parameters:
#   room_furniture: Polygon
#   furniture: [coordinates]
# Returns True or False
def no_overlap(room_furniture, furniture):
    furniture = Polygon(furniture)
    return not room_furniture.intersects(furniture)

def plot(count, version, room, polygons):
    fig = pyplot.figure(1, figsize=(5,5), dpi=90)
    ax = fig.add_subplot(111)
    for i in polygons:
        x,y = i.exterior.xy
        ax.plot(x, y)
    ax.set_title('Comparison of Ploygons')
    xs, ys = zip(*room)
    x_range = [int(min(xs))- 1, int(max(xs)) + 1]
    y_range = [int(min(ys)) - 1, int(max(ys)) + 1]
    ax.set_xlim(*x_range)
    ax.set_xticks(list(range(*x_range)) + [x_range[-1]])
    ax.set_ylim(*y_range)
    ax.set_yticks(list(range(*y_range)) + [y_range[-1]])
    ax.set_aspect(1)
    if PLOT_EACH_PROBLEM:
        pyplot.show()
    if SAVE_PROBLEM:
        if not os.path.exists(VISUALISATION_FOLDER.format(version)):
                os.makedirs(VISUALISATION_FOLDER.format(version))
        pyplot.savefig(VISUALISATION_FOLDER.format(version) + VISUALISATION_FILENAME.format(count), bbox_inches="tight")
    pyplot.close()

def format_answer(furniture):
    result = ""
    for f in furniture:
        result += ", ".join(["({}, {})".format(x, y) for x,y in f])
        result += "; "
    return result[:-2]
