# Data Engineering Project: How does GTA V affect crime in the real world?
A project by Jonas Bohmann and Johann Adrion (Potato$alad) <br/>
Teacher: Riccardo Tommasini <br/>
Course: Foundation of Data Engineering at INSA Lyon <br/>
Poster: https://www.canva.com/design/DAGcFujhq5g/J2g5IH0500I_kRZoKcs9zQ/edit

# Motivation
With Grant Theft Auto 6 being right around the corner (for a few years now) we thought it would be interesting to see, if it's predecessor GTA V, a game that is all about comitting crimes and causing havoc in a very realistic simulation of our environment, could impact criminal behavior in our society. In order to get an answer as satisfying as possible to this question, we came up with three specific correlations we wanted to check.
### 1) Does the release of a new GTA V update come with a spike in crime rate?
If you look at the player number trend of the biggest games out there, you'll see, that new updates which bring new features can temporarily increase the current player count by a lot. We'll use this to our advantage by taking those events that lead to increased playing rates and check if there are sparks in crime rate on the release dates (and the following days).
### 2) Is the general interest in GTA V higher, if the crime rate is up?
Of course, not everybody interested in GTA V is playing it. So in order to make our analysis as consistent as possible, we decided, to also look at our initial question from a different perspective. To do that, we chose to take dates with a significant high crime rate and check the online interest in GTA V, using viewer numbers from the biggest streaming platform for video games: Twitch.
### 3) Does news coverage on crime incidents lead to more people wanting to play GTA V?
Even though a high crime rate might be generally sensed by the citizens, the general attention on crime incidents raises mainly due to news reports that are watched by most of the people. Considering that, we were also curious to see, if the mentioning of violent words in e.g. a report on a crime incident on national television alone could spark the desire of people to play a violent game such as GTA V.

# Realization
introduction on how we ended up with the data sources
## Data Sources
listing data sources
## Workflow
rough structure of the project steps (to be elaborated later)
# Project Steps
maybe insert picture
## Ingestion Phase
- download steps for every dataset
- 
## Staging Phase
- joining datasets (crime data)
- cleaning joined data set (crime data)
- conversion into table structure (update history)
- 
## Production Phase
- 
- building the star schema
