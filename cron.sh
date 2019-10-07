#!/usr/bin/env bash

project="aws_shortcuts"

cd "$HOME/.$project/$project"

echo "Updating local data, it may take few minutes..."

python driver.py
