import pandas
import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from util import execute_sql_with_airflow_postgres_connection_id

CSV_FILE_INGESTION = "/opt/airflow/dags/ingestion_zone/gta5_update_history.csv"
CSV_FILE_CLEANED = "/opt/airflow/dags/ingestion_zone/gta5_update_history_clean.csv"
CSV_FILE = "gta5_update_history.csv"
POSTGRES_CONN_ID = "data_eng"


def clean_csv_in_landing_zone():
    df = pandas.read_csv(CSV_FILE_INGESTION)
    df["game"] = "Grand Theft Auto 5"
    df.rename(
        columns={
            "Unnamed: 0": "id",
            "Release Date": "date",
            "PS3 and Xb360": "PS3_XB360",
            "PS4 and XbOne": "PS4_XBOne",
            "PS5 and XbSeriesX|S": "PS5_XBSeriesXS",
        },
        inplace=True,
    )
    df.to_csv(CSV_FILE_CLEANED, index=False)


def move_to_postgres():
    df = pandas.read_csv(CSV_FILE_CLEANED)
    df.astype({"PS3_XB360": str, "PS4_XBOne": str, "PC": str, "PS5_XBSeriesXS": str})
    data = []

    for _, row in df.iterrows():
        if row["PS3_XB360"] and isinstance(row["PS3_XB360"], str):
            data.append((row["date"], row["game"], "PS3_XB360", row["PS3_XB360"]))

        if row["PS4_XBOne"] and isinstance(row["PS4_XBOne"], str):
            data.append((row["date"], row["game"], "PS4_XBOne", row["PS4_XBOne"]))

        if row["PC"] and isinstance(row["PC"], str):
            data.append((row["date"], row["game"], "PC", row["PC"]))

        if row["PS5_XBSeriesXS"] and isinstance(row["PS5_XBSeriesXS"], str):
            data.append(
                (row["date"], row["game"], "PS5_XBSeriesXS", row["PS5_XBSeriesXS"])
            )

    records_list_template = ",".join(["%s"] * len(data))
    insert_query = "INSERT INTO staging_game_update_events (date, game, platform, event_name) VALUES {}".format(
        records_list_template
    )

    execute_sql_with_airflow_postgres_connection_id(insert_query, data=data)


default_args_dict = {
    "start_date": datetime.datetime.now(datetime.timezone.utc),
    "concurrency": 1,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="wrangle_gta5_update_history",
    default_args=default_args_dict,
    schedule="@weekly",
    catchup=False,
)

task_clean_csv_landing_zone = PythonOperator(
    task_id="task_clean_csv_landing_zone",
    python_callable=clean_csv_in_landing_zone,
    dag=dag,
)

task_create_sql_table = PostgresOperator(
    task_id="task_create_sql_table",
    postgres_conn_id="data_eng",
    sql="CREATE TABLE IF NOT EXISTS staging_game_update_events (id INTEGER PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, date DATE, game TEXT, platform TEXT, event_name TEXT);",
    dag=dag,
)

task_move_to_postgres = PythonOperator(
    task_id="task_move_to_postgres",
    python_callable=move_to_postgres,
    dag=dag,
)

task_clean_csv_landing_zone >> task_create_sql_table >> task_move_to_postgres