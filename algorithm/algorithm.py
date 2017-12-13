#!/usr/bin/python3

import math
import os
from shapely.geometry import Polygon
from shapely.ops import transform
from shapely.affinity import rotate
from matplotlib import pyplot

PLOT_EACH_PROBLEM = False
SAVE_PROBLEM = True
VISUALISATION_FOLDER = os.path.join(os.path.dirname(__file__), "../outputs/output_visualisations_{}/")
VISUALISATION_FILENAME = "{}.jpg"

USE_SNAPPING_TECHNIQUE = True
STEP_MULTIPLIER_PERCENTAGE = 5
USE_SCAN_TECHNIQUE = True

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
    furniture.sort(key=lambda x: x[0] * Polygon(x[1]).area, reverse=True)
    furniture_in_room = []
    furniture_in_room_polygons = []
    room_polygon = Polygon(room)
    counter = 1
    for f in furniture:
        print("Problem {}, {}/{}".format(count, counter, len(furniture)), end="\r")
        if type(room_polygon) is Polygon:
            room_polygon,coords = fits_in_room(room_polygon, furniture_in_room_polygons, Polygon(f[1]))
        else:
            for i in room_polygon:
                result = fits_in_room(i, furniture_in_room_polygons, Polygon(f[1]))
                if result[1]:
                    room_polygon,coords = result
                    break
        if coords:
            furniture_in_room.append(list(zip(*coords.exterior.xy)))
            furniture_in_room_polygons.append(coords)
        counter += 1
    if PLOT_EACH_PROBLEM or SAVE_PROBLEM:
        plot(count, version, room, [Polygon(room)] + furniture_in_room_polygons)
    return furniture_in_room

# Parameters:
#   room_polygon: Polygon
#   furniture_in_room_polygons: [Polygon]
#   f: Polygon
# Returns:
#   (Polygon, None) or (Polygon, Polygon)
def fits_in_room(room_polygon, furniture_in_room_polygons, f):
    if f.area > room_polygon.area:
        return (room_polygon, None)
    for i in transformations(f, room_polygon.bounds[0], room_polygon.bounds[2], room_polygon.bounds[1], room_polygon.bounds[3], room_polygon):
        for j in rotations(i[0], i[1]):
            if check_with_coords(room_polygon, furniture_in_room_polygons, j):
                return (new_room_polygon(room_polygon, j), j)
    return (room_polygon, None)

# Parameters:
#   room_polygon: Polygon
#   f: Polygon
# Returns:
#   Polygon
def new_room_polygon(room_polygon, f):
    return room_polygon.difference(f)

# Parameters:
#   room: Polygon
#   furniture_in_room: [Polygon]
#   f: Polygon
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
#   f: Polygon
# Returns True or False
def is_inside(room, f):
    return f.within(room)

# Parameters:
#   f: Polygon
#   min_x: double
#   max_x: double
#   min_y: double
#   max_y: double
#   room_polygon: Polygon
# Returns Polygon
def transformations(f, min_x, max_x, min_y, max_y, room_polygon):
    if USE_SNAPPING_TECHNIQUE:
        for i in list(zip(*room_polygon.exterior.coords.xy)):
            for j in list(zip(*f.exterior.coords.xy)):
                yield (transform(lambda x,y: (x + i[0] - j[0], y + i[1] - j[1]), f), i)
    
    if USE_SCAN_TECHNIQUE:
        largest = max_x - min_x if max_x - min_x >= max_y - min_y else max_y - min_y
        step = 0.01 * STEP_MULTIPLIER_PERCENTAGE * largest
        i = min_x
        while i < max_x:
            j = min_y
            while j < max_y:
                yield (transform(lambda x,y: (x + i, y + i), f), None)
                j += step
            i += step

# Parameters:
#   f: Polygon
#   rotation_point: coordinates
#       where:
#           coordinates: (double, double)
# Returns Polygon
def rotations(f, rotation_point):
    iterator = [rotation_point] if rotation_point else []
    iterator.append("centroid")
    
    for i in iterator:
        theta = 0
        step_in_degrees = 0.1
        end = 2 * math.pi
        a,b = list(zip(*f.exterior.coords.xy))[0]
        while theta < end:
            yield rotate(f, theta, i)
            theta += step_in_degrees

# Parameters:
#   room_furniture: Polygon
#   furniture: Polygon
# Returns True or False
def no_overlap(room_furniture, furniture):
    return not room_furniture.intersects(furniture)

def plot(count, version, room, polygons):
    fig = pyplot.figure(1, figsize=(5,5), dpi=90)
    ax = fig.add_subplot(111)
    for i in polygons:
        x,y = i.exterior.xy
        ax.plot(x, y)
    ax.set_title("Version {}, Problem {}".format(version, count))
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
