#!/usr/bin/env bash

project="aws_shortcuts"
printf "\nDetected OS type - $OSTYPE\n"
if ! [[ "$OSTYPE" == darwin* || "$OSTYPE" == "linux-gnu" ]]; then
    echo "Unsupported OS, exiting"
    exit 1
fi

printf "Started setting the project..."

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
printf "Installing pip dependencies..."
python -m pip install --ignore-installed -q -r requirements.txt --user

printf "\nStarted collecting data from AWS, it may take few minutes...\n"
python driver.py

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

source "$HOME/.$project/.aliases"
echo "Project set successfully, Open new terminal tab and enjoy the shortcut commands"
