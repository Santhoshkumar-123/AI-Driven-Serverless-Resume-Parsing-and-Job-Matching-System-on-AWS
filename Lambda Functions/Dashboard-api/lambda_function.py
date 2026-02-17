import json
import boto3

# AWS clients
dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

# DynamoDB tables
resume_table = dynamodb.Table("Resumes")
job_table = dynamodb.Table("Jobs")

# S3 bucket for reports
REPORT_BUCKET = "cloudai-hire-reports"


def jaccard_similarity(resume_skills, job_skills):
    r = set(resume_skills)
    j = set(job_skills)
    if not r or not j:
        return 0
    return len(r & j) / len(r | j)


def lambda_handler(event, context):

    # Fetch data
    resumes = resume_table.scan().get("Items", [])
    jobs = job_table.scan().get("Items", [])

    dashboard_data = []

    for r in resumes:
        resume_id = r["resumeId"]
        resume_skills = r.get("skills", [])
        experience = r.get("experience_years", "Not mentioned")
        education = r.get("education", [])

        matches = []

        # Match resume with jobs
        for job in jobs:
            score = jaccard_similarity(
                resume_skills,
                job.get("requiredSkills", [])
            )

            if score > 0:
                matches.append({
                    "jobId": job["jobId"],
                    "jobTitle": job["jobTitle"],
                    "matchScore": round(score, 2)
                })

        # --------- CREATE REPORT ----------
        report_text = f"""
Resume ID: {resume_id}

Skills:
{', '.join(resume_skills)}

Experience:
{experience}

Education:
{', '.join(education)}

Job Matches:
"""

        for m in matches:
            report_text += f"- {m['jobTitle']} ({int(m['matchScore'] * 100)}%)\n"

        report_key = f"reports/{resume_id}.txt"

        
        s3.put_object(
            Bucket=REPORT_BUCKET,
            Key=report_key,
            Body=report_text.encode("utf-8"),
            ContentType="text/plain",
            ContentDisposition="attachment"
        )

        

        report_url = f"https://{REPORT_BUCKET}.s3.amazonaws.com/{report_key}"

        # Final resume object for dashboard
        dashboard_data.append({
            "resumeId": resume_id,
            "skills": resume_skills,
            "experience_years": experience,
            "education": education,
            "matches": matches,
            "reportUrl": report_url
        })

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "resumes": dashboard_data
        })
    }
