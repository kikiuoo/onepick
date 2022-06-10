import os
import subprocess

socSrvProc = subprocess.check_output("pgrep -lf manage.py | wc -l", shell=True)

if int(socSrvProc) == 0 :
    os.system("python /data/onepick/manage.py runserver 0.0.0.0:80 &")
