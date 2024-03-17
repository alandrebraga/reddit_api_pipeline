from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/include')

from reddit_api import get_submissions_of_the_day, to_s3_bucket


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 16),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'reddit_to_s3',
    catchup=False,
    default_args=default_args,
    description='A simple DAG to fetch Reddit submissions and upload to S3',
    schedule_interval=timedelta(days=1),
)

def task_wrapper(subreddit):
   file_path = get_submissions_of_the_day(subreddit)
   to_s3_bucket(file_path)


start_task = DummyOperator(
   task_id="start_task",
   dag=dag
)

brdev = PythonOperator(
   task_id="brdev",
   python_callable=task_wrapper,
   op_args=["brdev"],
   dag=dag
)

cscareerquestions = PythonOperator(
   task_id="cscareerquestions",
   python_callable=task_wrapper,
   op_args=["cscareerquestions"],
   dag=dag
)

learnprogramming = PythonOperator(
   task_id="learnprogramming",
   python_callable=task_wrapper,
   op_args=["learnprogramming"],
   dag=dag
)

ExperiencedDevs = PythonOperator(
   task_id="ExperiencedDevs",
   python_callable=task_wrapper,
   op_args=["ExperiencedDevs"],
   dag=dag
)

end_task = DummyOperator(
   task_id="end_task",
   dag=dag
)

start_task >> [brdev, cscareerquestions, learnprogramming, ExperiencedDevs] >> end_task
