#!/usr/bin/env bash

project="aws_shortcuts"
printf "\nDetected OS type - $OSTYPE"
if ! [[ "$OSTYPE" == darwin* || "$OSTYPE" == "linux-gnu" ]]; then
    echo "Unsupported OS, exiting"
    exit 1
fi

printf "\nStarted setting the project..."

if ! [[ -z "$project" ]]; then
    rm -rf "$HOME/.$project"
fi

mkdir -p $HOME/."$project"/{"$project",logs,temp}


cd "$HOME/.$project"

git clone --quiet https://github.com/sunil-saini/"$project".git temp >/dev/null
cp -r temp/{*.py,*.json,*.properties,*.txt,*.sh} "$project"

rm -rf temp

cd "$project"

cron="$HOME/.$project/$project/cron.sh"

chmod +x "$cron"
printf "\nInstalling pip dependencies..."
python -m pip install --ignore-installed -q -r requirements.txt --user

printf "\nStarted collecting data from AWS, it may take few minutes...\n"

if python driver.py ; then
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
else
    echo "Error(s) in setting the project, please fix above mentioned error and run again"
fi
