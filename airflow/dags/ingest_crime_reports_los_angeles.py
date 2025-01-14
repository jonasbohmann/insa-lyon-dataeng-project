import datetime
import requests

from airflow import DAG
from airflow.operators.python import PythonOperator

CRIME_LA_2010_2019_URL = (
    "https://data.lacity.org/api/views/63jg-8b9z/rows.csv?accessType=DOWNLOAD"
)
CRIME_LA_2020_PRESENT_URL = (
    "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"
)
CRIME_LA_2010_2019_FILE = "la_crime_2010_2019.csv"
CRIME_LA_2020_PRESENT_FILE = "la_crime_2020_present.csv"


def download_dataset(url: str, file_name: str) -> None:
    print(f"Downloading dataset at {url}, this might take a while...")
    response = requests.get(url)

    if response.status_code == 200:
        csv_content = response.content.decode("utf-8")

        with open(file_name, "w", encoding="utf-8") as file:
            file.write(csv_content)

        print(f"Dataset successfully saved: {file_name}")


default_args_dict = {
    "start_date": datetime.datetime.now(datetime.timezone.utc),
    "concurrency": 1,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="ingest_crime_reports_los_angeles",
    default_args=default_args_dict,
    schedule="@monthly",
    catchup=False,
)

task_download_2010_2019 = PythonOperator(
    task_id="download_2010_2019_crime_reports",
    python_callable=download_dataset,
    dag=dag,
    op_kwargs={
        "file_name": f"/opt/airflow/dags/ingestion_zone/{CRIME_LA_2010_2019_FILE}",
        "url": CRIME_LA_2010_2019_URL,
    },
)

task_download_2020_present = PythonOperator(
    task_id="download_2020_present_crime_reports",
    python_callable=download_dataset,
    dag=dag,
    op_kwargs={
        "file_name": f"/opt/airflow/dags/ingestion_zone/{CRIME_LA_2020_PRESENT_FILE}",
        "url": CRIME_LA_2020_PRESENT_URL,
    },
)

task_download_2010_2019 >> task_download_2020_present
