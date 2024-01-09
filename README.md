# <center>Playfinder for Steam</center>

Welcome to the Steam Video Game Recommendation System project. Our mission is to develop a sophisticated recommendation system leveraging Steam's extensive gaming data. Part of the Machine Learning Operations (MLOps) team, we're committed to transitioning our recommendation model from a conceptual phase to a fully operational state.

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
As a Steam Data Scientist, my task is to tackle the complexities of creating a user-centric video game recommendation system. The primary challenges involve managing deeply nested data and updating product listings without existing automated processes.

#### Goals
- To develop a data-driven recommendation system for video games on Steam.
- To create a user-friendly API using FastAPI, enabling easy access to our recommendations.
- To engage in thorough Exploratory Data Analysis (EDA) for a deeper understanding of data patterns and relationships.
- To train a robust machine learning model that powers our recommendation logic.
- To curate game suggestions based on intricate game similarity algorithms.

## Project Workflow

### Data Preparation
The project started with an MVP approach, focusing on refining and structuring our datasets - items, reviews, and games. The data transformation involved demystifying nested structures, pruning redundant columns, and dealing with missing information, all aimed at enhancing API performance and model efficiency.

### Data Exploration
I dove into each dataset with a comprehensive EDA. Steering clear of automated EDA tools, I manually dissected the datasets to unearth patterns, anomalies, and relationships. This bespoke approach ensured a nuanced understanding of the data.

### API Functionality
The FastAPI framework was used to craft an API offering specific endpoints:
- `PlayTimeGenre(genre: str)`: Identifies the most popular year for a given genre.
- `UserForGenre(genre: str)`: Finds the top user and their yearly playtime for a specific genre.
- `UsersRecommend(year: int)`: Lists the top three user-recommended games for a particular year.
- `UsersNotRecommend(year: int)`: Highlights the top three games with the least recommendations for a specific year.
- `sentiment_analysis(year: int)`: Analyzes user review sentiments based on the game's release year.

### System Deployment
The deployment of the API was carried out on Render due to its user-friendly interface and web accessibility.

### ML Model Training
A machine learning model was developed, focusing on game-to-game similarity for generating recommendations. This model was integrated into the API, allowing users to get game suggestions.

## Resources
- [Notebooks](https://github.com/SebasArmijo/Playfinder-for-Steam/tree/master/notebooks): Make sure you unzip the data in th eprocessed folder if you want to follow the step by step.
- [Data](https://github.com/SebasArmijo/Playfinder-for-Steam/tree/master/data): Data used in our project.
- [Link to API](https://playfinder-for-steam.onrender.com/docs): Note that the datasets used were only samples of the originals since render has limited memory to work with. 

