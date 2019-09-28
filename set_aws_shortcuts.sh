#!/usr/bin/env bash

echo "Started setting the project..."
project="aws_shortcuts"

mkdir -p "$HOME/.$project"

mkdir -p "$HOME/.$project/logs"

cd "$HOME/.$project"

git clone --quiet https://github.com/sunil-saini/aws_shortcuts.git >/dev/null

cd "$project"
cron="$HOME/.$project/$project/cron.sh"

chmod +x "$cron"
echo "Installing pip dependencies..."
python -m pip install --ignore-installed -q -r requirements.txt --user

echo "Started collecting data from AWS, it may take few minutes..."
python driver.py
echo "Collected data successfully, open new terminal tab to run the shortcut commands"

echo "Detected OS - $OSTYPE, setting cron.."
if [[ $OSTYPE == darwin* ]]; then
    label="com.$project"
    plist="$label.plist"
    plist_path="$HOME/Library/LaunchAgents/$plist"

    cat << EOF > "$plist_path"
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
      <key>Label</key>
      <string>$label</string>

      <key>ProgramArguments</key>
      <array>
        <string>$cron</string>
      </array>

      <key>Nice</key>
      <integer>1</integer>

      <key>StartInterval</key>
      <integer>7200</integer>

      <key>RunAtLoad</key>
      <true/>

    </dict>
    </plist>
EOF
    launchctl load "$plist_path"

elif [[ "$OSTYPE" == "linux-gnu" ]]; then

    crontab -l > current_cron
    echo "0 */2 * * * /bin/bash $cron" >> current_cron
    crontab current_cron
    rm current_cron

else
    echo "Unsupported OS"
fi
