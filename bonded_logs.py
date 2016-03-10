from sys import argv
import datetime
from os.path import expanduser

_, file  = argv

with open('%s/Downloads/%s' % (expanduser('~'), file)) as f:
    log_lines = f.read().splitlines()

for line in log_lines:
    if 'mobileTransportEnabled=true' in line:
        print datetime.datetime.fromtimestamp(int(line.split(' ')[0])/1000)