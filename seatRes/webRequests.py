import requests
from lxml import etree
from urllib import parse


def reserve(username, password, seat, start, end):
    print('!!!!!!!!reserve my seat!!!!!!!!')
    cookie, token_login = get_cookie()
    log_in(username, password, cookie, token_login)
    token_res = get_login_page(cookie)
    res_id = make_res(cookie, token_res, seat, start, end)
    return res_id


def cancel(username, password, seat_id):
    print('!!!!!!!!cancel my seat!!!!!!!!')
    cookie, token_login = get_cookie()
    log_in(username, password, cookie, token_login)
    cancel_res(cookie, seat_id)


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
    r = requests.get('https://seat.lib.whu.edu.cn/login?targetUri=%2F', verify=False, headers=headers)
    print('code: ', r.status_code)
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
    r = requests.post('https://seat.lib.whu.edu.cn/auth/signIn', data=parse.urlencode(data),
                      headers=headers, verify=False, allow_redirects=False)
    print('code: ', r.status_code)
    if r.headers['Location'] == 'https://seat.lib.whu.edu.cn/':
        print('Login success')
        return True
    else:
        print('Login fail')
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
    r = requests.get('https://seat.lib.whu.edu.cn/', headers=headers, verify=False)
    token = etree.HTML(r.text).xpath("//input[@id='SYNCHRONIZER_TOKEN']/@value")[0]
    print('SYNCHRONIZER_TOKEN: ' + token)
    return token


def make_res(cookie, token, seat, start, end):
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
    data = {'SYNCHRONIZER_TOKEN': token,
            'SYNCHRONIZER_URI': '/',
            'date': '',
            'seat': str(seat),
            'start': str(start),
            'end': str(end),
            'authid': '-1',
            'appId': 'a3a5c1faff9e41c2b2447a52c5bd7ea0',
            'appAuthKey': 'a109981dd38540d5b20b4af760d7f6f1'}
    r = requests.post('https://seat.lib.whu.edu.cn/selfRes', verify=False, headers=headers, data=data)
    print('code: ', r.status_code)
    seq_id = etree.HTML(r.text).xpath("//dd/text()")[0]
    if len(seq_id) != 10:
        print('res fail')
        return None
    res_id = '47'+seq_id.split('-')[2]+'3'+seq_id.split('-')[1]
    print(res_id)
    return res_id


def cancel_res(cookie, seat_id):
    print('===cancel res===')
    if seat_id is None:
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
    r = requests.get('https://seat.lib.whu.edu.cn/reservation/cancel/'+seat_id, headers=headers, verify=False, allow_redirects=False)
    print('code: ', r.status_code)
