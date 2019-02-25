import rospy, os, sys, time, serial, threading
from std_msgs.msg import Float64
from std_msgs.msg import String

class tpg261_driver(object):
    def __init__(self):

        self.pub_p = rospy.Publisher("/tpg_pressure", Float64, queue_size=1)
        self.pub_p = rospy.Publisher("/tpg_status", String, queue_size=1)

        self.tpg261 = serial.Serial("/dev/ttyUSB1",timeout=1)

    def query_pressure(self):
        while not rospy.is_shutdown():
            self.tpg261.write(b"PR1 \r[\n]")
            time.sleep(1.0)
            raw = self.tpg261.write(b"\x05")
            time.sleep(1.0)
            status = raw[0:1]
            pressure = raw[2:13]
            if status == b'2':
                 msg = String()
                 msg.data = Overrange
                 self.pub_status.publish(msg)
            elif status == b'0':
                 msg = Float64()
                 msg.data = float(pressure)
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
