import os
import time

while True:
    os.system('python manage.py dbbackup')
    time.sleep(1)