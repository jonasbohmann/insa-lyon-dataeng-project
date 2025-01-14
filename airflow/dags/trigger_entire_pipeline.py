import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule

default_args_dict = {
    "start_date": datetime.datetime.now(datetime.timezone.utc),
    "concurrency": 1,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="a_trigger_everything",
    default_args=default_args_dict,
    schedule=None,
    catchup=False,
)

trigger_ingest_crime_report = TriggerDagRunOperator(
    dag=dag,
    task_id="trigger_ingest_crime_report",
    trigger_rule=TriggerRule.ALL_SUCCESS,
    trigger_dag_id="ingest_crime_reports_los_angeles",
)

trigger_ingest_gta5_player_viewer = TriggerDagRunOperator(
    dag=dag,
    task_id="trigger_ingest_gta5_player_viewer",
    trigger_rule=TriggerRule.ALL_SUCCESS,
    trigger_dag_id="ingest_gta5_player_and_viewer_data",
)

trigger_ingest_gta5_update_history = TriggerDagRunOperator(
    dag=dag,
    task_id="trigger_ingest_gta5_update_history",
    trigger_rule=TriggerRule.ALL_SUCCESS,
    trigger_dag_id="ingest_gta5_update_history",
)

trigger_ingest_media_coverage = TriggerDagRunOperator(
    dag=dag,
    task_id="trigger_ingest_media_coverage",
    trigger_rule=TriggerRule.ALL_SUCCESS,
    trigger_dag_id="ingest_media_coverage_of_crime",
)

trigger_wrangle_crime_reports_la = TriggerDagRunOperator(
    dag=dag,
    task_id="trigger_wrangle_crime_reports_la",
    trigger_rule=TriggerRule.ALL_SUCCESS,
    trigger_dag_id="wrangle_crime_reports_los_angeles",
)

trigger_wrangle_gta5_update = TriggerDagRunOperator(
    dag=dag,
    task_id="trigger_wrangle_gta5_update",
    trigger_rule=TriggerRule.ALL_SUCCESS,
    trigger_dag_id="wrangle_gta5_update_history",
)

trigger_wrangle_gta5_player_viewer = TriggerDagRunOperator(
    dag=dag,
    task_id="trigger_wrangle_gta5_player_viewer",
    trigger_rule=TriggerRule.ALL_SUCCESS,
    trigger_dag_id="wrangle_gta5_player_and_viewer_data",
)

trigger_wrangle_media_coverage = TriggerDagRunOperator(
    dag=dag,
    task_id="trigger_wrangle_media_coverage",
    trigger_rule=TriggerRule.ALL_SUCCESS,
    trigger_dag_id="wrange_media_coverage_of_crime",
)

trigger_prod_task = TriggerDagRunOperator(
    dag=dag,
    task_id="trigger_prod_star_schema",
    trigger_rule=TriggerRule.ALL_SUCCESS,
    trigger_dag_id="prod_make_star_schema",
)

start_task = EmptyOperator(task_id="start", dag=dag)
dummy = EmptyOperator(task_id="dummy", dag=dag)
end_task = EmptyOperator(task_id="end", dag=dag)

(
    start_task
    >> [
        trigger_ingest_crime_report,
        trigger_ingest_gta5_update_history,
        trigger_ingest_gta5_player_viewer,
        trigger_ingest_media_coverage,
    ]
    >> dummy
    >> [
        trigger_wrangle_crime_reports_la,
        trigger_wrangle_gta5_update,
        trigger_wrangle_gta5_player_viewer,
        trigger_wrangle_media_coverage,
    ]
    >> trigger_prod_task
    >> end_task
)
