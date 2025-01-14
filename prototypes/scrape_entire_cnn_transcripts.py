import datetime
import requests
import pandas
import aiohttp
import asyncio
from timeit import default_timer as timer
from pymongo import MongoClient
import motor.motor_asyncio

from bs4 import BeautifulSoup, SoupStrainer, Tag

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


async def async_download_cnn_transcripts(
    date: str = None, *, session: aiohttp.ClientSession, db
):
    if not date:
        date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    response = await session.get(f"{CNN_BASE_URL}/date/{date}", headers=DEFAULT_HEADERS)
    transcript_html = []
    to_mongodb = []

    for link in BeautifulSoup(
        await response.text(), "lxml", parse_only=SoupStrainer("a")
    ):
        if isinstance(link, Tag) and link.has_attr("href"):
            if link["href"].startswith("/show"):
                transcript_response = await session.get(
                    f"{CNN_BASE_URL}{link["href"]}", headers=DEFAULT_HEADERS
                )
                transcript_html.append(await transcript_response.text())

    for html in transcript_html:
        page = BeautifulSoup(html, "lxml")
        title = page.find("p", {"class": CNN_TRANSCRIPT_HTML_CLASSES[0]})
        text_tags = page.find_all("p", {"class": CNN_TRANSCRIPT_HTML_CLASSES[1]})

        full_text = []

        for text_tag in text_tags:
            thing = text_tag.find_all(string=True)
            full_text.extend(thing)

        to_mongodb.append(
            {"date": date, "title": title.text, "content": "\n".join(full_text)}
        )

    if to_mongodb:
        db.cnn_full_collection.insert_many(to_mongodb)


def sync_download_cnn_transcripts(date: str = None, *, db):
    if not date:
        date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    response = requests.get(f"{CNN_BASE_URL}/date/{date}", headers=DEFAULT_HEADERS)
    found_links_to_transcripts = []
    transcript_html = []

    for link in BeautifulSoup(response.content, "lxml", parse_only=SoupStrainer("a")):
        if hasattr(link, "has_attr") and link.has_attr("href"):
            if link["href"].startswith("/show"):
                found_links_to_transcripts.append(link["href"])

    for link in found_links_to_transcripts:
        response = requests.get(f"{CNN_BASE_URL}{link}", headers=DEFAULT_HEADERS)
        transcript_html.append(response.content)

    to_mongodb = []

    for html in transcript_html:
        page = BeautifulSoup(html, "lxml")
        title = page.find("p", {"class": CNN_TRANSCRIPT_HTML_CLASSES[0]})
        text_tags = page.find_all("p", {"class": CNN_TRANSCRIPT_HTML_CLASSES[1]})

        full_text = []

        for text_tag in text_tags:
            thing = text_tag.find_all(string=True)
            full_text.extend(thing)

        to_mongodb.append(
            {"date": date, "title": title.text, "content": "\n".join(full_text)}
        )

    db.cnn_full_collection.insert_many(to_mongodb)


def run_sync():
    client = MongoClient("localhost", 27017, username="admin", password="admin")
    db = client.media_coverage_of_crime_database

    dates = (
        pandas.date_range(datetime.date(2015, 4, 1), datetime.date.today(), freq="d")
        .strftime("%Y-%m-%d")
        .to_list()
    )

    for date in dates:
        t1 = timer()
        sync_download_cnn_transcripts(date, db=db)
        t2 = timer()
        took = t2 - t1
        print(f"{date} took {took:.3f} seconds")


async def run_async():
    dates = (
        pandas.date_range(datetime.date(2015, 4, 1), datetime.date.today(), freq="d")
        .strftime("%Y-%m-%d")
        .to_list()
    )
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongo",
        27017,
        username="admin",
        password="admin",
    )
    db = client.media_coverage_of_crime_database

    async with aiohttp.ClientSession() as session:
        for date in dates:
            t1 = timer()
            await async_extract_mentions_of_crime(date, session=session, db=db)
            t2 = timer()
            took = t2 - t1
            print(f"{date} took {took} seconds")


if __name__ == "__main__":
    asyncio.run(run_async())
