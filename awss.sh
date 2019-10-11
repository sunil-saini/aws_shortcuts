#!/usr/bin/env bash


read -r prj ec2 ec2f s3 s3f lambdas lambdasf<<< $(echo $1 $2 $3 $4 $5 $6 $7)
shift 7
read -r params paramsf get_param dns dnsf lb lbf<<< $(echo $1 $2 $3 $4 $5 $6 $7)

store="$HOME/.$prj"
alias_file="$HOME/.$prj/.aliases"

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
         cwd=$(pwd)
         cd $store/$prj
         python -c \"from aws import get_ssm_parameter_value as gspv;gspv('\$1')\"
         cd $cwd
    fi
}

$dns() {
    grep \"\$1\" \"$store/$dnsf.txt\"
}

$lb() {
    grep \"\$1\" \"$store/$lbf.txt\"
}

awss() {
cwd=$(pwd)
cd $HOME/.$prj
case \"\$1\" in
	"configure")
		cd $prj
		python -c 'from common import configure_project_commands as cpc, create_alias_functions as caf;cpc(); caf()'
		;;
	"update-data")
		$store/$prj/cron.sh
		;;
	"update-project")
		git clone --quiet https://github.com/sunil-saini/$prj.git temp >/dev/null
		cp -r temp/{*.py,*.json,*.txt,*.sh} $prj
		rm -rf temp
		cd $prj
		python -m pip install --ignore-installed -q -r requirements.txt --user
		awss update-data
		awss
		;;
	*)
		cd $prj
		python -c 'from common import read_project_current_commands as rpcc; rpcc()'
		;;
esac
cd $cwd
}""" > "$alias_file"