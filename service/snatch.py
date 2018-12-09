from datetime import datetime
from seatRes import webRequests
import multiprocessing
import warnings


result = None


def check_time():
    cur_time = datetime.now()
    des_time = cur_time.replace(hour=14, minute=50, second=0, microsecond=0)
    delta = des_time-cur_time
    skip_seconds = int(delta.total_seconds())
    if skip_seconds == 0:
        return True
    else:
        return False


def snatch_seat(lock, username, password, seat):
    global result
    while True:
        if check_time():
            for i in range(3):
                res_id = webRequests.reserve(username, password, seat, 1260, 1350)
                if res_id is not None:
                    print('预约成功!res_id为:'+res_id+',time = '+str(datetime.now()))
                    if res_id is not None:
                        lock.acquire()
                        result = res_id
                        lock.release()
                        print('预约序列存储成功!')
                    return True
            print('预约失败！,time = '+str(datetime.now()))
            return False


def multi_snatch(username, password, seat):
    lock = multiprocessing.Lock()
    for i in range(10):
        p = multiprocessing.Process(target=snatch_seat, args=(lock, username, password, seat))
        p.daemon = False
        p.start()


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    multi_snatch('xxx', 'xxx', 2659)
