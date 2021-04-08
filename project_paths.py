from os.path import join, normpath, dirname

repo_path = normpath(dirname(__file__))
config_path = normpath(join(repo_path, 'config.ini'))
