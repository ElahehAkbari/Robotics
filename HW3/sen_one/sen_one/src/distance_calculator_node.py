#!/usr/bin/python3

import rospy
from nav_msgs.msg import Odometry
from math import sqrt
from sen_one.srv import GetDistance, GetDistanceResponse

class Distance_calculator():
    def __init__(self) -> None:
        self.default = -1
        self.obstacles = {}
        self.obstacles["book_shelf"] = (2.64, -1.55)
        self.obstacles["dumpster"] = (1.23, -4.57)
        self.obstacles["barrel"] = (-2.51, -3.08)
        self.obstacles["postbox"] = (-4.47, -0.57)
        self.obstacles["brick_box"] = (-3.44, 2.75)
        self.obstacles["cabinet"] = (-0.45, 4.05)
        self.obstacles["cafe_table"] = (1.91, 3.37)
        self.obstacles["fountain"] = (4.08, 1.14)
    def get_distance(self, req):
        try:
            msg = rospy.wait_for_message("/odom" , Odometry)
            x = msg.pose.pose.position.x
            y = msg.pose.pose.position.y
            distance = cal_distance(x,y,self.obstacles[req.obstacle_name][0],self.obstacles[req.obstacle_name][1])
        except:
            return None
        res = GetDistanceResponse()
        res.distance = distance
        return res  
        
def cal_distance(x1,y1,x2,y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
def listener():
    rospy.init_node('distance_calculator_node', anonymous=True)
    dc = Distance_calculator()
    s = rospy.Service('/get_distance', GetDistance, dc.get_distance)
    rospy.spin()

if __name__ == '__main__':
    listener()