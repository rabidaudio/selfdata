# Games played

```chess_win_rates
-- TODO: make transforms rather than querying raw data
select date_trunc('month', TO_TIMESTAMP(createdat / 1000)) as month,
case winner
when 'white' then case when players__white__user__id = username then 'won' else 'lost' end
when 'black' then case when players__black__user__id = username then 'won' else 'lost' end
else 'draw'
end as outcome,
count(1) as count
from tap_lichess.games
where username = 'charlesjuliank'
group by month, outcome
order by month, outcome
```

<AreaChart 
    data={chess_win_rates}  
    x=month 
    y=count
    series=outcome
/>

# Favorite openings

## As white

```favorite_openings_white
with top_openings as (
  select opening__name as opening,
  count(1) as count
  from tap_lichess.games
  where username = 'charlesjuliank' and players__white__user__id = 'charlesjuliank'
  and opening__name is not null
  group by opening
)
select * from top_openings
order by count desc
limit 10
```

<DataTable
    data={favorite_openings_white}
    rows=10
/>

## As black

```favorite_openings_black
with top_openings as (
  select opening__name as opening,
  count(1) as count
  from tap_lichess.games
  where username = 'charlesjuliank' and players__black__user__id = 'charlesjuliank'
  and opening__name is not null
  group by opening
)
select * from top_openings
order by count desc
limit 10
```

<DataTable
    data={favorite_openings_black}
    rows=10
/>
