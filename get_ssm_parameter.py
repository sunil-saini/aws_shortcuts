import sys
import rip_aws

parameter = sys.argv[1]

rip_aws.get_ssm_parameter_value(parameter)
