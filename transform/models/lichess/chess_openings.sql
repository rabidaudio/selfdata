with games as (
    select * from {{ ref('chess_games') }}
)

select
    username,
    opening_name,
    side,
    count(1) as total_games,
    sum(case when outcome = 'won' then 1 else 0 end) as total_won_games,
    sum(case when outcome = 'lost' then 1 else 0 end) as total_lost_games,
    sum(case when outcome = 'drawn' then 1 else 0 end) as total_drawn_games
from games
group by username, opening_name, side
