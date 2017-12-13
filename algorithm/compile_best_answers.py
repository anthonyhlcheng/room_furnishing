#!/usr/bin/python3

import coverage_calculator
import os

problems_file = os.path.join(os.path.dirname(__file__), "../problems.rfp")
directory_path = os.path.join(os.path.dirname(__file__), "../outputs/")
output_file = directory_path + "output_best.txt"

def write_best_answers():
    best_results = {}
    # best_results format:
    # {(resulting score, string)}
    for answer_file in os.listdir(directory_path):
        if answer_file[-4:] != ".txt":
            continue
        for i in range(1, 31):
            result = coverage_calculator.go_with_string(problems_file, directory_path + answer_file, i)
            if result:
                if result[0] >= 30:
                    if str(i) not in best_results or result[1] > best_results[str(i)][0]:
                        best_results[str(i)] = (result[1], result[2])
    with open(output_file, "w") as output:
        output.write("zaragoza\n")
        output.write("t2ri0va94ush0tdu9gpuusq64r\n")
        for i in range(1, 31):
            if str(i) in best_results:
                output.write(best_results[str(i)][1])

def show_status():
    passed = 0
    for i in range(1, 31):
        result = coverage_calculator.go(problems_file, output_file, i)
        status = "32mPASSED" if result and result[0] >= 30 else "31mFAILED"
        if result:
            passed += 1
            print("\033[{}\033[0m Problem {} - Coverage: {}%, Score: {}".format(status, i, result[0], result[1]))
        else:
            print("\033[{}\033[0m Problem {} - No result".format(status, i))
    print("Number of passed problems: {}".format(passed))

if __name__ == "__main__":
    write_best_answers()
    print("Done. Output to file {}".format(output_file))
    show_status()
