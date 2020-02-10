from datetime import datetime
import time

def cron_job(): # 7.45pm UTC == 8.45am NZT
    timeout = 60
    while True:
        print(datetime.utcnow())
        if datetime.utcnow().hour == 23:
            timeout = 10
            if datetime.utcnow().minute > 2:
                # d = bamboo_bot.get_anniversary_data()
                print("it is time!!!")
                # do birthday message post
                timeout = 60
        print(f'timeout for {timeout}')
        time.sleep(timeout)

if __name__ == '__main__':
    cron_job()