import sys
import aws

parameter = sys.argv[1]

aws.get_ssm_parameter_value(parameter)
