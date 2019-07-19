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
    
All these commands are configurable in services_mapping.json
        

To run the program first install the dependencies from requirements.txt

    pip install -r requirements.txt
    

To Run the program and set the cron
    
    python set_cron.py
    
Finally open a terminal to run all above mentioned commands 
