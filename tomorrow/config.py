import os

# Define the API URL and location data
URL = "https://api.tomorrow.io/v4/timelines?apikey=rw4xHJ47416anwbpRFzFY6cbHsINb9P1"
LOCATIONS = [
    '25.8600, -97.4200',
    '25.9000, -97.5200',
    '25.9000, -97.4800',
    '25.9000, -97.4400',
    '25.9000, -97.4000',
    '25.9200, -97.3800',
    '25.9400, -97.5400',
    '25.9400, -97.5200',
    '25.9400, -97.4800',
    '25.9400, -97.4400'
]
DATABASE_USER_NAME = os.environ.get('PGUSER')
DATABASE_PASSWORD = os.environ.get('PGPASSWORD')
DATABASE_PORT = os.environ.get('PGPORT')
DATABASE_NAME = os.environ.get('PGDATABASE')
DATABASE_HOST = 'postgres'

# Payload data for the API requests
payload_template = {
    "fields": ["temperature", "temperatureApparent", "windSpeed", "humidity", "rainIntensity", "snowIntensity", "cloudCover"],
    "units": "metric",
    "timesteps": ["1h"],
    "startTime": "now",
    "endTime": "nowPlus5d"
}

headers = {
    "accept": "application/json",
    "Accept-Encoding": "gzip",
    "content-type": "application/json"
}

# Path to the dbt project directory
DBT_PROJECT_DIR = "tomorrow/report_models/tomorrow_weather"