# _author: Coke
# _date: 2022/12/10 23:21

import time


class Lock:
    """ 线程锁 """

    def __init__(self, timeout=3):
        self.timeout = timeout
        self.lock = False

    def acquire(self):
        """ 加锁 """

        start_time = time.monotonic()
        while start_time + self.timeout > time.monotonic():
            if not self.lock:
                break
            time.sleep(0.1)

        else:
            return

        self.lock = True
        return True

    def release(self):
        """ 释放锁 """

        self.lock = False
