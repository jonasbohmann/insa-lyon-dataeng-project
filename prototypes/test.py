import psycopg2

try:
    conn = psycopg2.connect("dbname='airflow' user='airflow' host='localhost' password='airflow'")
except:
    print("I am unable to connect to the database")
