{{
    config(
        materialized="incremental",
        unique_key="id",
        merge_update_columns=[
            "temperature",
            "feels_like",
            "wind_speed",
            "humidity",
            "rain_intensity",
            "snow_intensity",
            "cloud_cover",
            "edw_updated_at"
        ],
    )
}}
with
    base as (
        select
            id,
            api_call_timestamp,
            timestamp,
            lat,
            lon,
            temperature,
            apparent_temperature as feels_like,
            wind_speed,
            humidity,
            rain_intensity,
            snow_intensity,
            cloud_cover,
            row_number() over (partition by id order by api_call_timestamp desc) as rn
        from {{ source("weather_api_source", "weather_data") }}
        {% if is_incremental() %}
            where
                api_call_timestamp >= coalesce(
                    (select max(api_call_timestamp) from {{ this }}), '1900-01-01'
                )
        {% endif %}
    )
select 
    id,
    api_call_timestamp,
    timestamp,
    lat,
    lon,
    temperature,
    feels_like,
    wind_speed,
    humidity,
    rain_intensity,
    snow_intensity,
    cloud_cover,
    current_timestamp as edw_created_at,
    current_timestamp as edw_updated_at
from base
where rn = 1
