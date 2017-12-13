#!/bin/bash

if [ "$1" == "" ] || [ "$2" == "" ]; then
    echo "Usage $0 [Version Number] [Version Comment]"
    exit 1
fi

./algorithm/main.py problems.rfp outputs/output_{}.txt "$1"
echo "- __Version $1__ - ${@:2}" >> README.md
./algorithm/compile_best_answers.py
