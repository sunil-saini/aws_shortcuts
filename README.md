# aws_shortcuts
Shorthand configurable personalized commands to work faster on AWS locally

e.g. - 

List all EC2 instances

    ali <any pattern>
    
    instance01	i-91d62f6f	10.10.110.245	56.13.52.19	t2.small	running
    instance02	i-3b2e0ceb	10.10.110.62	56.12.36.95	t2.small	running
    instance03	i-ce62201c	10.10.110.54	56.21.41.14	t2.medium	running
    
    For any specific pattern
    
    ali 10.10.110.245
    
    instance01	i-91d62f6f	10.10.110.245	56.13.52.19	t2.small	running
    
        
List all S3 buckets
        
    alb <any pattern>
    
    alb test1
    
    test1.test.bodies
    test1.test.client-logs
    test1.test.files
        
List all Lambdas

    all <any pattern>
    
    all example
    
    staging.example1
    staging.example2
    staging.example3
        
List all SSM Parameters

    alp <any pattern>
    
    alp prod.db
    
    prod.db1.password
    prod.db2.password
    prod.db3.password
        
Get value of a particular ssm parameter

    agp <parameter>
    
    agp prod.db1.password
    
    xYvd$%sgh#
        
List all Route53 hosted DNS with their all records type

    alz <any pattern>
    
    alz example.com
    
    example.com.	Private	v1.example.com.	A	10.10.74.4	10.10.74.5
    example.com.	Private	v2.example.com.	A	10.10.75.4	10.10.75.5

List all load balancers with their port(s), instance(s), target group(s) mapping

    allb <any pattern>
    
    allb 
    
    classic     testclb     internet-facing     ['80-->80', '443-->80']     ['i-a51baa4a', 'i-e4142b1f']
    network     testnlb     internet-facing     ['80-->test-tg']    {'test-tg': [i-d21resde-->80, i-d345werds-->80]}
    

List all configured commands at any time
        
    awss 

Rename any command(s) at any time

    awss configure

Fetch latest data quickly from AWS

    awss update-data
        
Update Project codebase to latest version for new features

    awss update-project 


All list commands support pattern(s), specify the pattern for specific result else all dataset will be returned


Steps to set the project - 

1. Install aws cli https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
           
2. Configure aws secret key and access key as same credentials will be used to query AWS resources
    
       aws configure

3. Run the following command to set project with default commands

       curl -s https://raw.githubusercontent.com/sunil-saini/aws_shortcuts/master/awss.sh -o awss.sh && . ./awss.sh && rm awss.sh
    

Connect to me for any feedback

    email - sunilsaini314@gmail.com
    linkedin - www.linkedin.com/in/sunilsaini314
    
Happy Coding, Enjoy.
