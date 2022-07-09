#!/usr/bin/env bash


get_os_type() {

case "$OSTYPE" in
  linux*)   os="Linux" ;;
  darwin*)  os="Mac OS" ;;
  win*)     os="Windows" ;;
  msys*)    os="MSYS / MinGW / Git Bash" ;;
  cygwin*)  os="Cygwin" ;;
  bsd*)     os="BSD" ;;
  solaris*) os="Solaris" ;;
  *)        os="Unknown: $OSTYPE" ;;
esac
echo "$os"

}

os_type=$(get_os_type)

project="aws_shortcuts"

store="$HOME/.$project"
project_path="$store/$project"
alias_file="$store/.aliases"

printf "\nOS - $os_type"
if ! [[ "$os_type" == "Linux" || "$os_type" == "Mac OS" || "$os_type" == "BSD" || "$os_type" == "Solaris" ]]; then
    echo "Unsupported OS, exiting"
    exit 1
fi

printf "\nStarted setting the project $project..."

if [[ -d "$store" ]]; then
    rm -rf "$store"
    printf "\nDeleted old files of project"
fi

mkdir -p "$store"/{"$project",logs,temp}

git clone --quiet https://github.com/sunil-saini/"$project".git "$store/temp" >/dev/null
cp -r "$store/temp"/{resources,scripts,services,requirements.txt,awss.py} $project_path

rm -rf "$store/temp"

cron="$project_path/scripts/cron.sh"

chmod +x "$cron"

printf "\nInstalling pip dependencies...\n"

python -m ensurepip --user
python -m pip install --ignore-installed -q -r "$project_path"/requirements.txt --user

printf "\nStarted Collecting data from AWS...\n\n"

if python "$project_path/awss.py"; then
    crontab -l > current_cron
    cron_line="0 */6 * * * /bin/bash $cron"
    if grep -Fxq "$cron_line" current_cron; then
        echo "Cron already set, skipping"
    else
        echo "0 */6 * * * /bin/bash -l $cron" >> current_cron
        crontab current_cron
        echo "Cron set successfully to keep updating local data from AWS periodically"
    fi
    rm current_cron
    source "$alias_file"
    echo "Project set successfully, Run default set commands and enjoy shorthand commands"
else
    echo "Error(s) in setting the project, please fix above mentioned error and run again"
fi
