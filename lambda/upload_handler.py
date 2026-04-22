import json
import boto3
import os
import uuid
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

BUCKET_NAME = os.environ['BUCKET_NAME']
TABLE_NAME = os.environ['TABLE_NAME']
QUEUE_URL = os.environ['QUEUE_URL']

table = dynamodb.Table(TABLE_NAME)


def validate_file(file_name, file_content):
    allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg']
    
    ext = file_name.split('.')[-1].lower()
    
    if ext not in allowed_extensions:
        return False, "Invalid file type"
    
    if len(file_content.encode()) > 5242880:
        return False, "File size exceeds 5MB"
    
    return True, "Valid"


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        file_data = body['file']
        file_name = body['file_name']

        is_valid, message = validate_file(file_name, file_data)

        if not is_valid:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": message})
            }

        file_id = str(uuid.uuid4())

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_data
        )

        table.put_item(
            Item={
                "file_id": file_id,
                "file_name": file_name,
                "status": "UPLOADED",
                "uploaded_at": str(datetime.utcnow())
            }
        )

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({
                "file_id": file_id,
                "file_name": file_name
            })
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "File uploaded successfully",
                "file_id": file_id
            })
        }

    except Exception as e:
        print(str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }
