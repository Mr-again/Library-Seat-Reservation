import requests
from lxml import etree
from urllib import parse
import datetime


def reserve(username, password, seat, start, end, date_flag):
    print('!!!!!!!!reserve my seat!!!!!!!!')
    cookie, token_login = get_cookie()
    if cookie is None or token_login is None:
        print('reserve fail bcz get_cookie')
        return None
    res1 = log_in(username, password, cookie, token_login)
    if res1 is None or res1 is False:
        print('reserve fail bcz log_in')
        return None
    token_res = get_login_page(cookie)
    if token_res is None:
        print('reserve fail bcz get_login_page')
        return None
    res_id = make_res(cookie, token_res, seat, start, end, date_flag)
    if res_id is None:
        print('reserve fail bcz make_res')
        return None
    res2 = log_out(cookie)
    if res2 is None or res2 is False:
        print('reserve success but log_out fail')
    print('reserve success')
    return res_id


def cancel(username, password, res_id):
    print('!!!!!!!!cancel my seat!!!!!!!!')
    cookie, token_login = get_cookie()
    if cookie is None or token_login is None:
        print('cancel fail bcz get_cookie')
        return None
    res1 = log_in(username, password, cookie, token_login)
    if res1 is None or res1 is False:
        print('cancel fail bcz log_in')
        return None
    res2 = cancel_res(cookie, res_id)
    if res2 is None or res2 is False:
        print('cancel fail bcz cancel_res')
        return None
    res3 = log_out(cookie)
    if res3 is None or res3 is False:
        print('cancel success bcz cancel_res')
    print('cancel success')
    return True


def get_cookie():
    print('===get cookie===')
    headers = {'Host': 'seat.lib.whu.edu.cn',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://seat.lib.whu.edu.cn/selfRes',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
    try:
        r = requests.get('https://seat.lib.whu.edu.cn/login?targetUri=%2F', verify=False, headers=headers)
    except requests.exceptions as e:
        print(e)
        return None, None
    if r.status_code != 200:
        print('http-code is not 200')
        return None, None
    cookie = r.headers.get('Set-Cookie').split(';')[0]
    print('cookie: '+cookie)
    token = etree.HTML(r.text).xpath("//input[@id='SYNCHRONIZER_TOKEN']/@value")[0]
    print('SYNCHRONIZER_TOKEN: '+token)
    return cookie, token


def log_in(username, password, cookie, token):
    print('===log in===')
    headers = {'Host': 'seat.lib.whu.edu.cn',
               'Connection': 'keep-alive',
               'Content-Length': '213',
               'Cache-Control': 'max-age=0',
               'Origin': 'https://seat.lib.whu.edu.cn',
               'Upgrade-Insecure-Requests': '1',
               'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://seat.lib.whu.edu.cn/login?targetUri=%2F',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Cookie': cookie}
    data = {'SYNCHRONIZER_TOKEN': token,
            'SYNCHRONIZER_URI': '/login',
            'username': username,
            'password': password,
            'authid': '-1',
            'appId': 'a3a5c1faff9e41c2b2447a52c5bd7ea0',
            'appAuthKey': 'a109981dd38540d5b20b4af760d7f6f1'}
    try:
        r = requests.post('https://seat.lib.whu.edu.cn/auth/signIn', data=parse.urlencode(data),
                          headers=headers, verify=False, allow_redirects=False)
    except requests.exceptions as e:
        print(e)
        return None
    if r.status_code != 302:
        print('http-code is not 302')
        return None
    if r.headers['Location'] == 'https://seat.lib.whu.edu.cn/':
        print('log_in success')
        return True
    else:
        print('log_in fail')
        return False


def get_login_page(cookie):
    print("===get login page===")
    headers = {'Host': 'seat.lib.whu.edu.cn',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://seat.lib.whu.edu.cn/login?targetUri=%2F',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Cookie': cookie}
    try:
        r = requests.get('https://seat.lib.whu.edu.cn/', headers=headers, verify=False)
    except requests.exceptions as e:
        print(e)
        return None
    if r.status_code != 200:
        print('http-code is not 200')
        return None
    token = etree.HTML(r.text).xpath("//input[@id='SYNCHRONIZER_TOKEN']/@value")[0]
    print('SYNCHRONIZER_TOKEN: ' + token)
    return token


def make_res(cookie, token, seat, start, end, date_flag):
    headers = {'Host': 'seat.lib.whu.edu.cn',
               'Connection': 'keep-alive',
               'Content-Length': '203',
               'Cache-Control': 'max-age=0',
               'Origin': 'https://seat.lib.whu.edu.cn',
               'Upgrade-Insecure-Requests': '1',
               'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://seat.lib.whu.edu.cn/login?targetUri=%2F',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Cookie': cookie}
    if date_flag is False:
        tomorrow = ''
    else:
        tomorrow_time = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow = str(tomorrow_time.date())
    data = {'SYNCHRONIZER_TOKEN': token,
            'SYNCHRONIZER_URI': '/',
            'date': tomorrow,
            'seat': str(seat),
            'start': str(start),
            'end': str(end),
            'authid': '-1',
            'appId': 'a3a5c1faff9e41c2b2447a52c5bd7ea0',
            'appAuthKey': 'a109981dd38540d5b20b4af760d7f6f1'}
    try:
        r = requests.post('https://seat.lib.whu.edu.cn/selfRes', verify=False, headers=headers, data=data)
    except requests.exceptions as e:
        print(e)
        return None
    if r.status_code != 200:
        print('http-code is not 200')
        return None
    seq_id = etree.HTML(r.text).xpath("//dd/text()")[0]
    if len(seq_id) != 10:
        print('make_res fail')
        return None
    res_id = '47'+seq_id.split('-')[2]+'-'+seq_id.split('-')[1]
    print(res_id)
    return res_id


def cancel_res(cookie, res_id):
    print('===cancel res===')
    if res_id is None:
        print('no seat to cancel')
        return
    headers = {'Host': 'seat.lib.whu.edu.cn',
               'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://seat.lib.whu.edu.cn/login?targetUri=%2F',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Cookie': cookie}
    for i in range(10):
        try:
            r = requests.get('https://seat.lib.whu.edu.cn/reservation/cancel/'+res_id.replace('-', str(i)),
                             headers=headers, verify=False, allow_redirects=False)
        except requests.exceptions as e:
            print(e)
            return None
        if r.status_code != 302:
            print('http-code is not 302')
            return None
    print('cancel_res success')
    return True


def log_out(cookie):
    print('===log out===')
    headers = {'Host': 'seat.lib.whu.edu.cn',
               'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://seat.lib.whu.edu.cn/login?targetUri=%2F',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Cookie': cookie}
    try:
        r = requests.get('https://seat.lib.whu.edu.cn/logout', headers=headers, verify=False, allow_redirects=False)
    except requests.exceptions as e:
        print(e)
        return None
    if r.status_code != 302:
        print('http-code is not 302')
        return None
    print("log_out success")
    return True
