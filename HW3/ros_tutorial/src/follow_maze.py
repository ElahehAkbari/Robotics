#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt

class PIDController():


    def __init__(self):
        
        rospy.init_node('ros_tutorial', anonymous=False)
        rospy.on_shutdown(self.on_shutdown)
        
        self.k_i = 0.0001
        self.k_p = 0.4
        self.k_d = 11
        
        self.dt = 0.005
        self.v = 0.1
        self.D = 0.5
        rate = 1/self.dt
        
        self.r = rospy.Rate(rate)
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        self.errs = []

    
    def distance_from_wall(self,a,b):
        laser_data = rospy.wait_for_message("/scan" , LaserScan)
        rng = laser_data.ranges[a:b]
        d = min(rng)
        return d
    
    def follow_wall(self):
        
        d = self.distance_from_wall(5,180)    
        sum_i_theta = 0
        prev_theta_error = 0
        
        move_cmd = Twist()
        move_cmd.angular.z = 0
        move_cmd.linear.x = self.v

        while not rospy.is_shutdown():
            fd = self.distance_from_wall(0,4)

            if fd <= self.D :
                fd = self.distance_from_wall(0,4)
                twist = Twist()
                twist.angular.z = -0.093
                self.cmd_vel.publish(twist)
            
            else:
                self.cmd_vel.publish(move_cmd)

                err = d - self.D
                self.errs.append(err)
                sum_i_theta += err * self.dt
                
                P = self.k_p * err
                I = self.k_i * sum_i_theta
                D = self.k_d * (err - prev_theta_error)

                rospy.loginfo(f"P : {P} I : {I} D : {D}")
                move_cmd.angular.z = P + I + D 
                prev_theta_error = err
                move_cmd.linear.x = self.v            
                
                rospy.loginfo(f"error : {err} speed : {move_cmd.linear.x} theta : {move_cmd.angular.z}")
                
                d = self.distance_from_wall(5,180)
                

                self.r.sleep()

    def on_shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())

        rospy.sleep(1)
            

if __name__ == '__main__':
    try:
        pidc = PIDController()
        pidc.follow_wall()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation terminated.")