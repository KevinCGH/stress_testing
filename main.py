# -*- coding: utf-8 -*-
import http
import http.client
import threading
import time

HOST = "www.baidu.com"
URI = '/'
PORT = 80
TOTAL = 0  # 总数
SUCC = 0  # 响应成功数
FAIL = 0  # 响应失败数
TOTALTIME = 0  # 总响应时间


class RequestThread(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.test_count = 0

    def run(self):
        self.test_performace()

    def test_performace(self):
        global TOTAL
        global SUCC
        global TOTALTIME
        global FAIL
        try:
            st = time.time()
            conn = http.client.HTTPConnection(HOST, PORT, False)
            conn.request('GET', URI)
            res = conn.getresponse()
            time_span = time.time() - st
            if res.status == http.HTTPStatus.OK:
                TOTAL += 1
                SUCC += 1
                TOTALTIME += time_span
            else:
                TOTAL += 1
                FAIL += 1
        except Exception as e:
            print(e)
            TOTAL += 1
            FAIL += 1
        conn.close()


def test(thread_count):
    global TOTAL
    global SUCC
    global FAIL
    global TOTALTIME

    i = 0
    TOTAL = 0
    SUCC = 0
    FAIL = 0
    TOTALTIME = 0
    print("============tesk start============")
    start_time = time.time()
    while i < thread_count:
        t = RequestThread("thread-" + str(i))
        t.start()
        i += 1

    print("============tesk end============")
    print(f"thread count: {thread_count}")
    print(f"total: {TOTAL}, success: {SUCC},  fail: {FAIL}")
    print(f"average time: {TOTALTIME / SUCC}")


def single_test():
    conn = http.client.HTTPConnection(HOST, PORT)
    conn.request('GET', '/')
    res = conn.getresponse()
    if res.status == http.HTTPStatus.OK:
        print("request ok")
    else:
        print("request fail! status: {}" % res.status)


if __name__ == "__main__":
    single_test()
    test(10)
