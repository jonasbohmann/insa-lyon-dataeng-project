# Data Engineering Project: Influence of video games on crime rate and accidents in the US

### Question #1: Spike in crime rate after new game release

NEW GAME(-UPDATE) RELEASE --> CRIME RATE ??
* Game releases from steam 
* Crime rates from data.gov

### Question #2: Correlation between game demand and crime rate

GAME DEMAND --> CRIME RATE ??
* correlating (per location):
  * crime rate (data.gov)
  * online game demand (-> reddit)

### Question #3: Effect of crime incident coverage on game demand

NEWS ON CRIME --> GAME DEMAND ??
* correlating (per location):
  * news transcripts https://transcripts.cnn.com
  * online game demand (-> reddit)


### Used datasets
Game releases from steam:
- Counter Strike 2, PUBG, Call of Duty, GTA V, Rainbow Six Siege, Apex Legends, Overwatch 2, Destiny 2, S.T.A.L.K.E.R 2, Red Dead Redemption
- Search for big updates for each game and release date
- Get player numbers for certain time amount after update release

Crime rates from data.gov:
- Cities: New York, Los Angeles, Chicago, Houston, Phoenix, Philadelphia, San Antonio, San Diego, Dallas, Austin
- New York: https://www.nyc.gov/site/nypd/stats/crime-statistics/citywide-crime-stats.page
- Los Angeles: https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data
- Chicago: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data
- Houston: https://www.houstontx.gov/police/cs/Monthly_Crime_Data_by_Street_and_Police_Beat.htm
- Phoenix: https://www.phoenix.gov/police/resources-information/crime-stats-maps
- Philadelphia: https://data.phila.gov/visualizations/crime-incidents
- (!) San Antonio: https://www.sa.gov/Directory/Departments/SAPD/Transparency-Open-Data
- San Diego: https://www.sandiego.gov/police/data-transparency/crime-statistics
- (!) Dallas: https://dallaspolice.net/resources/Pages/Crime-reports.aspx
- Austin: https://data.austintexas.gov/Public-Safety/Crime-Reports/fdj4-gpfu/about_data

Online game demand
* reddit

News transcripts
* https://transcripts.cnn.com (CNN)
* https://www.msnbc.com/transcripts (MSNBC)
* https://www.foxnews.com/transcript (Fox News)



&nbsp;
&nbsp;

<details>

<summary>Datasets</summary>


#### Datapool A: Datasets for real-life events in the US (or different countries)
- ⁠Crime Rate Los Angeles, 2020-present: https://catalog.data.gov/dataset/crime-data-from-2020-to-present
- ⁠New York City: Motor Vehicle Collisions Crashes: https://catalog.data.gov/dataset/motor-vehicle-collisions-crashes
- New York City: NYPD Arrest Data (Year to Date): https://catalog.data.gov/dataset/nypd-arrest-data-year-to-date
- ⁠All US crime datasets: https://catalog.data.gov/dataset/?q=crime&sort=views_recent+desc&ext_location=&ext_bbox=&ext_prev_extent=
- France, Crimes et délits enregistrés par les services de gendarmerie et de police depuis 2012: https://www.data.gouv.fr/fr/datasets/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012/
- ⁠All crime datasets by the German government: https://www.govdata.de/suche?q=Kriminalit%C3%A4t
- https://transcripts.cnn.com
- https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/ISDPJU
- https://github.com/notnews/cnn_transcripts?tab=readme-ov-file
- reddit
- Mass shootings: Mass shootings googlen


#### Datapool B: Datasets for Game stats (e.g on steam, stats such as current player count)
- ⁠PC Video Games Steam Charts: https://steamdb.info/charts/
- GTA 5 Historical Player Data: https://steamdb.info/app/271590/charts/
- Counter Strike Historical Player Data: https://steamdb.info/app/730/charts/
- ⁠Collection of datasets or APIs for video games: https://github.com/leomaurodesenv/game-datasets
- ⁠Video Game Sales: https://www.kaggle.com/datasets/gregorut/videogamesales
- ⁠Video Game Synopsis: https://www.kaggle.com/datasets/maso0dahmed/video-games-data
- ⁠Wikipedia, list of best selling and their release date: https://en.wikipedia.org/wiki/List_of_best-selling_video_games
- ⁠Video Game Rating by ESRB: https://www.kaggle.com/datasets/imohtn/video-games-rating-by-esrb
- Video game and aggression data: https://rdrr.io/github/profandyfield/discovr/man/video_games.html

Final Datasets (for Games A,B,C...):
- current player count
- age restriction


</details>