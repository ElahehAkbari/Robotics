#!/usr/bin/python3
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
import rospy, tf
from nav_msgs.msg import Odometry
from sen_one.msg import dist

class Lidar_rotate():
    def __init__(self) -> None:
        rospy.init_node("rotate_robot", anonymous=False)
        self.linear_speed = 0.4
        self.angular_speed = 0.5
        self.cmd_publisher = rospy.Publisher('/cmd_vel' , Twist , queue_size=10)
       
    def rotate(self, angle):
        stop_twist = Twist()
        stop_twist.angular.z = 0.0
        stop_twist.linear.x = 0.0
        self.cmd_publisher.publish(stop_twist)
        rospy.sleep(1)

        msg = rospy.wait_for_message("/odom" , Odometry) 
        orientation = msg.pose.pose.orientation
        roll,pitch, prev_angle = tf.transformations.euler_from_quaternion((orientation.x ,orientation.y ,orientation.z ,orientation.w))
        g_angle = prev_angle + angle


        twist = Twist()
        twist.angular.z = self.angular_speed
        self.cmd_publisher.publish(twist)
        curr_angle = prev_angle    

        while g_angle >= abs(prev_angle - curr_angle):
            msg = rospy.wait_for_message("/odom" , Odometry)
            orientation = msg.pose.pose.orientation
            roll, pitch, temp_angle = tf.transformations.euler_from_quaternion((orientation.x ,orientation.y ,orientation.z ,orientation.w))
            if temp_angle < 0:
                curr_angle = temp_angle
            else :
                curr_angle = curr_angle - (abs(abs(temp_angle) - abs(curr_angle)))

        self.cmd_publisher.publish(stop_twist)
        rospy.sleep(1)

    def set_twist(self, s):
        twist = Twist()
        twist.angular.z = 0.0
        twist.linear.x = s
        self.cmd_publisher.publish(twist)
    
    def get_angle(self):
        data = rospy.wait_for_message("/scan", LaserScan)
        rot_angle = data.ranges.index(min(data.ranges))//4
        return rot_angle
    

    def get_heading():
        msg = rospy.wait_for_message("/odom" , Odometry)
            
        orientation = msg.pose.pose.orientation
        roll, pitch, yaw = tf.transformations.euler_from_quaternion((
            orientation.x ,orientation.y ,orientation.z ,orientation.w
        )) 
            
        return  yaw  

    def run(self):
        while not rospy.is_shutdown():
            obs = rospy.wait_for_message("/ClosestObstacle", dist)
            if obs.distance < 1.5 :
                self.rotate(np.deg2rad(self.get_angle()))
                while True :
                    self.set_twist(0.5)
                    if obs.distance > 1.5:
                        break
            else :
                self.set_twist(0.5)

if __name__ == '__main__':
    lr = Lidar_rotate()
    lr.run()