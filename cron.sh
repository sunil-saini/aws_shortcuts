#!/usr/bin/env bash

cd $1
git pull origin master
python driver.py
