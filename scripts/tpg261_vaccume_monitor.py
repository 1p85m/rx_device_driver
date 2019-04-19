#! /usr/bin/env python3

import rospy, os, sys, time, serial, threading
from std_msgs.msg import String
from std_msgs.msg import Float64

from pymeasure_tpg261 import tpg261

class tpg261_driver(object):
    def __init__(self):

        self.pub_p = rospy.Publisher("/tpg_pressure", Float64, queue_size=1)
        self.pub_er = rospy.Publisher("/tpg_error", String, queue_size=1)
        self.pub_g1 = rospy.Publisher("/tpg_gauge1", String, queue_size=1)
        self.pub_g2 = rospy.Publisher("/tpg_gauge2", String, queue_size=1)
        self.dev = tpg261.device()

    def query_pressure(self):
        while not rospy.is_shutdown():
            self.dev.pressure()
            self.dev.pressure_error()
            self.b = self.dev.check()
            status = self.dev.pressure_error()
            if self.b == 0:
                pressure = self.dev.pressure()
                pres = float(pressure)
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


    def check_gauge(self):
        self.dev.gauge_query()
        self.dev.gauge1_check()
        self.dev.gauge2_check()
        print(status1)
        if status1 == b'0':
            msg = String()
            msg.data = "CannotBeChanged"
            self.pub_g1.publish(msg)
        elif status1 == b'1':
            msg = String()
            msg.data = "TurnedOff"
            self.pub_g1.publish(msg)
        elif status1 == b'2':
            msg = String()
            msg.data = "TurnedOn"
            self.pub_g1.publish(msg)
        else:
            pass

        if status2 == b'0':
            msg = String()
            msg.data = "CannotBeChanged"
            self.pub_g2.publish(msg)
        elif status2 == b'1':
            msg = String()
            msg.data = "TurnedOff"
            self.pub_g2.publish(msg)
        elif status2 == b'2':
            msg = String()
            msg.data = "TurnedOn"
            self.pub_g2.publish(msg)
        else:
            pass

'''
    def query_bothpressure(self):
        while not rospy.is_shutdown():
            self.dev.pressure_both()
            if raw2 == b'\x06\r\n':
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





    def turn_gauge(self):
        self.dev.gauge_change(gague1,gague2)
        if status1 == b'0':
            msg = String()
            msg.data = CannotBeChanged
            self.pub_p.publish(msg)
        elif status1 == b'1':
            msg = String()
            msg.data = TurnedOff
            self.pub_p.publish(msg)
        elif status1 == b'2':
            msg = String()
            msg.data = TurnedOn
            self.pub_p.publish(msg)
        else:
            pass

        if status2 == b'0':
            msg = String()
            msg.data = CannotBeChanged
            self.pub_p.publish(msg)
        elif status2 == b'1':
            msg = String()
            msg.data = TurnedOff
            self.pub_p.publish(msg)
        elif status2 == b'2':
            msg = String()
            msg.data = TurnedOn
            self.pub_p.publish(msg)
        else:
            pass

    def display_gauge1(self):
        self.dev.change_gague1()
        msg = String()
        msg.data = gague1
        self.pub_p.publish(msg)

    def display_gauge2(self):
        self.dev.change_gague2()
        msg = String()
        msg.data = gague2
        self.pub_p.publish(msg)

    def error_status(self):
        self.dev.query_error()
        if status == b'0000':
            msg = String()
            msg.data = NoError
            self.pub_p.publish(msg)
        elif status == b'1000':
            msg = String()
            msg.data = ControllerErrorSeeDisplay
            self.pub_p.publish(msg)
        elif status == b'0100':
            msg = String()
            msg.data = NoHardware
            self.pub_p.publish(msg)
        elif status == b'0010':
            msg = String()
            msg.data = InadmissibleParameter
            self.pub_p.publish(msg)
        elif status == b'0001':
            msg = String()
            msg.data = Syntaxerror
            self.pub_p.publish(msg)
        else:
            pass
'''

if __name__ == "__main__" :
    rospy.init_node("tpg261")
    tpg = tpg261_driver()
    thread_tpg = threading.Thread(target=tpg.query_pressure)
    thread_tpg.start()






#2019
#written by T.Takashima
