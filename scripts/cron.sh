#!/usr/bin/env bash

project="aws_shortcuts"

project_path="$HOME/.$project/$project"

import_project="import sys;sys.path.append('$project_path');from services import aws, common, driver"

printf "\nStarted collecting latest data, it may take few minutes...\n\n"

python -c "$import_project;driver.update_services_data()"

printf "\nLocal data is up-to-date now\n\n"

exit 0
