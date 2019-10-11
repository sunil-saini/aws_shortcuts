#!/usr/bin/env bash

project="aws_shortcuts"

project_path="$HOME/.$project/$project"

printf "\nStarted collecting latest data, it may take few minutes...\n\n"

python -c "import sys;sys.path.append('$project_path');from driver import update_services_data as usd; usd()"

printf "\nLocal data is up-to-date now\n\n"

exit 0
