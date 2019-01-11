#! /usr/bin/env python3

import sys
import time
import pymeasure

import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String

class phasematrix_controller(object):

    def __init__(self):
        self.host = rospy.get_param('~host')
        self.port = rospy.get_param('~port')
        self.rate = rospy.get_param('~rate')
        ###=== Create instance ===###
        try:
            com = pymeasure.ethernet(self.host, self.port)
            self.sg = pymeasure.Phasematrix.FSW0010(com)
        except OSError as e:
            rospy.logerr("{e.strerror}. node={node_name}".format(self.node_name, self.rsw_id))
        ###=== Define topic ===###
        topic_freq = 'phasematrix_freq'
        topic_power = 'phasematrix_power'
        topic_onoff = 'phasematirx_onoff'
        ###=== Define Publisher ===###
        self.pub_freq = rospy.Publisher(topic_freq, Float64, queue_size=1)
        self.pub_power = rospy.Publisher(topic_power, Float64, queue_size=1)
        self.pub_onoff = rospy.Publisher(topic_onoff, String, queue_size=1)
        ###=== Define Subscriber ===###
        self.sub_freq = rospy.Subscriber(topic_freq+'_cmd', Float64, self.freq_set)
        self.sub_power = rospy.Subscriber(topic_power+'_cmd', Float64, self.power_set)
        self.sub_onoff = rospy.Subscriber(topic_onoff+'_cmd', String, self.onoff_set)

    def freq_set(self, q):
        self.sg.freq_set(freq=q.data, unit='Hz')
        time.sleep(1)
        freq = self.sg.freq_query()
        print(freq)
        print(type(freq))
        self.pub_freq.Publish(freq)
        return

    def power_set(self, q):
        self.sg.power_set(pow=q.data, unit='dBm')
        power = self.sg.power_query()
        self.pub_power.Publish(power)
        return

    def onoff_set(self, q):
        if q.data == 'on': self.sg.output_on()
        if q.data == 'off': self.sg.output_off()
        onoff = self.sg.output_query()
        self.pub_onoff.Publish(onoff)
        pass

if __name__ == '__main__':
    rospy.init_node('phasematrix')
    phasematrix_controller()
    rospy.spin()
