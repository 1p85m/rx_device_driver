#! /usr/bin/env python3

import rospy, os, sys, time, serial, threading
from std_msgs.msg import String
from std_msgs.msg import Float64

from pymeasure_tpg261 import tpg261

class tpg261_driver(object):
    def __init__(self):

        self.pub_er = rospy.Publisher("/tpg_error", String, queue_size=1)
        self.pub_p = rospy.Publisher("/tpg_pressure", Float64, queue_size=1)

        self.dev = tpg261.device()

    def query_pressure(self):
        while not rospy.is_shutdown():
            self.dev.pressure()
            self.dev.pressure_error()
            self.b = self.dev.check()
            status = self.dev.pressure_error()
            if self.b == 0:
                pressure = self.dev.pressure()
                print(pressure)
                pressure1 = pressure.strip("b'")
                print(pressure1)
                pres = float(pressure1)
                self.pub_p.publish(pres)
                continue
            else:
                 if status == b'2':
                      msg = String()
                      msg.data = Overrange
                      self.pub_er.publish(msg)
                 elif status == b'0':
                      msg = String()
                      msg.data = pressure
                      self.pub_er.publish(msg)
                 else:
                     error = self.dev.pressure_error()
                     self.pub_er.publish(error)
                     pass

if __name__ == "__main__" :
    rospy.init_node("tpg261")
    tpg = tpg261_driver()
    thread_tpg = threading.Thread(target=tpg.query_pressure)
    thread_tpg.start()


#2019
#written by T.Takashima
