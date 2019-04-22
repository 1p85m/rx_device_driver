#! /usr/bin/env python3


import sys
import time
import pymeasure

import rospy
from std_msgs.msg import Float64

from pymeasure_l218 import l218

def str2list(param):
    return param.strip('[').strip(']').split(',')


if __name__ == '__main__':
    node_name = 'lakeshore_218'
    rospy.init_node(node_name)

    ch_number = 8
    topic_name_index = 0
    onoff_index = 1
    host = rospy.get_param('~host')
    port = rospy.get_param('~port')
    rate = rospy.get_param('~rate')
    onoff_list = list(map(int, str2list(rospy.get_param('~onoff'))))
    print(onoff_list)

    try:
        temp = l218.lakeshore218_driver(host, port)
    except OSError as e:
        rospy.logerr("{e.strerror}. host={host}".format(**locals()))
        sys.exit()

    pub_list = [rospy.Publisher('lakeshore_ch{0}'.format(ch),
                                Float64,
                                queue_size=1) \
                for ch, onoff in enumerate(onoff_list, start=1) if onoff == 1]

    while not rospy.is_shutdown():

        ret = temp.measure()
        for pub, onoff, idx in zip(pub_list, onoff_list, range(8)):
            msg = Float64()
            if onoff == 1:
                msg.data = ret[idx]
                print(msg)
                pub.publish(msg)
            else: pass
        continue
