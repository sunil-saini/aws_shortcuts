# aws_shortcuts
Shorthand configurable personalized commands to work faster on AWS locally

e.g. - 

To list all ec2 instances

        ali
        
To list all s3 buckets
        
        alb
        
To list all lambdas

        all
        
To list all ssm parameters

        alp
        
To get value of a ssm parameter

        agp parameter
        
To get all route53 hosted zones and their resources with values

        alz
    
All these commands are configurable in commands.properties file

Steps to run the project - 
        
1. First configure aws secret key and access key by aws configure command because same credentials will be used to query AWS resources

2. Run the following command

        curl -s https://raw.githubusercontent.com/sunil-saini/aws_shortcuts/master/set_aws_shortcuts.sh | bash +x
    
Open new terminal tab and enjoy all above mentioned commands
