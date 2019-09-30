# aws_shortcuts
Shorthand configurable personalized commands to work faster on AWS locally

e.g. - 

List all ec2 instances

        ali
        
        instance01	i-91d62f6f	10.10.110.245	56.13.52.19	t2.small	running
        instance02	i-3b2e0ceb	10.10.110.62	56.12.36.95	t2.small	running
        instance03	i-ce62201c	10.10.110.54	56.21.41.14	t2.medium	running
        
        For any specific pattern
        
        ali instance01
        
        instance01	i-91d62f6f	10.10.110.245	56.13.52.19	t2.small	running
        
        
List all s3 buckets
        
        alb <any pattern>
        
        alb test1
        
        test1.test.bodies
        test1.test.client-logs
        test1.test.files
        
List all lambdas

        all <any pattern>
        
        all staging
        
        staging.example1
        staging.example2
        staging.example3
        
List all ssm parameters

        alp <any pattern>
        
        alp prod
        
        prod.db1.password
        prod.db2.password
        prod.db3.password
        
Get value of a particular ssm parameter

        agp <parameter>
        
        agp prod.db1.password
        
        xYvd$%sgh#
        
Get all route53 hosted DNS with their all records type

        alz <any pattern>
        
        alz example.com
        
        example.com.	Private	v1.example.com.	A	10.10.74.4	10.10.74.5
        example.com.	Private	v2.example.com.	A	10.10.75.4	10.10.75.5
    
Rename any command at any time

        awss configure
        
List all configured commands at any time
        
        awss 
        
All list commands support pattern(s), so just specify the pattern for specific result else all dataset will be returned

Steps to set the project - 
        
1. First configure aws secret key and access key by aws configure command as same credentials will be used to query AWS resources

2. Run the following command to set project with default commands

        curl -s https://raw.githubusercontent.com/sunil-saini/aws_shortcuts/master/set_aws_shortcuts.sh | bash +x
    

Connect to me for any feedback

    email - sunilsaini314@gmail.com
    linkedin - www.linkedin.com/in/sunilsaini314
    
Peace, Enjoy.
