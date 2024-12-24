{{ config(materialized="table") }}

select *
from {{ ref("weather_data_base") }} as b
where
    b.timestamp >= to_char(current_timestamp, 'YYYY-MM-DD HH24:00:00 TZH:TZM')::timestamp
    and b.timestamp
    <= to_char(current_timestamp + interval '5 day', 'YYYY-MM-DD HH24:00:00 TZH:TZM')::timestamp

