with games as (
    select * from {{ ref('chess_games') }}
),

openings_with_stats as (
    select
        username,
        opening_name,
        side,
        count(1) as total_games,
        sum(case when outcome = 'won' then 1 else 0 end) as total_won_games,
        sum(case when outcome = 'lost' then 1 else 0 end) as total_lost_games,
        sum(case when outcome = 'drawn' then 1 else 0 end) as total_drawn_games
    from games
    where opening_name is not null
    group by username, opening_name, side
)

select *,
    cast((total_won_games - total_lost_games) as double) / cast(total_games as double) as score
    from openings_with_stats
