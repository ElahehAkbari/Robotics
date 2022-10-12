#!/usr/bin/python3

import rospy
import tf

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

from math import radians, sqrt
from dis import dis
from matplotlib import pyplot as plt
import numpy as np

import os
my_path = os.path.abspath(__file__)

X1 = np.linspace(-2, 2 , 100)

Y2 = np.linspace(-3, 3 , 100)

X3 = np.linspace(-2, 2 , 100)

Y4 = np.linspace(-3, 3 , 100)


class Controller:
    
    def __init__(self) -> None:
        
        rospy.init_node("controller" , anonymous=False)
        rospy.on_shutdown(self.on_shutdown)

        sub = rospy.Subscriber("/odometry/filtered", Odometry, self.get_heading)
        self.cmd_publisher = rospy.Publisher('/cmd_vel' , Twist , queue_size=10)

        # getting specified parameters
        self.linear_speed = rospy.get_param("/controller/linear_speed") # m/s
        self.angular_speed = rospy.get_param("/controller/angular_speed") # rad/s
        self.goal_angle = radians(rospy.get_param("/controller/goal_angle")) # rad
        self.stop_distance = rospy.get_param("/controller/stop_distance") # m
        self.epsilon = rospy.get_param("/controller/epsilon")

        
        # defining the states of our robot
        self.GO, self.ROTATE = 0, 1
        self.state = self.GO 

        self.rect_points = []
        self.errors =[]

        for x in X1:
            self.rect_points.append([x,3.0])

        for y in Y2:
            self.rect_points.append([2.0,y])

        for x in X3:
            self.rect_points.append([x,-3.0])

        for y in Y4:
            self.rect_points.append([-2.0,y])

    # heading of the robot 
    def get_heading(self, euler = True):
        
        # waiting for the most recent message from topic /odom
        msg = rospy.wait_for_message("/odom" , Odometry)
        
        orientation = msg.pose.pose.orientation
        
        # convert quaternion to odom
        roll, pitch, yaw = tf.transformations.euler_from_quaternion((
            orientation.x ,orientation.y ,orientation.z ,orientation.w
        )) 
        if euler:
            return yaw
        return  msg.pose.pose.position

    def move_forward(self):
        twist = Twist()
        twist.linear.x = self.linear_speed
        self.cmd_publisher.publish(twist)

    def rotate(self):
        twist = Twist()
        self.cmd_publisher.publish(Twist())
        rospy.sleep(1)

        remaining = self.goal_angle
        prev_angle = self.get_heading()
        
        twist = Twist()
        twist.angular.z = self.angular_speed
        self.cmd_publisher.publish(twist)
        
        # rotation loop
        while remaining >= self.epsilon:
            current_angle = self.get_heading()
            delta = abs(prev_angle - current_angle)
            remaining -= delta
            prev_angle = current_angle
        
        self.cmd_publisher.publish(Twist())
               

    def move_rec(self, x,y, length):
        current_pose = self.get_heading(False)
        self.errors.append(cal_error(self.rect_points, current_pose.x, current_pose.y))
        while cal_distance(current_pose.x,current_pose.y,x,y) <= length:
            self.move_forward()
            current_pose = self.get_heading(False)
            self.errors.append(cal_error(self.rect_points, current_pose.x, current_pose.y))
        self.rotate()
        return 

    def run(self):

        self.move_rec(-2,0,4)

        while not rospy.is_shutdown():
            self.move_rec(2,3,6)

            self.move_rec(2,-3,4)

            self.move_rec(-2,-3,6)

            self.move_rec(-2,3,4)

            self.state = self.GO

    def on_shutdown(self):
        rospy.loginfo("shut down")
        plt.figure()
        plt.plot(range(len(self.errors)), self.errors)
        plt.xlabel('Seconds')
        plt.ylabel('Error on path')
        plt.legend()
        plt.title('Error plot')
        # my_file = f"errors_{self.linear_speed}.png"
        plt.savefig(f"{my_path}_errors_{self.linear_speed}.png")
        plt.show()

        rospy.sleep(1)

def cal_error(rect_points,x,y):
    dist = []
    for p in rect_points:
        dist.append(cal_distance(p[0],p[1],x,y))
    return min(dist)

def cal_distance(x1,y1,x2,y2):
    return sqrt((float(x1) - float(x2)) ** 2 + (float(y1) - float(y2)) ** 2)

if __name__ == "__main__":
    controller = Controller()
    controller.run()
