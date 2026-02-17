import boto3
import re
import uuid
import logging

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = "Resumes"
table = dynamodb.Table(TABLE_NAME)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SKILLS = ["python", "java", "aws", "sql", "machine learning", "cloud"]
EDUCATION_KEYWORDS = ["bachelor", "master", "b.tech", "m.tech", "degree"]


def extract_skills(text):
    text = text.lower()
    return list({skill for skill in SKILLS if skill in text})


def extract_experience(text):
    match = re.search(r'(\d+)\+?\s+years?', text.lower())
    return match.group(1) if match else "Not mentioned"


def extract_education(text):
    text = text.lower()
    return list({edu for edu in EDUCATION_KEYWORDS if edu in text})


def lambda_handler(event, context):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    logger.info(f"Processing parsed text: s3://{bucket}/{key}")

    response = s3.get_object(Bucket=bucket, Key=key)
    text = response['Body'].read().decode('utf-8')

    skills = extract_skills(text)
    experience = extract_experience(text)
    education = extract_education(text)

    resume_id = str(uuid.uuid4())

    item = {
        "resumeId": resume_id,
        "skills": skills,
        "experience_years": experience,
        "education": education
    }

    table.put_item(Item=item)

    logger.info("Resume data stored in DynamoDB")

    return {
        "statusCode": 200,
        "resumeId": resume_id,
        "skills": skills,
        "experience": experience,
        "education": education
    }
