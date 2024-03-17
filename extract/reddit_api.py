import logging
import os
import praw
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError

load_dotenv()
logging.getLogger().setLevel(logging.INFO)

APP_ID = os.getenv("REDDIT_CLIENT_ID")
SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
USER_AGENT = 'brdev 1.0 by /u/Andremallmann'

reddit = praw.Reddit(
    client_id=APP_ID,
    client_secret=SECRET,
    user_agent=USER_AGENT,
    username=REDDIT_USERNAME,
    password=PASSWORD
)

def get_submissions_of_the_day(subreddit: str) -> str:
    subreddit = reddit.subreddit(subreddit)
    submissions_last_day = {"title": []}
    for submission in subreddit.new(limit=300):
        utc_time = submission.created
        submission_date = datetime.fromtimestamp(utc_time)

        current_time = datetime.now()
        delta = current_time - submission_date

        title = submission.title

        #get posts of the 24 hours
        if delta <= timedelta(days=1):
            submissions_last_day["title"].append(title)

    pd.DataFrame(submissions_last_day).to_csv(f"data/{subreddit}_{current_time.date()}.csv", header=False, index=False)
    return f"data/{subreddit}_{current_time.date()}.csv" #return the file path


def check_if_file_exists(bucket, content_name):
    s3 = boto3.client("s3")
    try:
        s3.head_object(Bucket=bucket, Key=content_name)
        logging.info(f"{content_name} already exists in S3")
        return False
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        return error_code == 404 #return True if the error code is 404


def to_s3_bucket(content):
    bucket = 'brdev-bucket'
    s3 = boto3.client("s3")
    content_name = os.path.basename(content)
    try:
        if(check_if_file_exists(bucket, content_name)):
            response = s3.upload_file(content, bucket, content_name)
            logging.info(f"Uploaded {content_name} to s3")
    except ClientError as e:
        logging.error(e)
        return False
    return True


to_s3_bucket(get_submissions_of_the_day("brdev"))