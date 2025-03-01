# Report - Data Engineering Project: How does GTA V affect crime in the real world?

A project by Jonas Bohmann and Johann Adrion (Potato$alad) <br/>
Teacher: Riccardo Tommasini <br/>
Course: Foundation of Data Engineering at INSA Lyon <br/>

Report: [Link](https://github.com/jonasbohmann/insa-lyon-dataeng-project/blob/main/README.md)

Poster: [Link](https://github.com/jonasbohmann/insa-lyon-dataeng-project/blob/main/docs/poster.pdf)

## Motivation

With Grand Theft Auto 6 being right around the corner (for a few years now) we thought it would be interesting to see if its predecessor GTA V, a game that is all about comitting crimes and causing havoc in a very realistic simulation of our environment, could impact criminal behavior in our society. In order to get an answer as satisfying as possible to this question, we came up with three specific correlations we wanted to check.

## Questions

### 1. Does the release of a new GTA V update come with a spike in crime rate?

If you look at the player number trend of the biggest games out there, you'll see that new updates which bring new features can temporarily increase the current player count by a lot. We'll use this to our advantage by taking those events that lead to increased playing rates and checking if there are sparks in crime rate on the release dates (and the following days).

### 2. Is the general interest in GTA V higher, if the crime rate is up?

Of course, not everybody interested in GTA V is playing it. So in order to make our analysis as consistent as possible, we decided to also look at our initial question from a different perspective. To do that, we chose to take dates with a significant high crime rate and check the online interest in GTA V, using viewer numbers from the biggest streaming platform for video games: Twitch.

### 3. Does news coverage on crime incidents lead to more people wanting to play GTA V?

Even though a high crime rate might be generally sensed by the citizens, the general attention on crime incidents raises mainly due to news reports that are watched by most of the people. Considering that, we were also curious to see if the mentioning of violent words in e.g. a report on a crime incident on national television alone could spark the desire of people to play a violent game such as GTA V.


## Scope & Assumptions

Based on the available data and the extent of this project, we had to lower the scope of our analysis and make a few assumptions in order to be efficient, but still able to come to a meaningful conclusion. <br/>

First of all, we decided to only look at the crime data in the city of Los Angeles, which in fact, is the city that the GTA V map is based on. Since we only found exact player number data on Steam, which is a platform for PC-games, we did not consider console players in our research. <br/>

Due to a lack of information on the worldwide player spread, we also made the following assumptions to get a representative number of GTA V players in Los Angeles at a certain time: <br/>

- the amount of US GTA V players equals the worldwide percentage from https://newsletter.gamediscover.co/p/whats-the-country-split-for-players for worldwide GTA V players

- the percentage of Los Angeles GTA V players from US GTA V players equals the percentage of Los Angeles inhabitants from US inhabitants

We also took the number of current GTA V Twitch viewers as a representative indicator for the general interest in the game, for which the same assumptions are applied as for the player numbers.

## Data sources

GTA V player & Twitch viewer count: <br/>
https://steamdb.info/app/271590/charts/ <br/>

GTA V update history: <br/>
https://gta.fandom.com/wiki/Grand_Theft_Auto_V/Title_Update_Notes <br/>

Crime Data Los Angeles: <br/>
https://catalog.data.gov/dataset/crime-data-from-2010-to-2019 <br/>
https://catalog.data.gov/dataset/crime-data-from-2020-to-present <br/>

CNN news transcripts: <br/>
https://transcripts.cnn.com 

## Pipeline Architecture

![architecture](./docs/architecture.svg)

## Ingestion Phase

We started off by downloading all required data from the respective websites, which, for some datasets, turned out to be more difficult than expected.

First we downloaded the datasets for all Los Angeles crime incidents during the years of 2010-2019 and 2020-2025 from data.gov, which was fairly easy due to the data being available to download as CSV files.<br/>

In order to get a timeline of all events and updates to GTA V, we used the GTA fandom site.We parsed the HTML with BeautifulSoup to locate the table and parsed the data with Pandas.

Steam player & Twitch viewer statistics were difficult to parse. The data we want was embedded into a graph and table on steamdb.info. Parsing the raw HTML was not possible because the graphs and tables were populated with JavaScript after visiting the website. 

That meant we had to resort to using Selenium to automate visiting steamdb.info to parse and extract the player and viewer numbers for GTA 5.

The last step was to ingest statistics about how often the news mentions crime. We decided to parse every single transcript from CNN, where we checked if the headline of each show every day mentions something related to crime. We save the amount of mentions to MongoDB.

## Staging Phase

The main goal of our staging phase is to clean our raw data and move it into PostgreSQL. Pandas was used for most of the transforming, merging, cleaning and wrangling.

We had to drop a lot of unnecessary colums from the very specific LA crime police reports. Both .csv files are about 300MB, so these steps take a bit longer. We also had to convert american timestamps (Month-Day-Year) into more sensible ones.

Wrangling the other datasets was less cumbersome. For some datasets we already did some processing of the available information to enrich the data with additional dataset that would be helpful for the production phase.

All PostgreSQL tables relevant to this phase start with the `staging_` prefix.

## Production Phase

After everything was moved into PostgreSQL, we decided to create a star schema to make it easier for our data marts to query the dataset.

All production PostgreSQL tables relevant to the star schema start with the `prod_star_` prefix.
We have one fact table and four dimension tables, one of those being the Date dimension.

## Verdict

Looking at our results for the 3 questions from the beginning, honestly, you cannot specifically say that there is a real correlation between the variables we examined. However, there are passages within the visualizations (to be found on the poster) which might indicate a connection between a lot of people playing GTA V and real-time incidents happening in the city of Los Angeles that are covered by national television in certain periods. <br/>
At this point, one could investigate further by using data from more similar games while looking at a bigger region and also including console players to gain convincing results, that show the real impact of violent video games on real-time events in our society.

## Setup

### Installation

1. Make sure Docker and `docker compose` are installed.
2. Create `.env` file in the root directory, which should look like this:

    ```
    AIRFLOW_UID=501
    AIRFLOW_PROJ_DIR=./airflow
    ```

    If `id -u` returns something other than 501, adjust the .env accordingly.

3. Make sure all expected directories exist:

    `mkdir -p ./airflow/dags/ingestion_zone ./airflow/logs ./airflow/config ./airflow/plugins`

4. Run this once:

    `docker compose up airflow-init`


### Running

`docker compose up -d --build`

### Preparing for offline usage

Wait until all services are ready.

This step is optional. Offline backups of all datasets are moved into the landing zone (MongoDB and airflow/dags/ingestion_zone).

1. `./prepare_for_offline_use.sh`

### URLs

| Service    | URL                    |
| ---------- | ---------------------- |
| Airflow Dashboard   | http://localhost:8080/ |
| Mongo Express | http://localhost:8081/ |
| Jupyter Notebook    | http://localhost:8889/ |

### Passwords

| Service    | User                    |Password                    |
| ---------- | ---------------------- | ---------------------- |
| Airflow Dashboard   | airflow | airflow |
| Mongo DB | admin  | admin |
| Mongo Express | admin  | admin |

### Connection URIs

| Service    | Inside Docker Network                    | Outside Docker Network                    |
| ---------- | ---------------------- |  ---------------------- |
| PostgreSQL   | postgresql://airflow:airflow@postgres-data-eng:5432/data_eng | postgresql://airflow:airflow@localhost:50008/data_eng


### Running DAGs

All DAGs are paused after installation.

Running the `ingest_*` DAGs will populate the landing zone (MongoDB + CSVs in `airflow/dags/ingestion_zone`). The `wrangle_*` DAGs will merge, clean, transform and then move all relevant data into PostgreSQL.

The `prod_make_star_schema` transforms the data in the staging tables into a fitting star schema.

### Evaluation with Jupyter Notebook

Data analysis is done in Jupyter Notebook. The prepared `queries.ipynb` notebook executes the relevant SQL queries against the star schema to answer our questions. 

The date ranges for all generated plots can be interactively changed.
