from airflow.providers.postgres.hooks.postgres import PostgresHook

POSTGRES_CONN_ID = "data_eng"


def execute_sql_with_airflow_postgres_connection_id(query, *, data=None):
    pg_hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
