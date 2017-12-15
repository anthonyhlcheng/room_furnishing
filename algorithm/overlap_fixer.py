#!/usr/bin/python3

import algorithm
import parser
import sys
from shapely.geometry import Polygon

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

    room = Polygon(parser.divide_problem(problem_info[input_file])[0])
    result = []
    furniture = []
    algorithm.USE_SCAN_TECHNIQUE = True
    for i in parser.parse_result(problem_info[results_file]):
        new_piece = Polygon(i)
        if new_piece.within(room) and algorithm.check_with_coords(room, furniture, new_piece):
            furniture.append(new_piece)
            result.append(i)
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
