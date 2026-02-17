import json
import boto3

textract = boto3.client("textract")
s3 = boto3.client("s3")

def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["body"])
        bucket = message["bucket"]
        key = message["key"]

        response = textract.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": key
                }
            }
        )

        lines = []
        for block in response["Blocks"]:
            if block["BlockType"] == "LINE":
                lines.append(block["Text"])

        output_key = key.replace(
            "resumes/", "parsed-text/"
        ).replace(".pdf", ".txt")

        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body="\n".join(lines)
        )
