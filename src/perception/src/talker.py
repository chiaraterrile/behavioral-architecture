#!/usr/bin/env python
# license removed for brevity
import rospy
import random
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('command', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    #the publisher sends every time to the topic /command random coordinates
    x = random.randint(0,10)
    y =random.randint(0,10)
    command = "x= "+str(x)+" y= "+str(y)
    rospy.loginfo(command)
    pub.publish(command)
       
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
