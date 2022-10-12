#!/usr/bin/python3

import rospy
import tf
from math import atan2
from cmath import sqrt

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry


class PIDController():


    def __init__(self):
        
        rospy.init_node('ros_tutorial', anonymous=False)
        rospy.on_shutdown(self.on_shutdown)
    

        self.k_i = 0.08
        self.k_p = 0.6
        self.k_d = 6
        
        self.dt = 0.005
        self.v = 0.06
        self.D = 0.7
        rate = 1/self.dt

        self.goal_x = 3
        self.goal_y = -1

        self.X = 0
        self.Y = 0
        
        self.r = rospy.Rate(rate)
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        self.errs = []

    # heading of the robot 
    def get_heading(self):
        
        # waiting for the most recent message from topic /odom
        msg = rospy.wait_for_message("/odom" , Odometry)
        
        orientation = msg.pose.pose.orientation
        
        # convert quaternion to odom
        roll, pitch, yaw = tf.transformations.euler_from_quaternion((
            orientation.x ,orientation.y ,orientation.z ,orientation.w
        )) 
        
        return yaw   

    def distance_from_wall(self):
        laser_data = rospy.wait_for_message("/scan" , LaserScan)
        rng = laser_data.ranges[10:190]
        d = min(rng)
        return d
    
    def distance_from_front(self):
        laser_data = rospy.wait_for_message("/scan" , LaserScan)
        d = min(min(laser_data.ranges[0:10]),min(laser_data.ranges[350:359]))
        return d


    def distance_from_goal(self):
        msg = rospy.wait_for_message("/odom" , Odometry) 
        self.X = msg.pose.pose.position.x
        self.Y = msg.pose.pose.position.y
        dist = cal_distance(self.X, self.Y, self.goal_x, self.goal_y)
        return dist
    
    def move_to_goal(self): 
        move_cmd = Twist()
        angle = atan2((self.goal_y - self.Y), (self.goal_x - self.X))

        if abs(angle - self.get_heading()) <= 0.2:
            move_cmd.linear.x = self.v
            move_cmd.angular.z = 0.0
        else:
            move_cmd.linear.x = 0.0
            move_cmd.angular.z = 0.3

        self.cmd_vel.publish(move_cmd)

    def decide(self):
        gd = self.distance_from_goal()

        while not rospy.is_shutdown() :
            gd = self.distance_from_goal()
            if gd.real <= 0.35:
                move_cmd = Twist()
                move_cmd.linear.x = 0.0
                move_cmd.angular.z = 0.0
                break
            else:
                fd = self.distance_from_front()
                th = self.D + 0.2
                if self.distance_from_wall() <= th:
                    self.follow_wall()
                else:
                    self.move_to_goal()
                self.r.sleep() 

    def follow_wall(self):
        
        d = self.distance_from_wall()    
        sum_i_theta = 0
        prev_theta_error = 0
            
        move_cmd = Twist()
        move_cmd.angular.z = 0
        move_cmd.linear.x = self.v

        fd = self.distance_from_front()
        th = self.D + 0.1
        if fd <= th:
            fd = self.distance_from_front()
            twist = Twist()
            twist.angular.z = -0.2
            self.cmd_vel.publish(twist)
            
        else:
            self.cmd_vel.publish(move_cmd)
            err = d - self.D
            self.errs.append(err)
            sum_i_theta += err * self.dt
            
            P = self.k_p * err
            I = self.k_i * sum_i_theta
            D = self.k_d * (err - prev_theta_error)

            move_cmd.angular.z = P + I + D 
            prev_theta_error = err
            move_cmd.linear.x = self.v                
             


    def on_shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())

        rospy.sleep(1)

def cal_distance(x1,y1,x2,y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)           

if __name__ == '__main__':
    try:
        pidc = PIDController()
        pidc.decide()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation terminated.")