import rospy, os, sys, threading
import pymeasure
from std_msgs.msg import Int32


class p_att_driver(object):
    def __init__(self, self.ip='192.168.100.28', self.port=6001):

        self.pub_value = rospy.Publisher("/set_p_att1", Int32, queue_size=1)
        self.pub_value = rospy.Publisher("/set_p_att2", Int32, queue_size=1)
        self.pub_state1 = rospy.Publisher("/get_p_att1", Int32, queue_size=1)
        self.pub_state2 = rospy.Publisher("/get_p_att2", Int32, queue_size=1)
        
        com = pymeasure.ethernet(self.ip, self.port)
        IO = pymeasure.SENA.adio(com)

    def query_p_att1(self):
        while not rospy.is_shutdown():
            raw = IO.get_att1()
            msg = Int32()
            msg.data = raw
            self.pub_state1.publish(msg)

    def query_p_att2(self):
        while not rospy.is_shutdown():
            raw = IO.get_att2()
            msg = Int32()
            msg.data = raw
            self.pub_state2.publish(msg)

    def set_p_att1(self, self.value):
        while not rospy.is_shutdown():
            raw = IO._set_att(1, self.value)
            msg = Int32()
            msg.data = raw
            self.pub_value1.publish(msg)

    def set_p_att2(self, self.value):
        while not rospy.is_shutdown():
            raw = IO._set_att(2, self.value)
            msg = Int32()
            msg.data = raw
            self.pub_value2.publish(msg)

if __name__ == "__main__" :
    rospy.init_node("p_att")
    p_att = p_att_driver()
    thread_p_att1 = threading.Thread(target=p_att.query_p_att1)
    thread_p_att2 = threading.Thread(target=p_att.query_p_att2)
    thread_p_att_state1 = threading.Thread(target=p_att.set_p_att1)
    thread_p_att_state2 = threading.Thread(target=p_att.set_p_att2)
    thread_p_att1.start()
    thread_p_att2.start()
    thread_p_att_state1.start()
    thread_p_att_state2.start()
    p_att.query_p_att1()
    p_att.query_p_att2()
    p_att.set_p_att1()
    p_att.set_p_att2()

#2019
#written by T.Takashima
