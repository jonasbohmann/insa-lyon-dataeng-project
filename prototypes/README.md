These were used to test data scraping outside of Airflow.

### CNN Transcripts
We initially tried to download the content of every CNN transcript, instead of just saving the amount of times crime was mentioned in the headline of each transcript. That took way too long.

### Selenium for SteamDB
In order to get the player statistics on Steam and the viewer statistics on Twitch for GTA 5, we had to use Selenium to automate executing JavaScript in the browser's console on steamdb.info which allowed us to export the dataset as .csv

Before using the script, you have to open steamdb.info in your browser and login with Steam. Then, copy the value of the Steam OAuth Cookie into STEAM_LOGIN_COOKIE in scrape_steamdb_selenium.py