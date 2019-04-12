#! /usr/bin/env python3

import rospy, os, sys, time, serial, threading
from std_msgs.msg import String

from pymeasure import *
class tpg261_driver(object):
    def __init__(self):

        self.pub_p = rospy.Publisher("/tpg_pressure", String, queue_size=1)

        self.tpg261 = serial.Serial("/dev/ttyUSB1",timeout=1)

        self.query_pres = pressure()

        self.query_bothpres = pressure()

        self.query_gauge = gauge()

        self.channel_dis = display()

        self.error_moni = error()

    def query_pressure(self):
        while not rospy.is_shutdown():
            self.query_pres.pressure_device()
            if raw == b'\x06\r\n':
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
                      pass

    def query_bothpressure(self):
        while not rospy.is_shutdown():
            self.query_bothpres.pressure_both()
            if raw == b'\x06\r\n':
                continue
            else:
                 if status1 == b'2' or status2 == b'2':
                      msg = String()
                      msg.data = Overrange
                      self.pub_p.publish(msg)
                 elif status1 == b'0' or status2 == b'0':
                      msg = String()
                      msg.data = pressure
                      self.pub_p.publish(msg)
                 else:
                      pass



    def check_gauge(self):
        self.query_gauge.gauge_check()

             if status1 == b'0':
                      msg = String()
                      msg.data = cannot be changed
                      self.pub_p.publish(msg)
                 elif status1 == b'1':
                      msg = String()
                      msg.data = turned off
                      self.pub_p.publish(msg)
                 elif status1 == b'2':
                            msg = String()
                            msg.data = turned on
                            self.pub_p.publish(msg)
                 else:
                      pass

                   if status2 == b'0':
                        msg = String()
                        msg.data = cannot be changed
                        self.pub_p.publish(msg)
                   elif status2 == b'1':
                        msg = String()
                        msg.data = turned off
                        self.pub_p.publish(msg)
                   elif status2 == b'2':
                              msg = String()
                              msg.data = turned on
                              self.pub_p.publish(msg)
                   else:
                        pass


    def turn_gauge(self):
            self.query_gauge.gauge_change(gague1,gague2)

                 if status1 == b'0':
                      msg = String()
                      msg.data = cannot be changed
                      self.pub_p.publish(msg)
                 elif status1 == b'1':
                      msg = String()
                      msg.data = turned off
                      self.pub_p.publish(msg)
                 elif status1 == b'2':
                      msg = String()
                      msg.data = turned on
                      self.pub_p.publish(msg)
                 else:
                      pass

                   if status2 == b'0':
                        msg = String()
                        msg.data = cannot be changed
                        self.pub_p.publish(msg)
                   elif status2 == b'1':
                        msg = String()
                        msg.data = turned off
                        self.pub_p.publish(msg)
                   elif status2 == b'2':
                        msg = String()
                        msg.data = turned on
                        self.pub_p.publish(msg)
                   else:
                        pass

    def display_gauge1(self):
        self.channel_dis.change_gague1()
        msg = String()
        msg.data = gague1
        self.pub_p.publish(msg)

    def display_gauge2(self):
        self.channel_dis.change_gague2()
        msg = String()
        msg.data = gague2
        self.pub_p.publish(msg)

    def error_status(self):
        self.error_moni.query_error()
                   if status == b'0000':
                        msg = String()
                        msg.data = No error
                        self.pub_p.publish(msg)
                   elif status == b'1000':
                        msg = String()
                        msg.data = Controller Error see display
                        self.pub_p.publish(msg)
                   elif status == b'0100':
                        msg = String()
                        msg.data = No hardware
                        self.pub_p.publish(msg)
                   elif status == b'0010':
                        msg = String()
                        msg.data = Inadmissible parameter
                        self.pub_p.publish(msg)
                   elif status == b'0001':
                        msg = String()
                        msg.data = Syntax Error
                        self.pub_p.publish(msg)
                   else:
                        pass


if __name__ == "__main__" :
    rospy.init_node("tpg261")
    tpg = tpg261_driver()
    thread_tpg = threading.Thread(target=tpg.query_pressure)
    thread_tpg.start()
    tpg.query_pressure()


#2019
#written by T.Takashima
