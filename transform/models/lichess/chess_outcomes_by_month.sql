with games as (
    select * from {{ ref('chess_games') }}
),

game_outcomes as (
    select
        username,
        date_trunc('month', created_at) as month,
        outcome
    from games
),

stats as (
    select
        username,
        month,
        count(1) as total_games,
        sum(case when outcome = 'won' then 1 else 0 end) as total_won_games,
        sum(case when outcome = 'lost' then 1 else 0 end) as total_lost_games,
        sum(case when outcome = 'drawn' then 1 else 0 end) as total_drawn_games
    from game_outcomes
    group by username, month
)

select *,
    cast((total_won_games - total_lost_games) as double) / cast(total_games as double) as score
from stats
