import datetime
from seatRes import webRequests
import multiprocessing
import configparser
import warnings


lock_io = multiprocessing.Lock()
warnings.filterwarnings('ignore')
conf_ini = configparser.ConfigParser()
conf_ini.read('../conf.ini')
hour = conf_ini.getint("snatch", "pre_res_hour")
minute = conf_ini.getint("snatch", "pre_res_minute")
second = conf_ini.getint("snatch", "pre_res_second")
microsecond = conf_ini.getint("snatch", "pre_res_microsecond")
snatch_start = conf_ini.getint("snatch", "snatch_start")
snatch_end = conf_ini.getint("snatch", "snatch_end")

users_conf_ini = configparser.ConfigParser()
users_conf_ini.read('../users_conf.ini')
users_list = users_conf_ini.sections()
users_conf_list = {}
for userID in users_list:
    users_conf_list[userID] = {'password': users_conf_ini.get(userID, 'password'),
                               'seat_id': users_conf_ini.getint(userID, 'seat_id')}

users_status_ini = configparser.ConfigParser()
users_status_ini.read('../users_status.ini')


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
                res_id = webRequests.reserve(username, password, seat, snatch_start, snatch_end, False)
                if res_id is not None:
                    print('预约成功!res_id为:'+res_id+',time = '+str(datetime.datetime.now()))
                    if res_id is not None:
                        lock.acquire()
                        users_status_ini.set(username, 'res_id', str(res_id))
                        users_status_ini.set(username, 'start', str(snatch_start))
                        users_status_ini.set(username, 'end', str(snatch_end))
                        users_status_ini.write(open('../users_status.ini', 'w'))
                        lock.release()
                        print('预约序列存储成功!')
                    return True
            print('预约失败！,time = '+str(datetime.datetime.now()))
            return False


def multi_snatch(lock, username, password, seat):
    for i in range(10):
        p = multiprocessing.Process(target=snatch_seat, args=(lock, username, password, seat))
        p.daemon = False
        p.start()


if __name__ == '__main__':
    print(users_conf_list)
    for key in users_conf_list:
        multi_snatch(lock_io, key, users_conf_list[key]['password'], users_conf_list[key]['seat_id'])

