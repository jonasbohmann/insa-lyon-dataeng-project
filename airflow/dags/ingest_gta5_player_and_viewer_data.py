import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args_dict = {
    "start_date": datetime.datetime.now(datetime.timezone.utc),
    "concurrency": 1,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="ingest_gta5_player_and_viewer_data",
    default_args=default_args_dict,
    schedule="@daily",
    catchup=False,
)

task_download_dataset = BashOperator(
    task_id="task_download_dataset",
    bash_command="curl -L -o /opt/airflow/dags/ingestion_zone/gta5-steam-twitch.zip https://www.kaggle.com/api/v1/datasets/download/miscealdata/gta5-steam-twitch",
    dag=dag,
)

task_unzip_dataset = BashOperator(
    task_id="task_unzip_dataset",
    bash_command="unzip /opt/airflow/dags/ingestion_zone/gta5-steam-twitch.zip -d /opt/airflow/dags/ingestion_zone/",
    dag=dag,
)

task_cleanup = BashOperator(
    task_id="task_cleanup",
    bash_command="rm /opt/airflow/dags/ingestion_zone/gta5-steam-twitch.zip",
    dag=dag,
)

task_download_dataset >> task_unzip_dataset >> task_cleanup
