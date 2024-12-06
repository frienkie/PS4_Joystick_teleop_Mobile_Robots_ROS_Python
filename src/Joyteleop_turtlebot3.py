#! /usr/bin/env python
import numpy as np
import rospy
import roslib
import subprocess
import time
from geometry_msgs.msg  import Twist
from sensor_msgs.msg import Joy
import sys
import signal

def signal_handler(signal, frame): # ctrl + c -> exit program
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
''' class '''
class robot():
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        print("human is 0,share is 1")
        x=input()
        if x=="0":
            self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        elif x=="1":
            self.velocity_publisher = rospy.Publisher('cmd_vel_human', Twist, queue_size=1)
        else:
            rospy.loginfo("input error,run as human")
            self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        #self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        #self.velocity_publisher = rospy.Publisher('/cmd_vel_human', Twist, queue_size=1)
        self.pose_subscriber2 = rospy.Subscriber('/joy',Joy,self.callback)
        self.rate = rospy.Rate(20)

    def callback(self, data):
        global inn
        inn=0
        # global flag
        # flag=1
        self.joy = data.buttons
        self.joy2= data.axes

        if np.shape(self.joy)[0]>0:
            inn=1
            self.nemo=self.joy[0]#A
            self.semo=self.joy[3]#Y
            self.one=self.joy[2]#X
            self.x=self.joy[1]#B
            self.lb=self.joy[4]
            self.rb=self.joy[5]
        if np.shape(self.joy2)[0]>0:
            inn=1
            self.linear=self.joy2[1]
            self.angular=self.joy2[3]
            self.lt=-(self.joy2[2]-1)
            self.rt=-(self.joy2[5]-1)
            #self.angular=self.joy2[0]
        # if inn==1:
        #     if self.joy[0]==0 and self.joy[1]==0 and self.joy[2]==0 and self.joy[3]==0 and self.joy2[1] and self.joy2[3] and self.joy2[2] and self.joy2[5]:
        #         inn=0
        #     else:
        #         pass
    def moving(self,vel_msg):
        self.velocity_publisher.publish(vel_msg)


data=Joy()
vel_msg=Twist()
efficient = 0.6 # 角度增益


''' robot position '''
turtle = robot()
turtle.callback(data) #without this, getting error


''' main '''
if __name__ == '__main__':
 while 1:
    # if inn==1:
    #     if turtle.one==1:
    #         time.sleep(0.05) # 休眠0.05秒
    #         if turtle.one==1:
    #             inn=0
    #             time.sleep(0.5)
    # if inn==0:
    #     if turtle.one==1:
    #         time.sleep(0.05) # 休眠0.05秒
    #         if turtle.one==1:
    #             inn=1
    #             time.sleep(0.5)
    if inn==1:
        if turtle.x==1 or turtle.rt>0.1:
             vel_msg.linear.x=0
             vel_msg.angular.z=0
        elif turtle.nemo==1:#slow
             vel_msg.linear.x=turtle.linear*0.1
             vel_msg.angular.z=turtle.angular*0.2
        elif turtle.semo==1:
             #subprocess.call('',shell=True)
             p=subprocess.Popen('rostopic pub /reset std_msgs/Empty "{}"',shell=True)
             time.sleep(2)
             p.terminate()
        elif turtle.lb==1:
            vel_msg.angular.z=1
            vel_msg.linear.x=turtle.linear*0.2
        elif turtle.rb==1:
            vel_msg.angular.z=-1
            vel_msg.linear.x=turtle.linear*0.2

        # elif turtle.one==1:#quick
        elif turtle.lt>0 and turtle.linear>0:
             vel_msg.linear.x=turtle.linear*0.2
             vel_msg.angular.z=turtle.angular*abs(turtle.angular)*efficient
        elif turtle.lt>0:
            vel_msg.linear.x=turtle.lt/2*0.2
            vel_msg.angular.z=turtle.angular*abs(turtle.angular)*efficient
        else:
            vel_msg.linear.x=turtle.linear*0.2
            vel_msg.angular.z=turtle.angular*abs(turtle.angular)*efficient
        turtle.moving(vel_msg)
    # else:
    #     print('no joystick input')
    #     vel_msg.linear.x=0
    #     vel_msg.angular.z=0
    #     turtle.moving(vel_msg) 

    #    flag=1        
    # else:
    #     if flag==1:
    #         print('stop')
    #         flag=0
    #     vel_msg.linear.x=0
    #     vel_msg.angular.z=0
    #     turtle.moving(vel_msg) 
    turtle.rate.sleep()