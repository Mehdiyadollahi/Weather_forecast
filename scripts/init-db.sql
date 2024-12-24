CREATE SCHEMA IF NOT EXISTS weather_source ;

CREATE TABLE IF NOT EXISTS weather_source.weather_data (
    id varchar(200) NOT NULL,
    api_call_timestamp TIMESTAMPTZ NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    lat varchar(20) NOT NULL,
    lon varchar(20) NOT NULL,
    temperature NUMERIC(5,2),
    apparent_temperature NUMERIC(5,2),
    wind_speed NUMERIC(5,2),
    humidity NUMERIC(5,2),
    rain_intensity NUMERIC(5,2),
    snow_intensity NUMERIC(5,2),
    cloud_cover NUMERIC(5,2)
);
