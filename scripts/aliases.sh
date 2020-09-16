#!/usr/bin/env bash


read -r project ec2 ec2f s3 s3f lambdas lambdasf params paramsf<<< $(echo $1 $2 $3 $4 $5 $6 $7 $8 $9)
shift 9
read -r get_param dns dnsf get_domain lb lbf cf cff<<< $(echo $1 $2 $3 $4 $5 $6 $7 $8)

store="$HOME/.$project"
project_path="$store/$project"
alias_file="$store/.aliases"
mysql_alias_file="$store/.mysqlaliases"

import_project="import sys;sys.path.append('$project_path');from services import aws, common, driver"

echo """
$ec2() {
    grep -i \"\$1\" \"$store/$ec2f.txt\"
}

$s3() {
    grep -i \"\$1\" \"$store/$s3f.txt\"
}

$lambdas() {
    grep -i \"\$1\" \"$store/$lambdasf.txt\"
}

$params() {
    grep -i \"\$1\" \"$store/$paramsf.txt\"
}

$get_param() {
    if [ ! -z \"\$1\" ]
    then
         python -c \"$import_project; aws.get_ssm_parameter_value('\$1')\"
    fi
}

$dns() {
    grep -i \"\$1\" \"$store/$dnsf.txt\"
}

$get_domain() {
    if [ ! -z \"\$1\" ]
    then
         python -c \"$import_project; common.get_domain('\$1')\"
    fi
}


$lb() {
    grep -i \"\$1\" \"$store/$lbf.txt\"
}

$cf() {
    grep -i \"\$1\" \"$store/$cff.txt\"
}

awss() {
case \"\$1\" in
	"configure")
		python -c \"$import_project;common.configure_project_commands();common.create_alias_functions()\"
		source "$alias_file"
		;;
	"update")
		$project_path/scripts/cron.sh
		;;
	"upgrade")
		git clone --quiet https://github.com/sunil-saini/"$project".git "$store/temp" >/dev/null
		cp $project_path/resources/commands.properties $project_path/resources/commands.properties.bak
		cp -r "$store/temp"/{resources,scripts,services,requirements.txt,awss.py} $project_path
		rm -rf "$store/temp"
		python -m pip install --ignore-installed -q -r "$project_path"/requirements.txt --user
		python -c \"$import_project;common.merge_properties_file();common.create_alias_functions()\"
		source "$alias_file"
		awss update
		awss
		;;
	*)
		python -c \"$import_project;common.read_project_current_commands()\"
		;;
esac
}

mysqlCommands() {
  echo "Enter host, user, password to add mysql connection alias"
  read -p "Enter command to set: " temp_sql_cmd
  read -p "Enter Host: " temp_sql_host
  read -p "Enter User: " temp_sql_user
  read -s -p "Enter password: " temp_sql_pass_1
  echo
  read -s -p "Confirm password: " temp_sql_pass_2

  if [[ \"\$temp_sql_pass_1\" == \"\$temp_sql_pass_2\" ]]; then
    security add-generic-password -a \$USER -s \"by_awss@\$temp_sql_cmd--\$temp_sql_host\" -w \"\$temp_sql_pass_1\"
    mysql_alias_file_path=\"\$HOME/.aws_shortcuts/.mysqlaliases\"

    echo \"\"\"
\$temp_sql_cmd() {
  mysql -h \"\$temp_sql_host\" -u \"\$temp_sql_user\" -p\\\$(security find-generic-password -a \\\$USER -s \"by_awss@\$temp_sql_cmd--\$temp_sql_host\" -w)
}
\"\"\" >> \"\$mysql_alias_file_path\"

    echo
    echo \"command \$temp_sql_cmd added successfully\"
  else
    echo
    echo \"passwords \$temp_sql_pass_1 & \$temp_sql_pass_2 doesn't match\"
  fi
}
""" > "$alias_file"
>"$mysql_alias_file"
