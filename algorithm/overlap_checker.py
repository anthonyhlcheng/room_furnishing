#!/usr/bin/python3

import algorithm
import parser
import sys
from shapely.geometry import Polygon

def go(input_file, results_file, number):
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
        return "{} has no result".format(number)

    room = Polygon(parser.divide_problem(problem_info[input_file])[0])
    correct = True
    furniture = []
    algorithm.USE_SCAN_TECHNIQUE = True
    for i in parser.parse_result(problem_info[results_file]):
        new_piece = Polygon(i)
        if new_piece.within(room) and algorithm.check_with_coords(room, furniture, new_piece):
            furniture.append(new_piece)
        else:
            correct = False
    return "{} is {}correct ".format(number, "" if correct else "not ")

def go_for_all(input_file, results_file, number):
    if number == 0:
        result = ""
        for i in range(1, 31):
            result += go(input_file, results_file, i)
            result += "\n"
        return result
    else:
        return go(input_file, results_file, number)

if __name__ == "__main__":
    try:
        print(go_for_all(sys.argv[1], sys.argv[2], int(sys.argv[3])))
    except Exception as e:
        print(e)
        print("Usage: {} [problems file] [results file] [problem number]".format(sys.argv[0]))
