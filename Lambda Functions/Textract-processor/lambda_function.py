import boto3
import logging
import time

textract = boto3.client('textract')
s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

OUTPUT_BUCKET = "cloudai-hire-resumes"
OUTPUT_PREFIX = "parsed-text/"


def lambda_handler(event, context):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    logger.info(f"Starting Textract for s3://{bucket}/{key}")

    # Start Textract job
    start_response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        }
    )

    job_id = start_response['JobId']
    logger.info(f"Textract job started: {job_id}")

    # Wait for completion
    while True:
        result = textract.get_document_text_detection(JobId=job_id)
        status = result['JobStatus']

        if status == 'SUCCEEDED':
            break
        elif status == 'FAILED':
            raise Exception("Textract job failed")
        time.sleep(2)

    # Extract text
    extracted_lines = []
    for block in result['Blocks']:
        if block['BlockType'] == 'LINE':
            extracted_lines.append(block['Text'])

    full_text = "\n".join(extracted_lines)

    output_key = OUTPUT_PREFIX + key.split('/')[-1].replace('.pdf', '.txt')

    # Save extracted text
    s3.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=output_key,
        Body=full_text.encode('utf-8'),
        ContentType='text/plain'
    )

    logger.info(f"Extracted text saved to {output_key}")

    return {
        "statusCode": 200,
        "message": "Textract completed",
        "output_key": output_key
    }
