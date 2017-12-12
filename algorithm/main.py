#!/usr/bin/python3

import parser
import algorithm
import sys

def start(input_file, output_file):
    with open(output_file, "w") as output:
        output.write("zaragoza\n")
        output.write("t2ri0va94ush0tdu9gpuusq64r\n")
        counter = 1
        for problem in parser.main(input_file):
            output.write("{}: {}\n".format(counter, algorithm.solve_problem(problem)))
            counter += 1

if __name__ == "__main__":
    start(sys.argv[1], sys.argv[2])
    try:
        start(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(e)
        print("Usage: {} [input filename] [output filename]".format(sys.argv[0]))
