#!/usr/bin/python3

import sys

# Returns:
#   (room, furniture)
#       where room: [(double,double)] // list of coordinates
#             furniture: [(int, [(double, double)]]
#               // list of tuples, tuples contain cost and list of coordinates
def divide_problem(problem):
    room = "".join(problem.split("#")[0].split(":")[1:]).strip()
    room = [tuple(map(float, i.replace(" ", "").strip("()").split(","))) for i in room.split("),")]
    furniture = [(int(i.strip().split(":")[0]), [tuple(map(float, j.replace(" ", "").strip("()").split(","))) for j in i.strip().split(":")[1].split("),")]) for i in problem.split("#")[1].split(";")]
    return (room, furniture)

# Returns:
#   [[coordinates]]
#       where coordinates: (double, double)
def parse_result(problem):
    return [[tuple(map(float, j.replace(" ", "").strip("()").split(","))) for j in i.split("),")] for i in problem.split(":")[1].strip().split("; ")]

# Returns list:
# [(room, temperature)]
def main(input_file):
    with open(input_file, "r") as input_file:
        for line in input_file:
            yield divide_problem(line)

if __name__ == "__main__":
    try:
        print(list(main(sys.argv[1])))
    except Exception as e:
        print(e)
        print("Usage: {} [filename]".format(sys.argv[0]))
