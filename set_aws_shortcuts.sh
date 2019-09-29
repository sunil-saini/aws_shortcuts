#!/usr/bin/env bash

project="aws_shortcuts"
echo "Detected OS - $OSTYPE"
if ! [[ "$OSTYPE" == darwin* || "$OSTYPE" == "linux-gnu" ]]; then
    echo "Unsupported OS, exiting"
    exit 1
fi

echo "Started setting the project..."

mkdir -p "$HOME/.$project"
mkdir -p "$HOME/.$project/logs"
cd "$HOME/.$project"

if [[ -d "$project" ]]; then
    cd "$project"
    git pull --quiet origin master >/dev/null
else
    git clone --quiet https://github.com/sunil-saini/"$project".git >/dev/null
    cd "$project"
fi

cron="$HOME/.$project/$project/cron.sh"

chmod +x "$cron"
echo "Installing pip dependencies..."
python -m pip install --ignore-installed -q -r requirements.txt --user

echo "Started collecting data from AWS, it may take few minutes..."
python driver.py
echo "Data collected successfully"

crontab -l > current_cron
cron_line="0 */2 * * * /bin/bash $cron"
if grep -Fxq "$cron_line" current_cron; then
    echo "Cron already set, skipping"
else
    echo "0 */2 * * * /bin/bash $cron" >> current_cron
    crontab current_cron
    rm current_cron
    echo "Cron set successfully to keep updating data from AWS periodically"
fi

echo "Project set successfully, open new terminal tab and enjoy the shortcut commands"
