#!/usr/bin/python3

import parser
import algorithm
import time
import sys

def start(input_file, output_file):
    with open(output_file, "w") as output:
        output.write("zaragoza\n")
        output.write("t2ri0va94ush0tdu9gpuusq64r\n")
        counter = 1
        for problem in parser.main(input_file):
            start_time = time.time()
            print("Problem {}".format(counter), end="")
            sys.stdout.flush()
            output.write("{}: {}\n".format(counter, algorithm.solve_problem(problem)))
            print(" - {} seconds".format(round(time.time() - start_time, 2)))
            counter += 1

if __name__ == "__main__":
    try:
        start(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(e)
        print("Usage: {} [input filename] [output filename]".format(sys.argv[0]))
