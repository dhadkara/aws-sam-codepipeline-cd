import json
import urllib.parse
import boto3
import os

def lambda_handler(event, context):

  # Available data provided in the event
  eventTitle = event.get("eventTitle", None)
  challengeTitle = event.get("challengeTitle", None)
  taskTitle = event.get("taskTitle", None)
  teamDisplayName = event.get("teamDisplayName", None)
  userInput = event.get("userInput", None) # <-- userInput only available if using the 'Lambda With Input' validation type
  stackOutputParams = event.get("stackOutputParams", {})

  completed = False
  message = "Not yet completed"
  client = boto3.client('s3')
  s3 = boto3.resource('s3')
  for bucket in s3.buckets.all():
    objs = bucket.meta.client.list_objects(Bucket=bucket.name);
    for o in bucket.objects.filter(Delimiter='/'):
      if "employeesalary" in bucket.name and o.key == "salaryindex.csv":
        print(o.key)
        print(bucket.name)
        #client.put_object_acl(ACL='private',Bucket=bucket.name,Key='123')
        ACL = client.get_object_acl(Bucket=bucket.name,Key=o.key) 
        print (ACL)
        for Grantee in (ACL['Grants']):
          print(Grantee['Permission'])
          if Grantee['Permission'] == 'READ':
            print ('Succeed')
            completed = True
            message = "The challenge has been completed"
  
  
  return {
    "completed": completed, # required: whether this task is completed
    "message": message, # required: a message to display to the team indicating progress or next steps
    "progressPercent": 0, # optional: any whole number between 0 and 100
    "metadata": {}, # optional: a map of key:value attributes to display to the team
  }