## Kun Won's Singapore Restaurant Recommender System
---
### Personal goals
For my capstone project for my General Assembly bootcamp, I wanted to build something meaningful and deployable which would be useful for people around me. I also had an interest in recommender systems e.g. the Youtube algorithm, which have profliferated in recent years and wanted to try my hand at building one. To these personal ends, I decided to focus on building a restaurant recommender system. This would also allow me to experience the full data science lifecycle --> defining the problem, scraping and cleaning the data, data exploration and modelling, deploying the solution, and gathering feedback from stakeholders.

### Problem Statement
According to Euromonitor, there are about 28,000 food retail outlets in Singapore as of 2018, with total worth about S$8.3bn and this is expected to grow by 2.1% CAGR to 2023. The proliferation of choice for consumers has a downside - difficulty in distinguishing a quality restaurant from the pack. Many still rely on word-of-mouth or food blogs for recommendations. A few recommender systems which serve the local market have been developed, but they have weaknesses. 
* Google Maps have the largest database of restaurant and review data, but it tries to do too much. As a result, the interface is difficult to use (combines restaurants/shops/attraction data alongside a map) and resource intensive (navigating the map to load recommendations is noticeably laggy). The ranking algorithm also does not weight review rating high enough (perhaps in order to prioritise distance and diversity), often delivering restaurants with less than 3 stars within the first 10 recommendations despite there being many other 3-4 star restaurants for the query. 
* Chope focuses on high-end restaurants and has a small database (roughly ~1,000) 
* Tripadvisor reviews largely come from tourists and may not be reflective of tastes of the local population.
* Grab/Foodpanda and other delivery apps focus on the delivery market. 

To this end, I seek to build a restaurant recommender system which takes in as its input restaurants that users like and outputs similar restaurants that users may also like. 

The goals of the system are as follows:

1. Simplicity - it should be relatively easy to use and quickly get recommendations
2. Relevance - it should recommend similar restaurants, as measured by whether the restaurants recommended share similar dishes with the input restaurant
3. Quality - the system should prioritise higher rated restaurants over others within a certain threshold of relevance.

### Summary of Methodology
1. Data scraping - used third-party API (Apify) to scrape data from Google Maps
2. Data cleaning - removed permanently closed restaurants, non-restaurants, retrieved geographical coordinates of restaurants using OneMap API. Cleaned review text using NLTK, Gensim and Spacy (kept only nouns and adjectives, removed stopwords, lemmatised text and generated bigrams, trigrams). 
3. Data exploration - Checked geographical and cuisine spread of restaurants using Matplotlib and Plotly as enabled by the OneMap API. 
4. Topic Modelling - For restaurants labelled with the undescriptive category 'Restaurant', used topic modelling (Gensim) on the review data to classify these restaurants. 
5. Recommender system - Used TFIDFVectorizer on review data and generated Cosine Similarity Matrix for restaurants. Built recommender system to sieve out top 50 restaurants by similarity, rank them by rating score and number of reviews, and spit out 10 recommendations. Used K-means clustering to allow filtering by location. 
6. Deployed app using Flask and HTML, hosted on Heroku.


### Findings
The model had a Precision @ K of 0.66 compared to the baseline random recommender which had a P@K of 0.14.

### App
Try the deployed app at http://kw-restaurant-recommender-app.herokuapp.com

### Future Improvements
* Evaluate the precision of other similarity functions such as Jaccard Similarity
* Refine stopwords and NLP to better topic model remaining restaurants which were not classified well in the first instance

### Repo Contents
Code Folder
* [`01_data_cleaning.ipynb`](./code/01_data_collection.ipynb)
* [`02_eda.ipynb`](./code/02_data_cleaning.ipynb)
* [`03_topic_modelling.ipynb`](./code/03_topic_modelling.ipynb)
* [`04_recommender_model.ipynb`](./code/04_recommender_model.ipynb)

Images Folder 

* Images used for presentation

Presentation Folder

* [`slides.pdf`](./presentation/slides.pdf): Slides used for presentation

### Data Dictionary
The project used scraped data of 5,990 restaurants in Singapore from Google Maps, along with 220,000 reviews (max 50 per restaurant). The raw data was split into two csv files - restaurants.csv and reviews.csv, which have been excluded from the Github due to size.

`restaurants.csv`

| Feature     | Type    | Description                                                    |
|:-----------:|:-------:|----------------------------------------------------------------|
| title       | object  | Restaurant name                                                |
| category    | object  | Restaurant category                                            |
| address     | object  | Restaurant address                                             |
| locatedin   | object  | Building in which restaurant is located in                     |
| street      | object  | Street location                                                |
| city        | object  | City location                                                  |
| postalcode  | object  | Postal Code                                                    |
| countrycode | object  | Country Code                                                   |
| website     | object  | Website of restaurant                                          |
| url         | object  | Google Maps URL for restaurant                                 |
| phone       | object  | Phone number for restaurant                                    |
| permclosed  | bool    | True indicating restaurant is permanently closed               |
| ad          | bool    | True indicating restaurant listing is a paid ad on Google Maps |
| score       | float64 | Average rating                                                 |
| placeid     | object  | Unique ID for restaurant                                       |
| lat         | float64 | Latitude of restaurant                                         |
| lng         | float64 | Longitude of restaurant                                        |
| reviewsno   | float64 | Total number of reviews                                        |
| onestar     | float64 | Number of 1-star reviews                                       |
| twostar     | float64 | Number of 2-star reviews                                       |
| threestar   | float64 | Number of 3-star reviews                                       |
| fourstar    | float64 | Number of 4-star reviews                                       |
| fivestar    | float64 | Number of 5-star reviews                                       |

`reviews.csv`

| Feature | Type    | Description              |
|:-------:|:-------:|--------------------------|
| title   | object  | Restaurant name          |
| placeid | object  | Unique ID for restaurant |
| revname | object  | Reviewer name            |
| revid   | object  | Unique ID for reviewer   |
| revdate | object  | Review timestamp         |
| revtext | object  | Review text              |
| stars   | float64 | Rating for review        |


