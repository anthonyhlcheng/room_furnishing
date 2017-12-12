#!/usr/bin/python3

import sys

# Returns list:
# (room, furniture)
#   room: [(double,double)] // list of coordinates
#   furniture: [(int, [(double, double)]]
#       list of tuples, tuples contain cost and list of coordinates
def divide_problem(problem):
    room = "".join(problem.split("#")[0].split(":")[1:]).strip()
    room = [tuple(map(float, i.replace(" ", "").strip("()").split(","))) for i in room.split("),")]
    furniture = [(int(i.strip().split(":")[0]), [tuple(map(float, j.replace(" ", "").strip("()").split(","))) for j in i.strip().split(":")[1].split("),")]) for i in problem.split("#")[1].split(";")]
    return (room, furniture)

def main(input_file):
    problems = []
    with open(input_file, "r") as input_file:
        for line in input_file:
            problems.append(divide_problem(line))
    return problems

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except Exception as e:
        print(e)
        print("Usage: {} [filename]".format(sys.argv[0]))
