import json
import boto3
import base64
import uuid

s3 = boto3.client("s3")
sqs = boto3.client("sqs")

BUCKET_NAME = "cloudai-hire-resumes"
QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/741448924406/resume-processing-queue"

def lambda_handler(event, context):
    try:
        # Decode PDF
        file_content = base64.b64decode(event["body"])
        resume_id = str(uuid.uuid4())
        s3_key = f"resumes/{resume_id}.pdf"

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType="application/pdf"
        )

        # Send message to SQS
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({
                "bucket": BUCKET_NAME,
                "key": s3_key,
                "resumeId": resume_id
            })
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Resume uploaded & queued",
                "resumeId": resume_id
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
