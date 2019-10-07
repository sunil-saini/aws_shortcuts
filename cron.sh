#!/usr/bin/env bash

project="aws_shortcuts"

cd "$HOME/.$project/$project"

echo "Updating local data, it may take few minutes..."

python -c "from driver import update_services_data as usd; usd()"

exit 0
