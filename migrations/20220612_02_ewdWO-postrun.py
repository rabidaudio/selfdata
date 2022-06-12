from yoyo import step

__depends__ = {'20220612_01_3qiZB'}

def add_index(table, *columns):
    return f"CREATE INDEX idx_{table.replace('.', '_')}_on_{'_'.join(columns)} ON {table} ({', '.join(columns)})"

steps = [
    step(add_index('tap_lastfm.users', 'username')),
    step(add_index('tap_lastfm.scrobbles', 'username')),
    step(add_index('tap_lastfm.scrobbles', 'date')),
]
