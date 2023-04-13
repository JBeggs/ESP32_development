import sched
from datetime import datetime, date
import time
from time import monotonic
import _thread


class Schedular(object):

    def __init__(self, start_date, start_time, end_date, end_time):

        self._start_date = start_date
        self._start_time = start_time
        self._end_date   = end_date
        self._end_time   = end_time

    def start(self):

        while True:

            current_time = time.localtime()

            time.sleep(5)

        # # 09/19/22 13:55
        # # valid  = date.fromisoformat('2003-12-23')
        # s = sched.scheduler()
        #
        # start_date_time = '{} {}'.format(self._start_date, self._start_time)
        # start_time_object = datetime.strptime(start_date_time, '%m/%d/%y %H:%M')
        # start_event = s.enterabs(float(start_time_object), 1, addition, kwargs = {"a": 10, "b": 20})
        #
        # s.run()
        # s = sched.scheduler()
        # end_date_time   = '{} {}'.format(self._end_date, self._end_time)
        # end_time_object   = datetime.strptime(end_date_time, '%m/%d/%y %H:%M')
        # send_event  = s.enterabs(end_time_object, 1, addition, kwargs = {"a": 10, "b": 20})
        # s.run()


def addition(a, b):
    print("\nInside Addition : ", datetime.now())
    print("Time : ", time.monotonic())
    print("Result : ", a+b)

