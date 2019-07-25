# rip_aws
Shorthand personalized commands to work faster on AWS

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

        alhz
    
All these commands are configurable in services_mapping.json
        
First configure aws secret key and access key by aws configure command because same credentials will be used to query AWS resources

To run the program first install the dependencies from requirements.txt

    pip install -r requirements.txt --user
    

To Run the program and set the cron
    
    python main.py
    
Finally open a terminal to run all above mentioned commands 
