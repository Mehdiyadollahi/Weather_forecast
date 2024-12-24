# Weather API

This project is a weather data pipeline that fetches weather data from Tomorrow.io's API, stores it in a PostgreSQL database, processes it using dbt to create curated datasets, and visualizes insights through a Jupyter Notebook. The setup is containerized using Docker, making it simple to deploy locally.

## Overview

In this Project we want to build a small system that scrapes the Tomorrow IO API <https://docs.tomorrow.io/reference/welcome> for forecasts and
recent weather history for a set of geographic locations. This project use the free plan and is limited the list of geolocations
at these 10 locations:

|   lat   |   lon    |
|:-------:|:--------:|
| 25.8600 | -97.4200 |
| 25.9000 | -97.5200 |
| 25.9000 | -97.4800 |
| 25.9000 | -97.4400 |
| 25.9000 | -97.4000 |
| 25.9200 | -97.3800 |
| 25.9400 | -97.5400 |
| 25.9400 | -97.5200 |
| 25.9400 | -97.4800 |
| 25.9400 | -97.4400 |

The forecasts be scraped hourly for each location on the list, and they should be available to query in a SQL
database at the end.

At the end it capable to answer the following questions using SQL:

* What's the latest temperature for each geolocation? What's the latest wind speed?
* Show an hourly time series of temperature (or any other available weather variable) from a day ago to 5 days in the
  future for a selected location.

## Components

### 1. Data Scraper (tomorrow)

The `scraper` module fetches weather forecast data and stores it in a PostgreSQL database.

#### How It Works

1. **API Call**: Uses the Tomorrow.io API to fetch weather forecast data for 10 specific locations.
2. **Database Insertion**: After retrieving the data, it stores all results in the `weather_source.weather_data` table within PostgreSQL.

#### Key Files

- **main.py**: The main script to run the data scraping and database population process. Also it calls the `dbt run` to transform data into the required report.
- **scraper.py**: Contains an asynchronous function to fetch weather data from the API, with a delay to prevent rate-limiting issues. Database utility functions to batch insert data into PostgreSQL after all API calls are existed in this file as well.
- **utils.py**: Contains the utility functions that are used during calling API or storing data into DB.

### 2. Data Transformation (tomorrow/report_models/)

The 'dbt_project' module processes raw data stored in PostgreSQL and applies data transformations to create the final weather forecast model.

#### How It Works

1. Base Model (`weather_data_base`): Extracts and cleans raw data, including fields like id, timestamp, and location.
2. Final Model (`weather_report_daily`): Filters weather data for a specific 5-day range based on the timestamp, creating a curated dataset for further analysis.

#### Key Files

- **weather_data_base.sql**: dbt model that cleans and extracts relevant fields from raw data
- **weather_report_daily.sql**: dbt model that filters data for a specified date range and applies any final transformations.
- **_model.yml**: Schema configuration for each model, defining field descriptions and tests for data quality.

### 3. Data Analysis

The 'analysis' module includes a Jupyter Notebook for analyzing the weather data.

#### How It Works

1. **Data Loading**: Loads processed data from the PostgreSQL database.
2. **Visualization**: Visualizes temperature, humidity, and other weather metrics over time 
for each location.

#### Key Files

- **analysis.ipynb**: Notebook to analyze and visualize trends in the weather data, providing insights based on the processed data in the `weather_report_daily`.

## USAGE

Build and start the containers

```shell
$ docker compose up --build
```

after starting the container, the `__main__.py` will run automatically. It fetches the data from API and then call the `dbt run` with the proper address of project and `profile.yml` to complete the transformation. There are a scheduler that call these two steps in hourly basis after the frst run.

Navigate to [localhost:8888](http://localhost:8888) to access the jupyter notebook server. open the `analysis.ipynb` notebook to explore the data.

Lastly, cleanup your system with

```shell
$ docker compose down --volumes
```

## Additional Information

- **Environment Variables**: Configure PostgreSQL connection details and the Tomorrow.io API key.
- **Testing**: dbt includes data quality tests in `_model.yml` for key fields.
- **Required Package**: there is a file name requirment.txt that contains all the required python packages to run the whole piplines. they will be installed during the `docker compose up --build` step so there is no need to do an extra step to install them
