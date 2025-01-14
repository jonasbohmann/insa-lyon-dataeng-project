# install unzip and pymongo

FROM apache/airflow:2.10.3
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         unzip \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" pymongo
ENV AIRFLOW_CONN_DATA_ENG="postgresql://airflow:airflow@postgres-data-eng:5432/data_eng"