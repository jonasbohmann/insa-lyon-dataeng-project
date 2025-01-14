import io
import requests
import pandas
import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

DEFAULT_HEADERS = {"User-Agent": USER_AGENT}
URL = "https://gta.fandom.com/wiki/Grand_Theft_Auto_V/Title_Update_Notes"


def extract_update_history():
    response = requests.get(URL, headers=DEFAULT_HEADERS)

    soup = BeautifulSoup(response.content, "html.parser")
    start_of_version_history = soup.find("span", id="Version_History")
    version_history_table = start_of_version_history.find_all_next("table")

    if not version_history_table:
        return

    df = pandas.read_html(io.StringIO(str(version_history_table[0])))

    if not df:
        return

    df[0].to_csv("/opt/airflow/dags/ingestion_zone/gta5_update_history.csv")


default_args_dict = {
    "start_date": datetime.datetime.now(datetime.timezone.utc),
    "concurrency": 1,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="ingest_gta5_update_history",
    default_args=default_args_dict,
    schedule="@daily",
    catchup=False,
)

task_get_update_history = PythonOperator(
    task_id="get_update_history",
    python_callable=extract_update_history,
    dag=dag,
)

task_get_update_history
