#!/usr/bin/python3

import rospy
import tf
from sen_one.msg import dist
from nav_msgs.msg import Odometry
from math import radians, sqrt

# heading of the robot 
def get_heading():
        
    # waiting for the most recent message from topic /odom
    msg = rospy.wait_for_message("/odom" , Odometry)
        
    orientation = msg.pose.pose.orientation
        
    # convert quaternion to odom
    roll, pitch, yaw = tf.transformations.euler_from_quaternion((
        orientation.x ,orientation.y ,orientation.z ,orientation.w
    )) 
        
    return  msg.pose.pose.position    

def talker():
    student = dist()
    
    pub = rospy.Publisher('ClosestObstacle', dist, queue_size=10)
    rospy.init_node('closest_obstacle', anonymous=True)
    rate = rospy.Rate(1)
    
    while not rospy.is_shutdown():
        current_pose = get_heading()
        x = current_pose.x
        y = current_pose.y

        distance = {}

        distance["bookshelf"] = cal_distance(x,y,2.64,-1.55)

        distance["dumpster"] = cal_distance(x,y,1.23,-4.57)

        distance["barrel"] = cal_distance(x,y,-2.51,-3.08)

        distance["postbox"] = cal_distance(x,y,-4.47,-0.57)
        
        distance["brick_box"] = cal_distance(x,y,-3.44,2.75)

        distance["cabinet"] = cal_distance(x,y,-0.45,4.05)

        distance["cafe_table"] = cal_distance(x,y,1.91,3.37)

        distance["fountain"] = cal_distance(x,y,4.08,1.14)

        closest_dist = min(distance.values())
        obstacle_name = list(distance.keys())[list(distance.values()).index(closest_dist)]

        obstacle = dist()
        obstacle.obstacle_name = obstacle_name
        obstacle.distance = closest_dist

        rospy.loginfo('Info: obstacle: {} | distance: {}'.format(obstacle_name, closest_dist))
        pub.publish(obstacle)
        rate.sleep()

def cal_distance(x1,y1,x2,y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass