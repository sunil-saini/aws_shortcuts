#!/usr/bin/env bash

project="aws_shortcuts"

mkdir ~/."$project"

mkdir ~/."$project"/logs

cd ~/."$project"

git clone https://github.com/sunil-saini/aws_shortcuts.git

cd aws_shortcuts

pip install -r requirements.txt --user

echo "Started collecting data from AWS, it may take few minutes..."
python driver.py
python set_cron.py
echo "Collected data successfully, open new terminal tab to run the shortcut commands"