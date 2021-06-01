#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String

def callback(data):
    #the subscriber waits some time and then print the new position of the robot and keeps waiting for new      targets
    time.sleep(5)
    rospy.loginfo(rospy.get_caller_id() + " the actual position is : %s", data.data)
    
def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("target", String, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
