import json
import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _get_config_path(filename):
    config_paths = [
        os.path.join(BASE_DIR, 'configs'),
        os.path.join(os.path.expanduser('~'), 'configs'),
    ]
    for config_path in config_paths:
        p = os.path.join(config_path, filename)
        if os.path.exists(p):
            return p
    return None


def load_env_params():
    env = os.environ.get('ENV')
    if env is None:
        return

    config_path = _get_config_path('env_{0:s}.json'.format(env))

    if config_path is None:
        print('ERROR: {0:s} environment config file not found'.format(env), file=sys.stderr)
        return

    with open(config_path) as f:
        env_config = json.load(f)
    for key, value in env_config.items():
        os.environ.setdefault(key, value)
