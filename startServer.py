import psutil


for q in psutil.process_iter():
    try:
        if q.name() == 'manage.py':
            if len(q.cmdline()) > 1 and '실행하고 있는 python 파일 이름' in q.cmdline()[1]:
                print("존재")

    except psutil.AccessDenied:
        continue