#!/usr/bin/python3

from shapely.geometry import Polygon
import parser
import sys

def go(problem_filename, results_filename, output_filename):
    problem_dict = {}
    results_dict = {}
    counter = 1
    with open(problem_filename, "r") as problems:
        for line in problems:
            problem_dict[counter] = parser.divide_problem(line)
            counter += 1
    counter = -1
    with open(results_filename, "r") as results:
        for line in results:
            if counter > 0:
                results_dict[counter] = parser.parse_result(line)
            counter += 1
    for i in range(1, 31):
        if i in results_dict:
            with open(output_filename.format(i), "w") as out_file:
                out_file.write(str(problem_dict[i][0])[1:-1] + "\n")
                for j in results_dict[i]:
                    out_file.write(str(j)[1:-1] + "\n")
                out_file.write("#\n")
                furniture_areas = set()
                for j in results_dict[i]:
                    furniture_areas.add(Polygon(j).area)
                for j in problem_dict[i][1]:
                    if not Polygon(j[1]).area in furniture_areas:
                        out_file.write("{}: {}\n".format(j[0], str(j[1])[1:-1]))
    return "Done."

if __name__ == "__main__":
    try:
        print(go(sys.argv[1], sys.argv[2], sys.argv[3]))
    except Exception as e:
        print(e)
        print("Usage: {} [problem filename] [results filename] [output filename with {}]".format(sys.argv[0], "{}"))
