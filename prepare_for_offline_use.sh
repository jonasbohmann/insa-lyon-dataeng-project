#!/bin/bash

echo "Make sure all services in docker-compose.yml are running and ready."
cp ./airflow/dags/offline_ingestion_zone/* ./airflow/dags/ingestion_zone/
docker compose cp ./airflow/dags/ingestion_zone/cnn_mentions_collection.json mongo:/tmp/cnn_mentions_collection.json
docker compose exec mongo mongoimport --username admin --password admin --db media_coverage_of_crime_database --collection cnn_mentions_collection --file /tmp/cnn_mentions_collection.json --authenticationDatabase admin
echo "Datasets were copied from airflow/dags/offline_ingestion_zone to airflow/dags/ingestion_zone and MongoDB was filled with an exported collection backup."
echo "All ingest_* DAGs can be skipped now."