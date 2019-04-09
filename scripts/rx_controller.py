#! /usr/bin/env python3
import rospy
import os, sys, time ,datetime

import std_msgs
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32

class controllaer(object):
    def __init__(self):

        self.sis_iv = sis_iv()
        self.logger = logger()
        self.chopper = chopper()


class sis_iv(object):
    def __init__(self):
        ch = rospy.get_param("~sis_ch"))

        pub_list = [rospy.Publisher('/sis_vol_cmd_ch{i}'.format(i), Float64, queue_size=1) for i in ch]

    def measure(self, initv, interval, repeat):
        for i in range(repeat+1):
            vol = initv+interval*i
            msg = Float64()
            msg.data = vol
            [pub.publish(msg) for pub in pub_list]
            time.sleep(0.1)


class logger(object):
    def __init__(self):

    self.pub_piv_logger = rospy.Publisher("/sis_piv_logger_flag", String, queue_size=1)
    self.pub_XFFTS_logger = rospy.Publisher("/XFFTS_logger_flag", String, queue_size=1)

    def start(self, flag):
        pass


class chopper(object):
    def __init__(self):
        pass

    def jog(self, ):
        pass

    def ptp(self, ):
        pass

class phasematrix(object):
    def __init__(self):
        pass

    def output(self, freq):
        pass


class e8250d_signal_generateor(object):
    def __init__(self):
        pass

    def output(self, freq):
        pass


class usbpm(object):
    def __init__(self):
        pass

    def output(self, freq):
        pass



if __name__ == "__main__" :
    rospy.init_node("rx_controller")


#20190408
#written by H.Kondo
