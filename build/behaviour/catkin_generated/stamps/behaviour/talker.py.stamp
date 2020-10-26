#!/usr/bin/env python
# license removed for brevity
import rospy
import random
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('command', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    #rate = rospy.Rate(10) # 10hz
    #while not rospy.is_shutdown():
    #command = "x=2.0 y=2.0"#%s"# % rospy.get_time()
   # command1 = "none"
    x = random.randint(0,10)
    y =random.randint(0,10)
    #command2 = "x= "+str(x)+" y= "+str(y)
    #command = random.choice([command1,command2])
    command = "x= "+str(x)+" y= "+str(y)
    rospy.loginfo(command)
    pub.publish(command)
        #rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
