#!/usr/bin/env bash

project="aws_shortcuts"

cd "$HOME/.$project/$project"

git pull --quiet origin master >/dev/null

python driver.py
