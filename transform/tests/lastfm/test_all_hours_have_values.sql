with listening_clock as (
  select * from {{ ref('listening_clock') }}
),

first_user as (
  select distinct username from listening_clock limit 1
),

first_user_data as (
  select listening_clock.* from listening_clock
  inner join first_user on first_user.username = listening_clock.username
),

all_hours as (
  select generate_series(0, 23) as hour_of_day
)

select 1
from all_hours
left join first_user_data on first_user_data.hour_of_day = all_hours.hour_of_day
where first_user_data.absolute_plays is null
