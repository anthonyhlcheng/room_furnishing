#!/usr/bin/python3

import parser
import algorithm_old as algorithm
#import algorithm
import coverage_calculator
import time
import sys

def start(input_file, output_file, version):
    output_file
    with open(output_file, "w") as output:
        output.write("zaragoza\n")
        output.write("t2ri0va94ush0tdu9gpuusq64r\n")
    counter = 1
    for problem in parser.main(input_file):
        try:
            start_time = time.time()
            print("Problem {}".format(counter), end="\r")
            sys.stdout.flush()
            with open(output_file, "a") as output:
                resulting_string = algorithm.solve_problem(counter, version, problem)
                if not resulting_string.replace(" ", ""):
                    print("Problem {} not completed due to no result found".format(counter))
                    counter += 1
                    continue
                output.write("{}: {}\n".format(counter, resulting_string))
            problem_coverage_results = coverage_calculator.go(input_file, output_file, counter)
            result = "32mPASSED" if problem_coverage_results[0] >= 30 else "31mFAILED"
            print("\033[{}\033[0m Problem {}: Coverage: {}%, Score: {} - {} seconds".format(result, counter, problem_coverage_results[0], problem_coverage_results[1], round(time.time() - start_time, 2)))
            counter += 1
        except KeyboardInterrupt:
            print("Problem {} not completed due to Keyboard Interrupt".format(counter))
            sys.stdout.flush()
            counter += 1

if __name__ == "__main__":
    start(sys.argv[1], sys.argv[2].format(sys.argv[3]), sys.argv[3])
    try:
        start(sys.argv[1], sys.argv[2].format(sys.argv[3]), sys.argv[3])
    except Exception as e:
        print(e)
        print("Usage: {} [input filename] [output filename with {} inside] [version number]".format(sys.argv[0], "{}"))
