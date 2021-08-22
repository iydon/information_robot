__all__ = ('host', 'auth_key', 'account', 'database_path', 'information_groups')


import pathlib
import yaml


paths = (
    pathlib.Path('bots'),
    pathlib.Path('config', 'net.mamoe.mirai-api-http', 'setting.yml'),
)
assert all(path.exists() for path in paths)
account = next(paths[0].iterdir()).name
setting = yaml.full_load(paths[1].read_text())
host = f'http://{setting["host"]}:{setting["port"]}'
auth_key = setting['authKey']
database_path = pathlib.Path('db.json')  # .absolute()
information_groups = ()
