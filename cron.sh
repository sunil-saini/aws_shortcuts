#!/usr/bin/env bash

project="aws_shortcuts"

cwd=$(pwd)
cd "$HOME/.$project/$project"

printf "\nStarted collecting latest data, it may take few minutes...\n\n"

python -c "from driver import update_services_data as usd; usd()"

printf "\nLocal data is up-to-date now\n\n"

cd "$cwd"

exit 0
