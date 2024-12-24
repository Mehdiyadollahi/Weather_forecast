import aiohttp
import asyncpg
import asyncio
from datetime import datetime
from .utils import calculate_md5
# from utils import calculate_md5
from . import config
# import config


async def fetch_weather(session, location):
    # Customize the payload with the location
    payload = config.payload_template.copy()
    payload["location"] = location

    async with session.post(config.URL, json=payload, headers=config.headers) as response:
        data = await response.json()
        data = data['data']['timelines'][0]
        await asyncio.sleep(1)
        response_list = []
        for interval_data in data['intervals']:
            temp_dict = {}
            temp_dict['lat'] = location.split(',')[0].strip()
            temp_dict['lon'] = location.split(',')[1].strip()
            temp_dict['api_call_timestamp'] = datetime.fromisoformat(
                data['startTime'].replace("Z", "+00:00"))
            temp_dict['timestamp'] = datetime.fromisoformat(
                interval_data['startTime'].replace("Z", "+00:00"))
            temp_dict['id'] = calculate_md5(
                temp_dict['lat'] + temp_dict['lon'] + str(temp_dict['timestamp']))
            temp_dict = {**temp_dict, **{k: v for k,
                                         v in interval_data['values'].items()}}
            response_list.append(temp_dict)

        return response_list


async def fetch_all_weather():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather(session, location)
                 for location in config.LOCATIONS]
        results = await asyncio.gather(*tasks)
        return results


async def store_weather_data_batch(weather_data):
    # Establish a connection to the database
    conn = await asyncpg.connect(
        host=config.DATABASE_HOST,
        database=config.DATABASE_NAME,
        user=config.DATABASE_USER_NAME,
        password=config.DATABASE_PASSWORD)

    # Prepare the SQL insertion query
    insert_query = """
    INSERT INTO weather_source.weather_data (
        id, api_call_timestamp, timestamp, lat, lon, temperature, apparent_temperature, wind_speed, 
        humidity, rain_intensity, snow_intensity, cloud_cover
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    """

    # Create a list of tuples to hold the data for batch insertion
    values = []
    for wd in weather_data:
        values.append((wd['id'], wd['api_call_timestamp'], wd['timestamp'], wd['lat'], wd['lon'], wd['temperature'],
                      wd['temperatureApparent'], wd['windSpeed'], wd['humidity'], wd['rainIntensity'], wd['snowIntensity'], wd['cloudCover']))

    # Execute the batch insert
    await conn.executemany(insert_query, values)

    # Close the connection
    await conn.close()
