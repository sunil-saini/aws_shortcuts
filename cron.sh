#!/usr/bin/env bash

if [[ $# -eq 0 ]]
  then
    echo "aws_shortcuts project directory parameter not given"
    exit
fi
cd $1
python driver.py
