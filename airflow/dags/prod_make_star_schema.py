import pandas as pd
import datetime
import psycopg2

from timeit import default_timer as timer

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

POSTGRES_CONN_ID = "data_eng"


def get_airflow_sql_connection():
    pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    connection = pg_hook.get_conn()
    return connection


def fill_prod_star_date_dimension():
    conn = get_airflow_sql_connection()
    cur = conn.cursor()

    dates_from_gta5_release_to_now = pd.date_range(
        datetime.date(2015, 7, 17), datetime.date(2024, 12, 31), freq="d"
    ).to_list()

    data = []

    for date in dates_from_gta5_release_to_now:
        data.append(
            (
                date.strftime("%Y-%m-%d"),
                date.strftime("%d"),
                date.strftime("%A"),
                date.strftime("%m"),
                date.strftime("%B"),
                date.strftime("%Y"),
            )
        )

    records_list_template = ",".join(["%s"] * len(data))
    insert_query = "INSERT INTO prod_star_date_dimension (date, day, day_of_week, month, month_name, year) VALUES {}".format(
        records_list_template
    )

    cur.execute(insert_query, data)
    conn.commit()
    cur.close()
    conn.close()


def fill_fact_table():
    conn = get_airflow_sql_connection()
    cur = conn.cursor()
    data = []

    dates_from_gta5_release_to_now = (
        pd.date_range(datetime.date(2015, 7, 17), datetime.date(2024, 12, 31), freq="d")
        .strftime("%Y-%m-%d")
        .to_list()
    )

    for date in dates_from_gta5_release_to_now:
        t1 = timer()

        cur.execute("SELECT id FROM prod_star_date_dimension WHERE date = %s", (date,))
        date_dimension_id = cur.fetchone()[0]

        cur.execute(
            "SELECT id FROM prod_star_game_update_events_dimension WHERE date = %s",
            (date,),
        )
        result_update = cur.fetchone()
        game_update_events_dimension_id = result_update[0] if result_update else None

        cur.execute(
            "SELECT id, crime_mention_rate FROM prod_star_crime_media_coverage_dimension WHERE date = %s",
            (date,),
        )
        result_media = cur.fetchone()
        crime_media_coverage_dimension_id = result_media[0] if result_media else None
        news_mention_crime_rate = result_media[1] if result_media else 0.0

        cur.execute(
            "SELECT id FROM prod_star_crime_reports_la_dimension WHERE date = %s",
            (date,),
        )
        result_crime_reports = cur.fetchone()
        crime_reports_la_dimension_id = (
            result_crime_reports[0] if result_crime_reports else None
        )

        cur.execute(
            "SELECT players, viewers FROM staging_game_interest WHERE date = %s",
            (date,),
        )
        result_interest = cur.fetchone()
        gta_5_players = (
            result_interest[0] if result_interest and len(result_interest) == 2 else 0
        )
        gta_5_viewers = (
            result_interest[1] if result_interest and len(result_interest) == 2 else 0
        )

        cur.execute(
            "SELECT date, event_name FROM prod_star_game_update_events_dimension WHERE date = %s AND event_name IS NOT NULL",
            (date,),
        )
        result_update_exist = cur.fetchone()
        gta_5_update_on_this_day = bool(result_update_exist)

        cur.execute(
            "SELECT COUNT(id) FROM prod_star_crime_reports_la_dimension WHERE date = %s",
            (date,),
        )
        result_amount_crime = cur.fetchone()

        amount_of_crime_reports_la = (
            result_amount_crime[0] if result_amount_crime else 0
        )

        data.append(
            (
                date_dimension_id,
                game_update_events_dimension_id,
                crime_media_coverage_dimension_id,
                crime_reports_la_dimension_id,
                date,
                gta_5_players,
                gta_5_viewers,
                gta_5_update_on_this_day,
                news_mention_crime_rate,
                amount_of_crime_reports_la,
            )
        )
        t2 = timer()
        took = t2 - t1
        print(f"Filling fact table for {date} took {took} seconds")

    records_list_template = ",".join(["%s"] * len(data))
    insert_query = "INSERT INTO prod_star_fact_table (date_dimension, game_update_events_dimension, crime_media_coverage_dimension, crime_reports_la_dimension, date, gta_5_players, gta_5_viewers, gta_5_update_on_this_day, news_mention_crime_rate, amount_of_crime_reports_la) VALUES {}".format(
        records_list_template
    )
    cur.execute(insert_query, data)
    conn.commit()
    cur.close()
    conn.close()


default_args_dict = {
    "start_date": datetime.datetime.now(datetime.timezone.utc),
    "concurrency": 1,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="prod_make_star_schema",
    default_args=default_args_dict,
    schedule="@daily",
    catchup=False,
)

task_create_star_schema_tables = PostgresOperator(
    task_id="create_star_schema_tables",
    postgres_conn_id="data_eng",
    sql="sql/create_star_schema.sql",
    dag=dag,
)

task_fill_prod_star_date_dimension = PythonOperator(
    task_id="fill_prod_star_date_dimension",
    python_callable=fill_prod_star_date_dimension,
    dag=dag,
)

task_fill_game_update_events_dimension = PostgresOperator(
    task_id="fill_game_update_events_dimension",
    postgres_conn_id="data_eng",
    sql="INSERT INTO prod_star_game_update_events_dimension (date, platform, event_name) SELECT date, platform, event_name FROM staging_game_update_events;",
    dag=dag,
)

task_fill_crime_media_coverage_dimension = PostgresOperator(
    task_id="fill_crime_media_coverage_dimension",
    postgres_conn_id="data_eng",
    sql="INSERT INTO prod_star_crime_media_coverage_dimension (date, transcripts_with_mentions_of_crime, total_transcripts, crime_mention_rate) SELECT date, transcripts_with_mentions_of_crime, total_transcripts, crime_mention_rate FROM staging_crime_media_coverage;",
    dag=dag,
)

task_fill_crime_reports_la_dimension = PostgresOperator(
    task_id="fill_crime_reports_la_dimension",
    postgres_conn_id="data_eng",
    sql="INSERT INTO prod_star_crime_reports_la_dimension (record_number, date, crime_code, crime_committed_description, type_of_structure_vehicle_location_code, type_of_structure_vehicle_location_description, type_of_weapon_code, type_of_weapon_description, status_of_the_crime_code, status_of_the_crime_description, latitude, longitude) SELECT record_number, date, crime_code, crime_committed_description, type_of_structure_vehicle_location_code, type_of_structure_vehicle_location_description, type_of_weapon_code, type_of_weapon_description, status_of_the_crime_code, status_of_the_crime_description, latitude, longitude FROM staging_crime_reports_la;",
    dag=dag,
)

task_fill_star_fact_table = PythonOperator(
    task_id="fill_star_fact_table",
    python_callable=fill_fact_table,
    dag=dag,
)

(
    task_create_star_schema_tables
    >> task_fill_prod_star_date_dimension
    >> task_fill_game_update_events_dimension
    >> task_fill_crime_media_coverage_dimension
    >> task_fill_crime_reports_la_dimension
    >> task_fill_star_fact_table
)
