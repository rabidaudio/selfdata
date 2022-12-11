# flake8: noqa E101
from my_meltano_project.assets.meltano import _parse_unique_streams

TEST_DATA = b"""
2022-12-10T21:28:00.363104Z [info     ] The default environment 'sandbox' will be ignored for `meltano select`. To configure a specific environment, please use the option `--environment=<environment name>`.
Legend:
	selected
	excluded
	automatic

Enabled patterns:
	*.*

Selected attributes:
	[selected ] games.analysis
	[selected ] games.clock
	[selected ] games.clock.increment
	[selected ] games.clock.initial
	[selected ] games.clock.totalTime
	[selected ] games.createdAt
	[selected ] games.daysPerTurn
	[automatic] games.id
	[selected ] games.initialFen
	[selected ] games.lastMoveAt
	[selected ] games.moves
	[selected ] games.opening
	[selected ] games.opening.eco
	[selected ] games.opening.name
	[selected ] games.opening.ply
	[selected ] games.perf
	[selected ] games.pgn
	[selected ] games.players
	[selected ] games.players.black
	[selected ] games.players.black.aiLevel
	[selected ] games.players.black.analysis
	[selected ] games.players.black.analysis.acpl
	[selected ] games.players.black.analysis.blunder
	[selected ] games.players.black.analysis.inaccuracy
	[selected ] games.players.black.analysis.mistake
	[selected ] games.players.black.name
	[selected ] games.players.black.provisional
	[selected ] games.players.black.rating
	[selected ] games.players.black.ratingDiff
	[selected ] games.players.black.team
	[selected ] games.players.black.user
	[selected ] games.players.black.user.id
	[selected ] games.players.black.user.name
	[selected ] games.players.black.user.patron
	[selected ] games.players.black.user.title
	[selected ] games.players.white
	[selected ] games.players.white.aiLevel
	[selected ] games.players.white.analysis
	[selected ] games.players.white.analysis.acpl
	[selected ] games.players.white.analysis.blunder
	[selected ] games.players.white.analysis.inaccuracy
	[selected ] games.players.white.analysis.mistake
	[selected ] games.players.white.name
	[selected ] games.players.white.provisional
	[selected ] games.players.white.rating
	[selected ] games.players.white.ratingDiff
	[selected ] games.players.white.team
	[selected ] games.players.white.user
	[selected ] games.players.white.user.id
	[selected ] games.players.white.user.name
	[selected ] games.players.white.user.patron
	[selected ] games.players.white.user.title
	[selected ] games.rated
	[selected ] games.speed
	[selected ] games.status
	[selected ] games.swiss
	[selected ] games.tournament
	[selected ] games.username
	[selected ] games.variant
	[selected ] games.winner
	[selected ] users.createdAt
	[selected ] users.disabled
	[automatic] users.id
	[selected ] users.online
	[selected ] users.patron
	[selected ] users.perfs
	[selected ] users.perfs.atomic
	[selected ] users.perfs.atomic.games
	[selected ] users.perfs.atomic.prog
	[selected ] users.perfs.atomic.prov
	[selected ] users.perfs.atomic.rating
	[selected ] users.perfs.atomic.rd
	[selected ] users.perfs.blitz
	[selected ] users.perfs.blitz.games
	[selected ] users.perfs.blitz.prog
	[selected ] users.perfs.blitz.prov
	[selected ] users.perfs.blitz.rating
	[selected ] users.perfs.blitz.rd
	[selected ] users.perfs.bullet
	[selected ] users.perfs.bullet.games
	[selected ] users.perfs.bullet.prog
	[selected ] users.perfs.bullet.prov
	[selected ] users.perfs.bullet.rating
	[selected ] users.perfs.bullet.rd
	[selected ] users.perfs.chess960
	[selected ] users.perfs.chess960.games
	[selected ] users.perfs.chess960.prog
	[selected ] users.perfs.chess960.prov
	[selected ] users.perfs.chess960.rating
	[selected ] users.perfs.chess960.rd
	[selected ] users.perfs.classical
	[selected ] users.perfs.classical.games
	[selected ] users.perfs.classical.prog
	[selected ] users.perfs.classical.prov
	[selected ] users.perfs.classical.rating
	[selected ] users.perfs.classical.rd
	[selected ] users.perfs.correspondence
	[selected ] users.perfs.correspondence.games
	[selected ] users.perfs.correspondence.prog
	[selected ] users.perfs.correspondence.prov
	[selected ] users.perfs.correspondence.rating
	[selected ] users.perfs.correspondence.rd
	[selected ] users.perfs.horde
	[selected ] users.perfs.horde.games
	[selected ] users.perfs.horde.prog
	[selected ] users.perfs.horde.prov
	[selected ] users.perfs.horde.rating
	[selected ] users.perfs.horde.rd
	[selected ] users.perfs.kingOfTheHill
	[selected ] users.perfs.kingOfTheHill.games
	[selected ] users.perfs.kingOfTheHill.prog
	[selected ] users.perfs.kingOfTheHill.prov
	[selected ] users.perfs.kingOfTheHill.rating
	[selected ] users.perfs.kingOfTheHill.rd
	[selected ] users.perfs.puzzle
	[selected ] users.perfs.puzzle.games
	[selected ] users.perfs.puzzle.prog
	[selected ] users.perfs.puzzle.prov
	[selected ] users.perfs.puzzle.rating
	[selected ] users.perfs.puzzle.rd
	[selected ] users.perfs.racingKings
	[selected ] users.perfs.racingKings.games
	[selected ] users.perfs.racingKings.prog
	[selected ] users.perfs.racingKings.prov
	[selected ] users.perfs.racingKings.rating
	[selected ] users.perfs.racingKings.rd
	[selected ] users.perfs.rapid
	[selected ] users.perfs.rapid.games
	[selected ] users.perfs.rapid.prog
	[selected ] users.perfs.rapid.prov
	[selected ] users.perfs.rapid.rating
	[selected ] users.perfs.rapid.rd
	[selected ] users.perfs.storm
	[selected ] users.perfs.storm.runs
	[selected ] users.perfs.storm.score
	[selected ] users.perfs.ultraBullet
	[selected ] users.perfs.ultraBullet.games
	[selected ] users.perfs.ultraBullet.prog
	[selected ] users.perfs.ultraBullet.prov
	[selected ] users.perfs.ultraBullet.rating
	[selected ] users.perfs.ultraBullet.rd
	[selected ] users.playTime
	[selected ] users.playTime.total
	[selected ] users.playTime.tv
	[selected ] users.profile
	[selected ] users.profile.bio
	[selected ] users.profile.country
	[selected ] users.profile.ecfRating
	[selected ] users.profile.fideRating
	[selected ] users.profile.firstName
	[selected ] users.profile.lastName
	[selected ] users.profile.links
	[selected ] users.profile.location
	[selected ] users.profile.uscfRating
	[selected ] users.seenAt
	[selected ] users.title
	[selected ] users.tosViolation
	[selected ] users.username
	[selected ] users.verified
"""  # noqa


def test_parse_unique_streams():
    assert _parse_unique_streams(TEST_DATA) == {"games", "users"}
