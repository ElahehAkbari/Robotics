#!/usr/bin/python3

import rospy
import tf

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Point

from math import radians, sqrt
from math import atan2, pi, radians, sqrt
from cmath import rect
import math
from dis import dis
from matplotlib import pyplot as plt
import numpy as np

class Controller:

    
    def __init__(self) -> None:
        
        rospy.init_node("controller" , anonymous=False)
        
        sub = rospy.Subscriber("/odometry/filtered", Odometry, self.get_heading)
        self.cmd_publisher = rospy.Publisher('/cmd_vel' , Twist , queue_size=10)

        # getting specified parameters
        self.linear_speed = rospy.get_param("/controller/linear_speed") # m/s
        self.angular_speed = rospy.get_param("/controller/angular_speed") # rad/s
        self.goal_angle = radians(rospy.get_param("/controller/goal_angle")) # rad
        self.stop_distance = rospy.get_param("/controller/stop_distance") # m
        self.epsilon = rospy.get_param("/controller/epsilon")
        self.twist = Twist()
        
        # defining the states of our robot
        self.GO, self.ROTATE = 0, 1
        self.state = self.GO 

        #params
        self.kp_distance = 0
        self.ki_distance = 0
        self.kd_distance = 0
        self.kp_theta = 0
        self.ki_theta = 0
        self.kd_theta  = 0
        

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

    def make_shape(self, name):
        if name == "rectangle":
            rectangle = []
            X3 = np.linspace(2, -2 , 20)
            X1 = np.linspace(-2, 2 , 20)
            Y2 = np.linspace(3, -3 , 10)
            Y4 = np.linspace(-3, 3 , 10)

            for x in X3:
                rectangle.append([x,3.0])
            
            for x in X1:
                rectangle.append([x,-3.0])
            
            for y in Y2:
                rectangle.append([2.0,y])

            for y in Y4:
                rectangle.append([-2.0,y]) 
            
            self.shape = rectangle

            self.kp_distance = 0.5
            self.ki_distance = 0.00001
            self.kd_distance = 1.5
            self.kp_theta = 1
            self.ki_theta = 0.03
            self.kd_theta = 0.05

        if name == "halfcircles":
            circle = []
            X1 = np.linspace(-6., -2 , 50)
            Y1 = np.zeros((50,))

            x_dim, y_dim = 2,2
            t = np.linspace(np.pi, 0, 100)
            X2 = x_dim * np.cos(t) 
            Y2 = y_dim * np.sin(t)


            X3 = np.linspace(2, 6 , 50)
            Y3 = np.zeros((50,))


            x_dim, y_dim = 6,6
            t = np.linspace(np.pi*2, np.pi, 200)
            X4 = x_dim * np.cos(t) 
            Y4 = y_dim * np.sin(t)

            for i,x in enumerate(X1):
                circle.append([x,Y1[i]])

            for i,x in enumerate(X2):
                circle.append([x,Y2[i]])

            for i,x in enumerate(X3):
                circle.append([x,Y3[i]])

            for i,x in enumerate(X4):
                circle.append([x,Y4[i]])

            self.shape = circle

            self.kp_distance = 10
            self.ki_distance = 20
            self.kd_distance = 1
            self.kp_theta = 1
            self.ki_theta = 0.03
            self.kd_theta = 0.05

        if name == "octagonal":
            octagonal = []
            X1 = np.linspace(-1, 1 , 100)

            X2 = np.linspace(1, 1 + 2**(1/2) , 100)
            Y2 = - (2**(1/2)) * (X2 - 1) + 3


            Y3 = np.linspace(1, -1 , 100)
            X3 = np.array([1 + 2**(1/2)]*100)


            X4 = np.linspace(1 + 2**(1/2), 1, 100)
            Y4 = (2**(1/2)) * (X4 - 1 - 2**(1/2)) -1 


            X5 = np.linspace(1, -1 , 100)

            X6 = np.linspace(-1, -1 - 2**(1/2) , 100)
            Y6 = - (2**(1/2)) * (X6 + 1) - 3 


            Y7 = np.linspace(-1, 1 , 100)
            X7 = np.array([- 1 - 2**(1/2)]*100)


            X8 = np.linspace(-1 - 2**(1/2), -1, 100)
            Y8 = (2**(1/2)) * (X8 + 1 + 2**(1/2)) + 1

            
            for x in X1:
                octagonal.append([x,3])

            for i,x in enumerate(X2):
                octagonal.append([x,Y2[i]])

            for i,x in enumerate(X3):
                octagonal.append([x,Y3[i]])

            for i,x in enumerate(X4):
                octagonal.append([x,Y4[i]])

            for i,x in enumerate(X5):
                octagonal.append([x,-3])

            for i,x in enumerate(X6):
                octagonal.append([x,Y6[i]])

            for i,x in enumerate(X7):
                octagonal.append([x,Y7[i]])

            for i,x in enumerate(X8):
                octagonal.append([x,Y8[i]])

            self.shape = octagonal

            self.kp_distance = 0.8
            self.ki_distance = 0.005
            self.kd_distance = 0.05
            self.kp_theta = 1
            self.ki_theta = 0.03
            self.kd_theta = 0.05

        if name == "logsp":
            logarithmic_spiral = [] 
            a = 0.17
            k = math.tan(a)

            for i in range(150):
                t = i / 20 * math.pi
                dx = a * math.exp(k * t) * math.cos(t)
                dy = a * math.exp(k * t) * math.sin(t)
                logarithmic_spiral.append([dx,dy])
            self.shape = logarithmic_spiral

            self.kp_distance = 10
            self.ki_distance = 20
            self.kd_distance = 1
            self.kp_theta = 1
            self.ki_theta = 0.03
            self.kd_theta = 0.05

        if name == "archsp":
            archimedean_spiral = []
            growth_factor = 0.1

            for i in range(400):
                t = i / 20 * math.pi
                dx = (1 + growth_factor * t) * math.cos(t)
                dy = (1 + growth_factor * t) * math.sin(t)
                archimedean_spiral.append([dx,dy])
            
            self.shape = archimedean_spiral

            self.kp_distance = 15
            self.ki_distance = 15
            self.kd_distance = 1
            self.kp_theta = 1.2
            self.ki_theta = 0.03
            self.kd_theta = 0.05

    def run(self):
        #change the name of argument in this funxtion for each shape
        self.make_shape("logsp")

        while not rospy.is_shutdown():
            prev_th = 0
            for x,y in self.shape:
                total_distance = 0
                prev_distance = 0

                self.cmd_publisher.publish(Twist())
                msg = rospy.wait_for_message("/odom" , Odometry) 
                curr_pose = self.get_heading(False)

                distance = sqrt((x - curr_pose.x)**2 + (y - curr_pose.y)**2)

                while distance > 0.25:
                    curr_th = self.get_heading(True)
                    msg = rospy.wait_for_message("/odom" , Odometry) 
                    curr_pose = self.get_heading(False)

                    path_angle = atan2(y - curr_pose.y , x - curr_pose.x) 
                    
                    if  path_angle > pi/4 or path_angle < -pi/4:
                        if curr_pose.y < y and y < 0 :
                            path_angle = -2*pi + path_angle
                        elif curr_pose.y > y and y >= 0 :
                            path_angle = 2*pi + path_angle

                    if  curr_th <= 0 and prev_th > pi-0.1:
                        curr_th = 2*pi + curr_th
                    elif curr_th > 0 and prev_th < -pi+0.1:
                        curr_th = -2*pi + curr_th
                        


                    distance = sqrt((x - curr_pose.x)**2 + (y - curr_pose.y)**2)

                    rotation_control = self.kp_theta*(path_angle - curr_th)
                    self.twist.angular.z = (rotation_control)
                    line_control = self.kp_distance*distance + self.ki_distance*total_distance + self.kd_distance*(distance - prev_distance)
                    self.twist.linear.x = min(line_control,0.1)

                    if self.twist.angular.z > 0:
                        self.twist.angular.z = min(self.twist.angular.z, 1.5)
                    else:
                        self.twist.angular.z = max(self.twist.angular.z, -1.5)

                    
                    prev_th = curr_th
                    self.cmd_publisher.publish(self.twist)

                    rospy.sleep(1)
                    total_distance += distance
                    prev_distance = distance

if __name__ == "__main__":
    controller = Controller()
    controller.run()