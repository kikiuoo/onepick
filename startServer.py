import psutil


for q in psutil.process_iter():
    try:
        if q.name() == 'python':
            if len(q.cmdline()) > 1 and 'manage.py' in q.cmdline()[1]:
                print("존재")
                
            else :
                print("없음")
        else :
            print("없음2")


    except psutil.AccessDenied:
        continue