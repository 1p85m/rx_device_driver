#! /usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from std_msgs.msg import String
import serial
import time
import sys,os
import threading

sys.path.append("/root/python")
import pymeasure_usbpm


class ma24126a_controller(object):
    def __init__(self):

        self.pm = pymeasure_usbpm.usbpm.open("ma24126a")
        self.rate = rospy.get_param("~rate")

#flag
        self.start_flag = 0
        self.zero_set_flag = 0
        self.close_flag = 0
        self.power_flag = 0
        self.avemode_flag = 0
        self.avetyp_flag = 0
        self.capt_flag = 0
        self.mode_flag = 0


#pubsub
        rospy.Subscriber("ma24126a_start_cmd", Float64, self.start_switch)
        rospy.Subscriber("ma24126a_zero_set_cmd", Float64, self.zero_set_switch)
        rospy.Subscriber("ma24126a_close_cmd", Float64, self.close_switch)
        rospy.Subscriber("ma24126a_power_cmd", Float64, self.power_switch)
        rospy.Subscriber("ma24126a_avemode_cmd", Float64, self.avemode_switch)
        rospy.Subscriber("ma24126a_avetyp_cmd", Float64, self.avetyp_switch)
        rospy.Subscriber("ma24126a_capt_cmd", Float64, self.capt_switch, callback_args=1)
        rospy.Subscriber("ma24126a_avemode_cmd", Float64, self.avemode_switch, callback_args=1)

        self.pub_power = rospy.Publisher("ma24126a_power", Float64, queue_size = 100)

        print("Doing zero setting now")
        self.pm.zero_set()
        print("Finish zero setting !!")

#flag
    def start_switch(self,q):
        self.start_flag = q.data
        return

    def zero_set_switch(self,q):
        self.zero_set_flag = q.data
        return

    def close_switch(self,q):
        self.close_flag = q.data
        return

    def power_switch(self,q):
        self.power_flag = q.data
        return

    def capt_switch(self,q):
        self.capt = q.data
        self.capt_flag = 1
        return

    def avemode_switch(self,q):
        self.avemode = q.data
        self.avemode_flag = 1
        return

    def avetyp_switch(self,q):
        self.avetyp = q.data
        self.avetyp_flag = 1
        return

    def mode_switch(self,q,flag):
        self.mode = q.data
        self.mode_flag = flag
        return

#main methond

    def start(self):
        while not rospy.is_shutdown():
            if self.start_flag == 0:
                continue

            self.pm.start()
            time.sleep(0.1)
            self.start_flag = 0
            continue

    def zero_set(self):
        while not rospy.is_shutdown():
            if self.zero_set_flag == 0:
                continue

            self.pm.zero_set()
            time.sleep(0.1)

            self.zero_set_flag = 0
            continue


    def power(self):
        msg = Float64()
        while not rospy.is_shutdown():
            if self.power_flag == 0:
                continue

            while self.power_flag == 1:
                ret = self.pm.power()
                msg.data = float(ret)
                self.pub_power.publish(msg)

            continue

    """
    def power(self):
        msg = Float64()
        while True:
            ret = self.pm.power()
            msg.data = float(ret)
            self.pub_power.publish(msg)
            continue
    """

    def close(self):
        while not rospy.is_shutdown():
            if self.close_flag == 0:
                continue
            self.pm.close()
            self.close_flag = 0
            continue

    def change_capt(self):
        while not rospy.is_shutdown():
            if self.capt_flag == 0:
                continue

            self.pm.change_capt(self.capt)

            self.capt_flag = 0
            continue

    def change_avemode(self):
        while not rospy.is_shutdown():
            if self.avemode_flag == 0:
                continue

            self.pm.change_avemode(self.avemode)

            self.avemode_flag = 0
            continue

    def change_avetyp(self):
        while not rospy.is_shutdown():
            if self.avetyp_flag == 0:
                continue

            self.pm.change_avetyp(self.avetyp)

            self.avetyp_flag = 0
            continue

    def change_mode(self):
        while not rospy.is_shutdown():
            if self.mode_flag == 0:
                continue

            self.pm.change_mode(self.mode)

            self.mode_flag = 0
            continue

#thread

    def start_thread(self):
        th1 = threading.Thread(target=self.power)
        th1.setDaemon(True)
        th1.start()
        th2 = threading.Thread(target=self.change_capt)
        th2.setDaemon(True)
        th2.start()
        th3 = threading.Thread(target=self.change_avemode)
        th3.setDaemon(True)
        th3.start()
        th4 = threading.Thread(target=self.zero_set)
        th4.setDaemon(True)
        th4.start()
        th5 = threading.Thread(target=self.close)
        th5.setDaemon(True)
        th5.start()
        th6 = threading.Thread(target=self.change_avetyp)
        th6.setDaemon(True)
        th6.start()
        th7 = threading.Thread(target=self.change_mode)
        th7.setDaemon(True)
        th7.start()

if __name__ == "__main__" :
    rospy.init_node("ma24126a")
    ctrl = ma24126a_controller()
    ctrl.start_thread()
    rospy.spin()
