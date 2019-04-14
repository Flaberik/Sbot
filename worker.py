import threading
import time

from datetime import datetime
from pytz import timezone

import MBot
import dbController

class Worker(threading.Thread):
    def __init__(self):
        super(Worker,self).__init__()

    status = True
    pause_ = False
    global times_
    times_ = []

    def update_times(self):
        global times_
        times_ = dbController.get_times_()

    def run(self):
        global delay_second
        delay_second = 1
        delay_pause = 1

        while self.status:
            if(self.pause_ == False):
                delay_second = 1
                #print('xyi')
                for t in times_:
                    #if(str(t) == str(self.get_time())):
                    MBot.send_message_for_all_group()
                    delay_second = 60
                    break

            time.sleep(10)

    def stop(self):
        self.status = False
    def stoped(self):
        return self.status

    def pause(self):
        if(self.pause_ == False):
            self.pause_ = True
        else:
            self.pause_ = False

    def paused(self):
        return self.pause_

    def get_time(self):
        return datetime.now(timezone('Europe/Moscow')).strftime('%H:%M')
