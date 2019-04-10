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

    def pub(self):
        pass


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

    def ready(self, flag):
        self.pub_piv_logger.publish("ready")
        self.pub_XFFTS_logger.publish("ready")
        pass

    def start(self, flag):
        self.pub_piv_logger.publish("start")
        self.pub_XFFTS_logger.publish("start")
        pass

    def end(self, flag):
        self.pub_piv_logger.publish("end")
        self.pub_XFFTS_logger.publish("end")
        pass

class chopper(object):
    def __init__(self):
        self.pub_ = rospy.Publisher("", Int64, queue_size=1)
        pass

    def jog(self, ):
        pass

    def ptp(self, ):
        pass

class phasematrix(object):
    def __init__(self):
        self.pub_freq = rospy.Publisher("/phasematrix_freq_cmd", Float64, queue_size=1)
        self.pub_power = rospy.Publisher("/phasematrix_power_cmd", Float64, queue_size=1)
        self.pub_onoff = rospy.Publisher("/phasematrix_onoff_cmd", String, queue_size=1)

    def onoff(self, onoff):
        self.pub_onoff.publish(onoff)
        pass

    def freq(self, freq):
        self.pub_freq.publish(freq)
        pass

    def power(self, power):
        self.pub_power.publish(power)
        pass

class e8250d_signal_generateor(object):
    def __init__(self):
        pass

    def output(self, freq):
        pass

class ml2437a(object):
    def __init__(self):

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
