#!/usr/bin/python3

import rospy
from rand_stu.msg import Student

def callback(data):
    rospy.loginfo('Software: name: {} {} | age: {} | dept: {}'.format(data.name, data.last_name, data.age, data.departement))
    
def listener():
    rospy.init_node('software', anonymous=True)

    rospy.Subscriber('software', Student, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
