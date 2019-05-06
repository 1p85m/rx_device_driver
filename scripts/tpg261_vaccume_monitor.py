#! /usr/bin/env python3

import rospy, os, sys, time, serial, threading
from std_msgs.msg import String
from std_msgs.msg import Float64

from pymeasure_tpg261 import tpg261

class tpg261_driver(object):
    def __init__(self):

        self.pub_p = rospy.Publisher("/tpg_pressure", Float64, queue_size=1)
        self.sub_p = rospy.Subscriber("/tpg_pres_sub", Float64, self.pres_switch)
        self.pub_er = rospy.Publisher("/tpg_error", String, queue_size=1)
        self.pub_g = rospy.Publisher("/tpg_gauge", String, queue_size=1)
        self.pub_g1 = rospy.Publisher("/tpg_gauge1", String, queue_size=1)
        self.pub_g2 = rospy.Publisher("/tpg_gauge2", String, queue_size=1)
        self.pub_uni = rospy.Publisher("/tpg_unit", String, queue_size=1)
        self.dev = tpg261.device()
#flag
        self.pres_flag = 3
        '''
        0:check gague
        1:pressure
        2:unit
        3:change gauge

        '''
        self.unit_flag = 2
        '''
        0:bar
        1:torr
        2:pa
        '''
        self.gauge_flag = 2
        '''
        1:gauge1 On
        2:gague2 On
        3:gague1 2 Off
        '''
#switch
    def pres_switch(self,q):
        self.pres_flag = q.data
        return

    def query_pressure(self):
        while not rospy.is_shutdown():
            while self.pres_flag != 1 :
                continue

            while self.pres_flag == 1 :
                self.dev.pressure()
                self.dev.pressure_error()
                self.b = self.dev.check()
                status_p = self.dev.pressure_error()
                if self.b == 0:
                    pressure = self.dev.pressure()
                    pres = float(pressure)
                    self.pub_p.publish(pres)
                    continue
                else:
                    if status_p == b'2':
                        msg = String()
                        msg.data = "Overrange"
                        self.pub_er.publish(msg)
                    elif status_p == b'0':
                        msg = String()
                        msg.data = "pressure"
                        self.pub_er.publish(msg)
                    else:
                        error = self.dev.pressure_error()
                        self.pub_er.publish(error)
                        pass

#subのなかにpubを置く
    def check_gauge_s(self):
        self.tpg.check_gauge()

    def check_gauge(self):
        while not rospy.is_shutdown():
            while self.pres_flag != 0 :
                continue

            while self.pres_flag == 0 :

                self.pres_flag = 0
                time.sleep(0.3)
                self.dev.gauge_query()
                status1_g = self.dev.gauge1_check()
                status2_g = self.dev.gauge2_check()
                self.gauge_moniter()

    def change_gauge(self):
        while not rospy.is_shutdown():
            while self.pres_flag != 3 :
                continue

            while self.pres_flag == 3 and self.gauge_flag == 1 :
                time.sleep(0.3)
                self.dev.gauge_change_1()
                status1_g = self.dev.gauge1_check()
                status2_g = self.dev.gauge2_check()
                self.gauge_moniter()

            while self.pres_flag == 3 and self.gauge_flag == 2 :
                time.sleep(0.3)
                self.dev.gauge_change_2()
                status1_g = self.dev.gauge1_check()
                status2_g = self.dev.gauge2_check()
                self.gauge_moniter()

            while self.pres_flag == 3 and self.gauge_flag == 3 :
                time.sleep(0.3)
                self.dev.gauge_change_Off1_2()
                status1_g = self.dev.gauge1_check()
                status2_g = self.dev.gauge2_check()
                self.gauge_moniter()


    def gauge_moniter(self,status1_g,status2_g):
        #status1_g = self.dev.gauge1_check()
        #status2_g = self.dev.gauge2_check()
        if status1_g == b'0' and status2_g == b'0':
            msg = String()
            msg.data = "CannotBeChanged_1And_2"
            self.pub_g.publish(msg)
        elif status1_g == b'1' and status2_g == b'1':
            msg = String()
            msg.data = "TurnedOff_1And_2"
            self.pub_g.publish(msg)
        elif status1_g == b'2' and status2_g == b'2':
            msg = String()
            msg.data = "TurnedOn_1And_2"
            self.pub_g.publish(msg)
        elif status1_g == b'0' and status2_g == b'1':
            msg = String()
            msg.data = "CannotBeChanged_1TurnedOff_2"
            self.pub_g.publish(msg)
        elif status1_g == b'0' and status2_g == b'2':
            msg = String()
            msg.data = "CannotBeChanged_1TurnedOn_2"
            self.pub_g.publish(msg)
        elif status1_g == b'1' and status2_g == b'0':
            msg = String()
            msg.data = "TurnedOff_1CannotBeChanged_2"
            self.pub_g.publish(msg)
        elif status1_g == b'1' and status2_g == b'2':
            msg = String()
            msg.data = "TurnedOff_1TurnedOn_2"
            self.pub_g.publish(msg)
        elif status1_g == b'2' and status2_g == b'0':
            msg = String()
            msg.data = "TurnedOn_1CannotBeChanged_2"
            self.pub_g.publish(msg)
        elif status1_g == b'2' and status2_g == b'1':
            msg = String()
            msg.data = "TurnedOn_1TurnedOff_2"
            self.pub_g.publish(msg)
            pass

                #self.pres_flag = 1


    def change_unit(self):
        while not rospy.is_shutdown():
            while self.pres_flag != 2:
                continue

            while self.pres_flag == 2 :
                self.pres_flag = 2
                time.sleep(0.3)

                if self.unit_flag == 0:
                    unit = self.dev.pres_unit_bar()
                    if unit == b'0':
                        msg = String()
                        msg.data = "mbarORbar"
                        self.pub_uni.publish(msg)
                    else:
                        pass
            #        self.pres_flag = 1

                elif self.unit_flag == 1:
                    unit = self.dev.pres_unit_torr()
                    if unit == b'1':
                        msg = String()
                        msg.data = "Torr"
                        self.pub_uni.publish(msg)
                    else:
                        pass
            #        self.pres_flag = 1

                elif self.unit_flag == 2:
                    unit = self.dev.pres_unit_pa()
                    if unit == b'2':
                        msg = String()
                        msg.data = "Pascal"
                        self.pub_uni.publish(msg)
                    else:
                        pass
        #            self.pres_flag = 1
                else:
                    pass


'''
    def change_unit_bar(self,q):
        self.pres_flag = 0
        time.sleep(1)
        self.dev.pres_unit_bar()
        unit = self.dev.pres_unit_bar()
        if unit == b'0':
            msg = String()
            msg.data = "mbarORbar"
            self.pub_uni.publish(msg)
        else:
            pass
        self.pres_flag = 1

    def change_unit_torr(self,q):
        self.pres_flag = 0
        time.sleep(1)
        self.dev.pres_unit_torr()
        unit = self.dev.pres_unit_torr()
        if unit == b'1':
            msg = String()
            msg.data = "Torr"
            self.pub_uni.publish(msg)
        else:
            pass
        self.pres_flag = 1

    def change_unit_pa(self,q):
        self.pres_flag = 0
        time.sleep(1)
        self.dev.pres_unit_pa()
        unit = self.dev.pres_unit_pa()
        if unit == b'2':
            msg = String()
            msg.data = "Pascal"
            self.pub_uni.publish(msg)
        else:
            pass
        self.pres_flag = 1
'''
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
    thread_tpg_pres = threading.Thread(target=tpg.query_pressure)
    thread_tpg_pres.start()
    thread_tpg_gauge = threading.Thread(target=tpg.check_gauge)
    thread_tpg_gauge.start()
    thread_tpg_unit = threading.Thread(target=tpg.change_unit)
    thread_tpg_unit.start()






#2019
#written by T.Takashima
