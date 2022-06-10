import psutil
import os


for q in psutil.process_iter():
    try:
        print(q.name())
        if q.name() == 'python3.8':
            if len(q.cmdline()) > 1 and 'manage.py' in q.cmdline()[1]:
                os.system("python /data/onepick/manage.py runserver 0.0.0.0:80 &")
                
            else :
                print("없음")

        else :
            print("없음2")

    except psutil.AccessDenied:
        continue