with listening_clock as (
  select * from {{ ref('listening_clock') }}
),

first_user as (
  select distinct username from listening_clock limit 1
),

first_user_data as (
  select lc.* from listening_clock lc
    inner join first_user u on u.username = lc.username
),

all_hours as (
  select generate_series(0, 23) as hour
)

select *
from all_hours h
left join first_user_data fud on fud.hour = h.hour
where fud.absolute_plays is null
