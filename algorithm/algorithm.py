#!/usr/bin/python3

PLOT_EACH_PROBLEM = True

import math
from shapely.geometry import Polygon

from matplotlib import pyplot

# Parameters:
#   problem: (room, furniture)
#       where room: [coordinates]
#             furniture: [(cost, [coordinates])]
#             cost: integer
#             coordinates: (double, double)
# Returns string
def solve_problem(problem):
    return format_answer(solve(problem[0], problem[1]))

# Parameters:
#   room: [coordinates]
#   furniture: [(cost, [coordinates])]
#       where cost: integer
#             coordinates: (double, double)
# Returns [[coordinates]]
def solve(room, furniture):
    furniture.sort(key=lambda x: x[0], reverse=True)
    furniture_in_room = []
    for f in furniture:
        coords = fits_in_room(room, furniture_in_room, f[1])
        if coords:
            furniture_in_room.append(coords)
    if PLOT_EACH_PROBLEM:
        plot([Polygon(room)] + [Polygon(f) for f in furniture_in_room])
    return furniture_in_room

# Parameters:
#   room: [coordinates]
#   furniture_in_room: [[coordinates]]
#   f: [coordinates]
# Returns None or [coordinates]
def fits_in_room(room, furniture_in_room, f):
    xs, ys = zip(*room)
    for i in transformations(f, min(xs), max(xs), min(ys), max(ys)):
        for j in rotations(i):
            if check_with_coords(room, furniture_in_room, j):
                return j
    return None

# Parameters:
#   room: [coordinates]
#   furniture_in_room: [[coordinates]]
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
#   room: [coordinates]
#   f: [coordinates]
# Returns True or False
def is_inside(room, f):
    room_polygon = Polygon(room)
    furniture_polygon = Polygon(f)
    return furniture_polygon.within(room_polygon)

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
#   room_furniture: [coordinates]
#   furniture: [coordinates]
# Returns True or False
def no_overlap(room_furniture, furniture):
    furniture_one = Polygon(room_furniture)
    furniture_two = Polygon(furniture)
    return not furniture_one.intersects(furniture_two)

def plot(polygons):
    fig = pyplot.figure(1, figsize=(5,5), dpi=90)
    ax = fig.add_subplot(111)
    for i in polygons:
        x,y = i.exterior.xy
        ax.plot(x, y)
    ax.set_title('Comparison of Ploygons')
    x_range = [-5, 15]
    y_range = [-5, 15]
    ax.set_xlim(*x_range)
    ax.set_xticks(list(range(*x_range)) + [x_range[-1]])
    ax.set_ylim(*y_range)
    ax.set_yticks(list(range(*y_range)) + [y_range[-1]])
    ax.set_aspect(1)
    pyplot.show()

def format_answer(furniture):
    result = ""
    for f in furniture:
        result += ", ".join(["({}, {})".format(x, y) for x,y in f])
        result += "; "
    return result[:-2]

'''
# Scales 2D array for increased fidelity
multiplier = 10


def solve(problem):
    furniture_list = [furniture(i[0], i[1]) for i in problem[1]]
    room = convert_to_room_array(problem[0])
    # TODO sort furniture_list
    furniture_in_room = []
    for f in furniture_list:
        if drop_furniture_into_room(room, furniture, furniture_in_room):
            furniture_in_room.append(f)
    # TODO return result

def convert_to_room_array(room_list):
    xs, ys = zip(*room_list)
    room_size = (max(xs) - min(xs), max(ys) - min(ys))
    return [[0 for j in range(multiplier * room_size[1])] for i in range(multiplier * room_size[0])]

def drop_furniture_into_room(room, furniture, furniture_in_room):
    

def try_translations(room, furniture_in_room, furniture):
    

def check_if_fits(room, furniture_in_room, furniture):
    # Check border box is in room
    if furniture.border_box 

def format_answer(result):
    # TODO
    
class furniture:
    def __init__(self, cost, verticies):
        self.cost = cost
        self.verticies = verticies
        calculate_border()
        calculate_area()
        calculate_final_cost()
        self.in_room = False
        
    def calculate_border(self):
        xs, ys = zip(*self.verticies)
        self.border_box = [(min(xs), min(ys)), (max(xs), min(ys)), (max(xs), max(ys)), (min(xs), max(ys))]

    def calculate_area(self):
        xs, ys = zip(*self.verticies)
        self.area = abs(0.5 * sum([(xs[i] * ys[i+1]) - (ys[i] * xs[i+1]) for i in range(len(self.verrticies)-1)] + [(xs[0] * ys[-1]) - (ys[0] * xs[-1])]))

    def calculate_final_cost(self):
        self.final_cost = self.area * self.cost
'''
