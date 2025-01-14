import datetime
import pandas
import aiohttp
import asyncio

from pymongo import MongoClient
from bs4 import BeautifulSoup, SoupStrainer, Tag
from airflow import DAG
from airflow.operators.python import PythonOperator

CNN_BASE_URL = "https://transcripts.cnn.com"
CNN_TRANSCRIPT_HTML_CLASSES = ["cnnTransSubHead", "cnnBodyText"]
CRIME_KEYWORDS = [
    "crime",
    "criminal",
    "murder",
    "kill",
    "rob",
    "homicide",
    "violen",
    "felony",
    "police",
    "detective",
    "gang",
    "armed",
    "weapon",
    "gun",
    "rifle",
    "assault",
    "assassin",
    "arson",
    "bomb",
    "violence",
    "homicide",
    "theft",
    "thief",
    "manslaughter",
    "mugg",
    "pickpocket",
    "shoplift",
    "vandel",
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
DEFAULT_HEADERS = {"User-Agent": USER_AGENT}


async def async_extract_mentions_of_crime(
    date: str = None, *, session: aiohttp.ClientSession, db
):
    if not date:
        date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    response = await session.get(f"{CNN_BASE_URL}/date/{date}", headers=DEFAULT_HEADERS)

    crime_mentions = 0
    total_transcripts = 0
    all_keyword_matches = []

    for link in BeautifulSoup(
        await response.text(), "lxml", parse_only=SoupStrainer("a")
    ):
        if (
            isinstance(link, Tag)
            and link.has_attr("href")
            and link["href"].startswith("/show")
        ):
            total_transcripts += 1
            matches = {x for x in CRIME_KEYWORDS if x in link.text.lower()}

            if matches:
                crime_mentions += 1
                all_keyword_matches.extend(matches)

    db.cnn_mentions_collection.insert_one(
        {
            "date": date,
            "transcripts_with_mentions_of_crime": crime_mentions,
            "total_transcripts": total_transcripts,
            "matched_crime_keywords": all_keyword_matches,
        }
    )


# release date on Steam
async def start_extraction_from_release_of_gta_5_to_now():
    dates = (
        pandas.date_range(datetime.date(2015, 7, 17), datetime.date.today(), freq="d")
        .strftime("%Y-%m-%d")
        .to_list()
    )
    client = MongoClient(
        "mongo",
        27017,
        username="admin",
        password="admin",
    )
    db = client.media_coverage_of_crime_database

    async with aiohttp.ClientSession() as session:
        for date in dates:
            await async_extract_mentions_of_crime(date, session=session, db=db)


def run_async():
    asyncio.run(start_extraction_from_release_of_gta_5_to_now())


default_args_dict = {
    "start_date": datetime.datetime.now(datetime.timezone.utc),
    "concurrency": 1,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    dag_id="ingest_media_coverage_of_crime",
    default_args=default_args_dict,
    schedule="@weekly",
    catchup=False,
)

task_extract_cnn = PythonOperator(
    task_id="extract_cnn_from_release_of_gta_5_to_now",
    python_callable=run_async,
    dag=dag,
)

task_extract_cnn
