#! /usr/bin/env python3

import sys
import time

import pymeasure

import rospy
import std_msgs
from std_msgs.msg import Float64
from std_msgs.msg import String
from std_msgs.msg import Int32


class ml2437a_controller(object):
    def __init__(self):

        self.pm = ml2437a_driver()

        self.pub_ave_onoff = rospy.Publisher("topic_pub_ave_onoff", Int32, queue_size = 1)
        self.sub_ave_onoff = rospy.Subscriber("topic_sub_ave_onoff", Int32, self.ave_onoff)
        self.pub_ave_count = rospy.Publisher("topic_pub_ave_count", Int32, queue_size = 1)
        self.sub_ave_count = rospy.Subscriber("topic_sub_ave_count", Int32, self.ave_count)
        self.pub_vol_start = rospy.Publisher("topic_pub_vol_start", Float64, queue_size = 1)
        self.sub_vol_start = rospy.Subscriber("topic_sub_vol_start", Float64, self.vol_start)
        self.pub_vol_stop = rospy.Publisher("topic_pub_vol_stop", Float64, queue_size = 1)
        self.sub_vol_stop = rospy.Subscriber("topic_sub_vol_stop", Float64, self.vol_stop)
        self.pub_val_start = rospy.Publisher("topic_pub_val_start", Float64, queue_size = 1)
        self.sub_val_start = rospy.Subscriber("topic_sub_val_start", Float64, self.val_start)
        self.pub_val_stop = rospy.Publisher("topic_pub_val_stop", Float64, queue_size = 1)
        self.sub_val_stop = rospy.Subscriber("topic_sub_val_stop", Float64, self.val_stop)


    def ave_onoff(self,q):
        self.pm.set_average_onoff(q.data)
        ret = self.pm.query_average_onoff()
        msg = Int32()
        msg.data = int(ret)
        self.pub_ave_onoff.publish(msg)

    def ave_count(self,q):
        self.pm.set_average_count(q.data)
        ret = self.pm.query_average_count()
        msg = Int32()
        msg.data = int(ret)
        self.pub_ave_count.publish(msg)


    def vol_start(self,q):
        self.pm.set_voltage_start(q.data)
        ret = self.pm.query_voltage_start()
        ret = float(ret[8:])
        msg = Float64()
        msg.data = ret
        self.pub_vol_start.publish(msg)


    def vol_stop(self,q):
        self.pm.set_voltage_stop(q.data)
        ret = self.pm.query_voltage_stop()
        ret = float(ret[8:])
        msg = Float64()
        msg.data = ret
        self.pub_vol_stop.publish(msg)


    def val_start(self,q):
        self.pm.set_value_start(q.data)
        ret = self.pm.query_value_start()
        ret = float(ret[11:])
        msg = Float64()
        msg.data = ret
        self.pub_val_start.publish(msg)

    def val_stop(self,q):
        self.pm.set_value_stop(q.data)
        ret = self.pm.query_value_stop()
        ret = float(ret[11:])
        msg = Float64()
        msg.data = ret
        self.pub_val_stop.publish(msg)


class ml2437a_driver(object):

    def __init__(self, ch=1, resolution=3):
        self.IP = IP
        self.GPIB = GPIB
        self.com = pymeasure.gpib_prologix(self.IP, self.GPIB)
        self.com.open()
        self.com.send('CHUNIT %d, DBM' %(ch))
        self.com.send('CHRES %d, %d' %(ch, resolution))

    def measure(self, ch=1, resolution=3):
        '''
        DESCRIPTION
        ================
        This function queries the input power level.
        ARGUMENTS
        ================
        1. ch: the sensor channel number.
            Number: 1-2
            Type: int
            Default: 1
        2. resolution: the sensor order of the resolution.
            Number: 1-3
            Type: int
            Default: 3
        RETURNS
        ================
        1. power: the power value [dBm]
            Type: float
        '''
        self.com.send('o %d' %(ch))
        ret = self.com.readline()
        power = float(ret)
        return power

    def set_average_onoff(self, onoff, sensor='A'):
        '''
        DESCRIPTION
        ================
        This function switches the averaging mode.
        ARGUMENTS
        ================
        1. onoff: averaging mode
            Number: 0 or 1
            Type: int
            Default: Nothing.
        2. sensor: averaging sensor.
            Number: 'A' or 'B'
            Type: string
            Default: 'A'
        RETURNS
        ================
        Nothing.
        '''

        if onoff == 1:
            self.com.send('AVG %s, RPT, 60' %(sensor))
        else:
            self.com.send('AVG %s, OFF, 60' %(sensor))
        return

    def query_average_onoff(self):
        '''
        DESCRIPTION
        ================
        This function queries the averaging mode.
        ARGUMENTS
        ================
        Nothing.
        RETURNS
        ================
        1. onoff: averaging mode
            Number: 0 or 1
            Type: int
        '''

        self.com.send('STATUS')
        ret = self.com.readline()
        if ret[17] == '0':
            ret = 0
        else:
            ret = 1
        return ret

    def set_average_count(self, count, sensor='A'):
        '''
        DESCRIPTION
        ================
        This function sets the averaging counts.
        ARGUMENTS
        ================
        1. count: averaging counts
            Type: int
            Default: Nothing.
        2. sensor: averaging sensor.
            Number: 'A' or 'B'
            Type: string
            Default: 'A'
        RETURNS
        ================
        Nothing.
        '''

        self.com.send('AVG %s, RPT, %d' %(sensor, count))

        return

    def query_average_count(self):
        '''
        DESCRIPTION
        ================
        This function queries the averaging counts.
        ARGUMENTS
        ================
        Nothing.
        RETURNS
        ================
        1. count: averaging counts
            Type: int
        '''
        self.com.send('STATUS')
        ret = self.com.readline()
        count = int(ret[19:23])

        return count

    def set_voltage_start(self, vstart, output = '1'):
        self.com.send('OBVST %s, %f' %(output, vstart))
        return

    def query_voltage_start(self, output = '1'):
        self.com.send('OBVST? %s' %(output))
        ret = self.com.readline()
        return ret

    def set_voltage_stop(self, vstop, output = '1'):
        self.com.send('OBVSP %s, %f' %(output, vstop))
        return

    def query_voltage_stop(self, output = '1'):
        self.com.send('OBVSP? %s' %(output))
        ret = self.com.readline()
        return ret

    def set_value_start(self, start, output = '1'):
        self.com.send('OBDST %s, DBM, %f' %(output, start))
        return

    def query_value_start(self, output = '1'):
        self.com.send('OBDST? %s' %(output))
        ret = self.com.readline()
        return ret

    def set_value_stop(self, stop, output = '1'):
        self.com.send('OBDSP %s, DBM, %f' %(output, stop))
        return

    def query_value_stop(self, output = '1'):
        self.com.send('OBDSP? %s' %(output))
        ret = self.com.readline()
        return ret

if __name__ == "__main__" :
    rospy.init_node("ml2437a")
    GPIB = rospy.get_param('~port')
    IP = rospy.get_param('~host')

    ctrl = ml2437a_controller()
    rospy.spin()

#2019/03/20
#written by H.Kondo
