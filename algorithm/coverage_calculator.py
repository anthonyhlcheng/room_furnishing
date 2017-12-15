#!/usr/bin/python3

from shapely.geometry import Polygon
import parser
import sys

# Parameters:
#   input_file: string
#   output_file: string
#   number: integer
# Returns:
#   (coverage, resulting_cost)
#       where coverage: double
#             resulting_cost: double
# Or returns None
def go(input_file, output_file, number):
    result = go_with_string(input_file, output_file, number)
    if not result:
        return None
    return (result[0], result[1])

# Parameters:
#   input_file: string
#   output_file: string
#   number: integer
# Returns:
#   (coverage, resulting_cost, string)
#       where coverage: double
#             resulting_cost: double
# Or returns None
def go_with_string(input_file, output_file, number):
    problem_info = {}
    for i in [input_file, output_file]:
        with open(i, "r") as in_file:
            for problem in in_file:
                if problem.split(":")[0].isdigit():
                    if int(problem.split(":")[0]) == number:
                        string = problem
                        problem_info[i] = problem
                        break
    if len(problem_info) != 2:
        return None
    return calculate(parser.divide_problem(problem_info[input_file]), parser.parse_result(problem_info[output_file])) + (string,)

# Parameters:
#   original_problem: (room, furniture)
#       where room: [coordinates]
#             furniture: [(cost, [coordinates])]
#             cost: integer
#             coordinates: (double, double)
#   result: [[coordinates]]
# Returns:
#   (coverage, resulting_cost)
#       where coverage: double
#             resulting_cost: double
def calculate(original_problem, result):
    coverage = 0
    resulting_cost = 0
    costs = {round(Polygon(f).area, 5) : cost for cost,f in original_problem[1]}
    for i in map(Polygon, result):
        coverage += i.area
        resulting_cost += costs[round(i.area, 5)] * i.area
    coverage /= Polygon(original_problem[0]).area
    coverage *= 100
    return (round(coverage, 2), round(resulting_cost, 3))

if __name__ == "__main__":
    try:
        print(go(sys.argv[1], sys.argv[2], int(sys.argv[3])))
    except Exception as e:
        print(e)
        print("Usage: {} [problem filename] [output filename] [problem number]".format(sys.argv[0]))
