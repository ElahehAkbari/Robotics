#!/usr/bin/python3

import rospy
from rand_stu.msg import Student
    
        
def callback(data):  
    if (data.departement == 'Software'):
       pub = rospy.Publisher('software', Student, queue_size=10)
       pub.publish(data)
    else:
       pub = rospy.Publisher('hardware', Student, queue_size=10)
       pub.publish(data)
        
      
def listener():
    rospy.init_node('splitter', anonymous=True)

    rospy.Subscriber("std_request", Student, callback)

    rospy.spin()
    
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInitException:
        pass

       
