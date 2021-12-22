import sys
sys.path.insert(0, '/var/www/greenhouse/')

activate_this = '/var/www/greenhouse/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from run import app as application
