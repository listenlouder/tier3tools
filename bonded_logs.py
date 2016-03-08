from sys import argv
import datetime
from os.path import expanduser

_, file  = argv
home = expanduser('~')

with open('%s/Downloads/%s' % (home, file)) as f:
    log_lines = f.read().splitlines()

for line in log_lines:
    if 'mobileTransportEnabled=true' in line:
        time = datetime.datetime.fromtimestamp(int(line.split(' ')[0])/1000)
        print time