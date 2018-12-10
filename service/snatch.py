import datetime
from seatRes import webRequests
import multiprocessing
import configparser
import warnings


warnings.filterwarnings('ignore')
conf_ini = configparser.ConfigParser()
conf_ini.read('../conf.ini')
hour = conf_ini.getint("snatch", "pre_res_hour")
minute = conf_ini.getint("snatch", "pre_res_minute")
second = conf_ini.getint("snatch", "pre_res_second")
microsecond = conf_ini.getint("snatch", "pre_res_microsecond")
users_ini = configparser.ConfigParser()
users_ini.read('../users.ini')


def check_time():
    cur_time = datetime.datetime.now()
    des_time = cur_time.replace(hour=hour, minute=minute, second=second, microsecond=microsecond)
    delta = des_time-cur_time
    skip_seconds = int(delta.total_seconds())
    if skip_seconds == 0:
        return True
    else:
        return False


def snatch_seat(lock, username, password, seat):
    while True:
        if check_time():
            for i in range(3):
                res_id = webRequests.reserve(username, password, seat, 1320, 1350, False)
                if res_id is not None:
                    print('预约成功!res_id为:'+res_id+',time = '+str(datetime.datetime.now()))
                    if res_id is not None:
                        lock.acquire()
                        users_ini.set('2015301500270', 'res_id', str(res_id))
                        users_ini.set('2015301500270', 'seat_id', str(seat))
                        users_ini.set('2015301500270', 'start', str(1290))
                        users_ini.set('2015301500270', 'end', str(1350))
                        users_ini.write(open('../users.ini', 'w'))
                        lock.release()
                        print('预约序列存储成功!')
                    return True
            print('预约失败！,time = '+str(datetime.datetime.now()))
            return False


def multi_snatch(username, password, seat):
    lock = multiprocessing.Lock()
    for i in range(10):
        p = multiprocessing.Process(target=snatch_seat, args=(lock, username, password, seat))
        p.daemon = False
        p.start()


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    result = manager.dict()
    multi_snatch('xxx', 'xxx', 12333)
