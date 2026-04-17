import json
import boto3
import uuid
import base64
import os
import logging

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Environment variables
BUCKET_NAME = os.environ['BUCKET_NAME']
TABLE_NAME = os.environ['TABLE_NAME']

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", event)

        body = json.loads(event['body'])

        file_content = base64.b64decode(body['file'])
        file_name = body['fileName']

        file_id = str(uuid.uuid4())

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_content
        )

        logger.info("File uploaded to S3: %s", file_name)

        # Store metadata in DynamoDB
        table.put_item(
            Item={
                'fileId': file_id,
                'fileName': file_name
            }
        )

        logger.info("Metadata stored in DynamoDB with fileId: %s", file_id)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File uploaded successfully',
                'fileId': file_id
            })
        }

    except Exception as e:
        logger.error("Error: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
