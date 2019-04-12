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
            self.dev.pressure_both()
            if raw1 == b'\x06\r\n':
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
        self.dev.gauge_check()

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


if __name__ == "__main__" :
    rospy.init_node("tpg261")
    tpg = tpg261_driver()
    thread1_tpg = threading.Thread(target=tpg.query_pressure)
    thread2_tpg = threading.Thread(target=tpg.query_bothpressure)
    thread1_tpg.start()
    thread2_tpg.start()
    tpg.query_pressure()
    tpg.query_bothpressure()

#2019
#written by T.Takashima
