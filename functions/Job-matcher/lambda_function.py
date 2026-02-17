import json
import boto3

dynamodb = boto3.resource('dynamodb')
resume_table = dynamodb.Table("Resumes")
job_table = dynamodb.Table("Jobs")

def jaccard_similarity(resume_skills, job_skills):
    set1 = set(resume_skills)
    set2 = set(job_skills)
    return len(set1 & set2) / len(set1 | set2)

def lambda_handler(event, context):
    resume_id = event["resumeId"]

    resume = resume_table.get_item(
        Key={"resumeId": resume_id}
    )["Item"]

    resume_skills = resume.get("skills", [])

    jobs = job_table.scan()["Items"]

    matches = []
    for job in jobs:
        score = jaccard_similarity(
            resume_skills,
            job["requiredSkills"]
        )
        if score > 0:
            matches.append({
                "jobId": job["jobId"],
                "jobTitle": job["jobTitle"],
                "matchScore": round(score, 2)
            })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "resumeId": resume_id,
            "matches": sorted(matches, key=lambda x: x["matchScore"], reverse=True)
        })
    }
