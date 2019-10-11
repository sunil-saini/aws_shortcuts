#!/usr/bin/env bash


read -r project ec2 ec2f s3 s3f lambdas lambdasf<<< $(echo $1 $2 $3 $4 $5 $6 $7)
shift 7
read -r params paramsf get_param dns dnsf lb lbf<<< $(echo $1 $2 $3 $4 $5 $6 $7)

store="$HOME/.$project"
project_path="$store/$project"
alias_file="$store/.aliases"

import_project="import sys;sys.path.append('$project_path')"

echo """
$ec2() {
    grep \"\$1\" \"$store/$ec2f.txt\"
}

$s3() {
    grep \"\$1\" \"$store/$s3f.txt\"
}

$lambdas() {
    grep \"\$1\" \"$store/$lambdasf.txt\"
}

$params() {
    grep \"\$1\" \"$store/$paramsf.txt\"
}

$get_param() {
    if [ ! -z \"\$1\" ]
    then
         python -c \"$import_project;from aws import get_ssm_parameter_value as gspv;gspv('\$1')\"
    fi
}

$dns() {
    grep \"\$1\" \"$store/$dnsf.txt\"
}

$lb() {
    grep \"\$1\" \"$store/$lbf.txt\"
}

awss() {
case \"\$1\" in
	"configure")
		python -c \"$import_project;from common import configure_project_commands as cpc, create_alias_functions as caf;cpc();caf()\"
		;;
	"update-data")
		$project_path/cron.sh
		;;
	"update-project")
		git clone --quiet https://github.com/sunil-saini/"$project".git "$store/temp" >/dev/null
		cp -r "$store/temp"/{*.py,*.json,*.txt,*.sh} $project_path
		rm -rf "$store/temp"
		python -m pip install --ignore-installed -q -r "$project_path"/requirements.txt --user
		python -c \"$import_project;from common import create_alias_functions as caf;caf()\"
		awss update-data
		awss
		;;
	*)
		python -c \"$import_project;from common import read_project_current_commands as rpcc; rpcc()\"
		;;
esac
}""" > "$alias_file"