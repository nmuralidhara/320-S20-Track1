import json
import boto3

#written by Matt Hill
#4/8/20
#Input: email, password
#Output: 
def create_student_user(event, context):
    
    email = "testEmail"     #event['student_id']
    password = "testPassword"           #event['password']
    client = boto3.client('rds-data') #Connecting to the database
    create = client.execute_statement(
        secretArn = "arn:aws:secretsmanager:us-east-2:500514381816:secret:rds-db-credentials/cluster-33FXTTBJUA6VTIJBXQWHEGXQRE/postgres-3QyWu7",
        database = "postgres",
        resourceArn = "arn:aws:rds:us-east-2:500514381816:cluster:postgres",
        sql = "INSERT INTO users(id,first_name,last_name, email, preferred_name, picture, bio,pronouns,gender,phone,is_blocked,GCal_permission,hashed_password,salt_key) \
        VALUES ((SELECT id FROM users ORDER BY id DESC LIMIT 1)+1,'fn','ln','%s','pn','pic','bio','pro','gen','pho',false,true,'%s','salt')" % (email,password)
    )

    if(create['records'] == []): 
        print("Student user not created")
        return {
            "statusCode": 404
        }
    else:
        print("Student user created")
        return{
            'statusCode': 200,
            'body': json.dumps(create['records']) #outputs the query in JSON format 
        }