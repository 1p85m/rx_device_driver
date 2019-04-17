#! /usr/bin/env python3

import rospy, os, sys, time, serial, threading
from std_msgs.msg import String

from pymeasure_tpg261 import tpg261

class tpg261_driver(object):
    def __init__(self):

        self.pub_p = rospy.Publisher("/tpg_pressure", String, queue_size=1)

        self.dev = tpg261.device()

    def query_pressure(self):
        while not rospy.is_shutdown():
            self.dev.pressure_device()
            self.b = self.dev.check()
            status = self.dev.pressure_device()
            print("akann1")
            if self.b == 0:
                continue
            else:
                 if status == b'2':
                      msg = String()
                      msg.data = Overrange
                      self.pub_p.publish(msg)
                 elif status == b'0':
                      msg = String()
                      msg.data = pressure
                      self.pub_p.publish(msg)
                 else:
                     print("akann2")
                      pass

if __name__ == "__main__" :
    rospy.init_node("tpg261")
    tpg = tpg261_driver()
    thread_tpg = threading.Thread(target=tpg.query_pressure)
    thread_tpg.start()


#2019
#written by T.Takashima
