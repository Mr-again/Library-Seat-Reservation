from datetime import datetime
from seatRes import webRequests


def check_time():
    cur_time = datetime.now()
    des_time = cur_time.replace(hour=11, minute=28, second=0, microsecond=0)
    delta = des_time-cur_time
    skip_seconds = int(delta.total_seconds())
    if skip_seconds == 0:
        return True
    else:
        return False


def snatch_seat(username, password, seat):
    while True:
        if check_time():
            for i in range(3):
                res_id = webRequests.reserve(username, password, seat, 1260, 1350)
                if res_id is not None:
                    print('预约成功!res_id为:'+res_id+',time = '+str(datetime.now()))
                    return res_id
            print('预约失败！,time = '+str(datetime.now()))
            return None
