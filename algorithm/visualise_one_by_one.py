#!/usr/bin/python3

import algorithm
import parser
import sys
from shapely.geometry import Polygon

USE_LINEAR_SEARCH = False # If False, then binary search is used

def go(input_file, results_file, number, output_file):
    problem_info = {}
    for i in [input_file, results_file]:
        with open(i, "r") as in_file:
            for problem in in_file:
                if problem.split(":")[0].isdigit():
                    if int(problem.split(":")[0]) == number:
                        string = problem
                        problem_info[i] = problem
                        break
    if len(problem_info) != 2:
        return None
    algorithm.PLOT_EACH_PROBLEM = True
    algorithm.SAVE_PROBLEM = False
    room = parser.divide_problem(problem_info[input_file])[0]
    result = []

    if USE_LINEAR_SEARCH:
        polygons = [Polygon(room)]
        for poly in parser.parse_result(problem_info[results_file]):
            polygons.append(Polygon(poly))
            algorithm.plot("Editor", poly[0], room, polygons)
            if input("Correct? (y/n)") == "y":
                result.append(poly)
            else:
                polygons = polygons[:-1]
    else:
        polygons_list = [[Polygon(room)]]
        for poly in parser.parse_result(problem_info[results_file]):
            polygons_list.append(polygons_list[-1] + [Polygon(poly)])
    
        start_index = 1
        end_index = len(polygons_list) - 1
        while start_index < end_index:
            if start_index + 1 == end_index:
                algorithm.plot("Editor", poly[0], room, polygons_list[start_index])
                if input("Correct? (y/n)") == "y":
                    algorithm.plot("Editor", poly[0], room, polygons_list[end_index])
                    if input("Correct? (y/n)") == "y":
                        start_index += 1
                else:
                    print("Beware, something may have errored")
                    start_index -= 1
                break
            middle_index = int((end_index + start_index) / 2)
            algorithm.plot("Editor", poly[0], room, polygons_list[middle_index])
            if input("Correct? (y/n)") == "y":
                start_index = middle_index
            else:
                end_index = middle_index
        results = [list(zip(*i.exterior.xy)) for i in polygons_list[start_index]]

    with open(output_file, "w") as out_file:
        out_file.write("zaragoza\n")
        out_file.write("t2ri0va94ush0tdu9gpuusq64r\n")
        out_file.write("{}: {}\n".format(number, algorithm.format_answer(result)))
    return "Done. Written to {}".format(output_file)

if __name__ == "__main__":
    try:
        print(go(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]))
    except Exception as e:
        print(e)
        print("Usage: {} [problems file] [results file] [problem number] [output file]".format(sys.argv[0]))
