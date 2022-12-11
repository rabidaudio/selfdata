with _src_games as (
    select * from {{ source('tap_lichess', 'games') }}
),

_distinct_games as (
    {{ distinct_on('_src_games', ['id']) }}
),

games as (
    select
        id,
        rated as is_rated,
        variant,
        speed,
        from_unixtime(createdat / 1000) as created_at,
        from_unixtime(lastmoveat / 1000) as last_move_at,
        status,
        coalesce(players.white.user.id, concat('stockfish', cast(players.white.ailevel as varchar))) as player_white,
        coalesce(players.black.user.id, concat('stockfish', cast(players.black.ailevel as varchar))) as player_black,
        winner,
        opening.name as opening_name,
        opening.eco as opening_code,
        moves,
        pgn,
        username
    from _distinct_games
),

games_with_winner as (
    select *,
        player_white = username as is_white,
        case when player_white = username then 'white' else 'back' end as side,
        case winner
        when 'white' then case when player_white = username then 'won' else 'lost' end
        when 'black' then case when player_black = username then 'won' else 'lost' end
        else 'drawn'
        end as outcome
    from games
)

select * from games_with_winner
