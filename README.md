# <center>Playfinder for Steam</center>

Welcome to the Steam Video Game Recommendation System initiative. This project is dedicated to building an advanced game recommendation engine utilizing the rich dataset provided by Steam. Being an integral part of the Machine Learning Operations team, we are focused on evolving our recommendation model from its initial conceptual design into a fully functional and effective tool.


## Table of Contents
1. [Project Overview](#project-overview)
2. [Challenges and Goals](#challenges-and-goals)
3. [Project Workflow](#project-workflow)
    - [Data Preparation](#data-preparation)
    - [Data Exploration](#data-exploration)
    - [API Functionality](#api-functionality)
    - [System Deployment](#system-deployment)
    - [ML Model Training](#ml-model-training)
4. [Evaluation Metrics](#evaluation-metrics)
5. [Data Resources](#data-resources)
6. [Conclusion](#conclusion)

## <center>Project Overview</center>

### Challenges and Goals

#### The Challenge

As a Data Scientist with Steam, I'm tasked with the intricate challenge of constructing a user-oriented video game recommendation system. The primary complexities I face include handling deeply nested and unstructured data, and the need to manually update product listings due to the lack of automated processes. In response, I am not only navigating these data challenges but also spearheading the creation of a bespoke API. This API is designed to efficiently manage data transformations and updates, ensuring seamless integration and accessibility of our recommendation system.


#### Goals
- Create a data-driven video game recommendation system for Steam, incorporating a user-friendly API with FastAPI for seamless access to personalized suggestions.
- Conduct an Exploratory Data Analysis (EDA) and train a machine learning model, focusing on leveraging intricate game similarity algorithms for tailored recommendations.

## Project Workflow

### Data Preparation
The project started with an MVP approach, focusing on refining and structuring our datasets - items, reviews, and games. The data transformation involved demystifying nested structures, pruning redundant columns, and dealing with missing information, all aimed at enhancing API performance and model efficiency.

### Data Exploration
I dove into each dataset with a comprehensive EDA. Steering clear of automated EDA tools as isntructed by mt superiors. I manually dissected the datasets to unearth patterns, anomalies, and relationships. This bespoke approach ensured a nuanced understanding of the data.

### API Functionality
The FastAPI framework was used to craft an API offering specific endpoints:
- `PlayTimeGenre(genre: str)`: Identifies the most popular year for a given genre.
- `UserForGenre(genre: str)`: Finds the top user and their yearly playtime for a specific genre.
- `UsersRecommend(year: int)`: Lists the top three user-recommended games for a particular year.
- `UsersNotRecommend(year: int)`: Highlights the top three games with the least recommendations for a specific year.
- `sentiment_analysis(year: int)`: Analyzes user review sentiments based on the game's release year.
  ### Machine Learning Endpoint:
- `recommend_game(game_id, top_n=5)`: Takes a product ID as input and should return a list of 5 recommended games that are similar to the input game


### System Deployment
The deployment of the API was carried out on Render due to its user-friendly interface and web accessibility.

### ML Model Training
A machine learning model was developed, focusing on game-to-game (item-to-item) similarity for generating recommendations. This model was integrated into the API, allowing users to get game suggestions.

## Resources
- [Notebooks](https://github.com/SebasArmijo/Playfinder-for-Steam/tree/master/notebooks): Make sure you unzip the data in th eprocessed folder if you want to follow the step by step.
- [Data](https://github.com/SebasArmijo/Playfinder-for-Steam/tree/master/data): Data used in our project.
- [Link to API](https://playfinder-for-steam.onrender.com/docs): Note that the datasets used were only samples of the originals since render has limited memory to work with.
- [Link to Youtube Video](https://playfinder-for-steam.onrender.com/docs)

