#/bin/bash

rm outputs/output_best.txt
./algorithm/compile_best_answers.py
./algorithm/overlap_checker.py problems.rfp outputs/output_best.txt 0
