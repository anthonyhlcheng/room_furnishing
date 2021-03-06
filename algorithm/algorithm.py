#!/usr/bin/python3

import math
import os
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.ops import transform
from shapely.affinity import rotate
from shapely.errors import PredicateError
from matplotlib import pyplot

PLOT_EACH_PROBLEM = False
SAVE_PROBLEM = True
VISUALISATION_FOLDER = os.path.join(os.path.dirname(__file__), "../outputs/output_visualisations_{}/")
VISUALISATION_FILENAME = "{}.jpg"

USE_SNAPPING_TECHNIQUE = True
STEP_MULTIPLIER_PERCENTAGE = 5
USE_SCAN_TECHNIQUE = False
USE_TWO_CORNER_OPTIMISER = True
ROTATION_DISTANCE = 180
ORDER_BY_SCORE =  True # False for order by unit cost
EXIT_WITH_COVERAGE = 42 # Set 100 for best score

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
    if ORDER_BY_SCORE:
        furniture.sort(key=lambda x: x[0] * Polygon(x[1]).area, reverse=True)
    else:
        furniture.sort(key=lambda x: x[0], reverse=True)
    furniture_in_room = []
    furniture_in_room_polygons = []
    room_polygon = Polygon(room)
    counter = 1
    current_area = 0
    original_area = room_polygon.area
    for f in furniture:
        coverage = 100 * current_area / original_area
        if coverage > EXIT_WITH_COVERAGE:
            break
        coords = None
        print("Problem {}, {}/{}: Coverage is ".format(count, counter, len(furniture)), coverage, end="\r")
        if type(room_polygon) is MultiPolygon or type(room_polygon) is list:
            for i in room_polygon:
                result = fits_in_room(i, furniture_in_room_polygons, Polygon(f[1]))
                if result[1]:
                    coords = result[1]
                    if type(result[0]) is MultiPolygon:
                        room_polygon = [j for j in room_polygon if j != i] + [i for i in result[0]]
                    else:
                        room_polygon = [j if j != i else result[0] for j in room_polygon]
                    break
        else:
            room_polygon,coords = fits_in_room(room_polygon, furniture_in_room_polygons, Polygon(f[1]))
        if coords:
            furniture_in_room.append(list(zip(*coords.exterior.xy))[:-1])
            furniture_in_room_polygons.append(coords)
            current_area += Polygon(coords).area
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
    if USE_SNAPPING_TECHNIQUE:
        difference_polygon = room_polygon.difference(f)
        i = 0.01
        step = 0.01
        while difference_polygon.intersects(f):
            difference_polygon = room_polygon.difference(f.buffer(i, cap_style=2))
            i += step
        return difference_polygon
    else:
        return room_polygon

# Parameters:
#   room: Polygon
#   furniture_in_room: [Polygon]
#   f: Polygon
# Returns True or False
def check_with_coords(room, furniture_in_room, f):
    if is_inside(room, f):
        if USE_SCAN_TECHNIQUE:
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
    try:
        return f.within(room)
    except Exception:
        return False

# Parameters:
#   coordinates: [coordinate]
#       where:
#           coordinate: (double, double)
# Returns:
#   [(double, double), (double, double)]
def get_best_two_corners(coordinates):
    if not USE_TWO_CORNER_OPTIMISER:
        return coordinates
    results = (0, [])
    for i in range(len(coordinates) - 1):
        for j in range(i + 1, len(coordinates)):
            distance = math.sqrt((coordinates[j][0] - coordinates[i][0]) ** 2 + (coordinates[j][1] - coordinates[i][1]) ** 2)
            if distance > results[0]:
                results = (distance, [coordinates[i], coordinates[j]])
    return results[1]
 
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
        corners = get_best_two_corners(list(zip(*f.exterior.coords.xy)))
        for i in list(zip(*room_polygon.exterior.coords.xy)):
            for j in corners:
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
        step_in_degrees = 15
        end = ROTATION_DISTANCE
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
