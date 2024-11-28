import datetime
import requests
import re
import random

from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient

from bs4 import BeautifulSoup, SoupStrainer

CNN_BASE_URL = "https://transcripts.cnn.com"
CNN_TRANSCRIPT_HTML_CLASSES = ["cnnTransSubHead", "cnnBodyText"]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

DEFAULT_HEADERS = {"User-Agent": USER_AGENT}


def extract_cnn_transcript():
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    client = MongoClient("localhost", 27017, username="admin", password="admin")

    response = requests.get(f"{CNN_BASE_URL}/date/{today}", headers=DEFAULT_HEADERS)
    found_links_to_transcripts = []
    transcript_html = []

    for link in BeautifulSoup(
        response.content, "html.parser", parse_only=SoupStrainer("a")
    ):
        if link.has_attr("href"):
            if link["href"].startswith("/show/"):
                found_links_to_transcripts.append(link["href"])

    for link in found_links_to_transcripts:

        response = requests.get(f"{CNN_BASE_URL}{link}", headers=DEFAULT_HEADERS)
        transcript_html.append(response.content)

    joined_transcripts = []

    for html in transcript_html:
        page = BeautifulSoup(html, "html.parser")
        text_tags = page.find_all("p", {"class": CNN_TRANSCRIPT_HTML_CLASSES[1]})

        full_text = []

        for text_tag in text_tags:
            thing = text_tag.find_all(string=True)
            full_text.extend(thing)

        joined_transcripts.append("\n".join(full_text))

        db = client.crime_database
        db.cnn_collection.insert_one({"content": "\n".join(full_text)})

    print(joined_transcripts)
    return joined_transcripts


dag = DAG(
    dag_id="crime_rate_video_games",
    start_date=datetime.datetime.now(datetime.timezone.utc),
    schedule="@once",
)

extract_cnn = PythonOperator(
    task_id="extract_cnn_transcript",
    python_callable=extract_cnn_transcript,
    dag=dag,
)


if __name__ == "__main__":
    extract_cnn_transcript()
