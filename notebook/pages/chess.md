# Games played

```chess_win_rates
select month, total_won_games,  total_lost_games, total_drawn_games, round(score, 2) as score
from chess_outcomes_by_month
where username = 'charlesjuliank'
order by month
```

<AreaChart 
    data={chess_win_rates}  
    x=month
    y={["total_won_games", "total_lost_games", "total_drawn_games"]}
/>
<!-- TODO: plot draws centered vertically, won above and lost below -->
<!-- https://docs.evidence.dev/features/charts/custom-charts -->

<LineChart 
    data={chess_win_rates}  
    x=month
    y=score
/>

# Favorite openings

## As white

```favorite_openings_white
select opening_name, total_games, round(score, 2) as score
from chess_openings
where username = 'charlesjuliank' and side = 'white'
order by total_games desc
limit 10
```

<DataTable
    data={favorite_openings_white}
    rows=10
/>

## As black

```favorite_openings_black
select opening_name, total_games, round(score, 2)
from chess_openings
where username = 'charlesjuliank' and side = 'black'
order by total_games desc
limit 10
```

<DataTable
    data={favorite_openings_black}
    rows=10
/>
