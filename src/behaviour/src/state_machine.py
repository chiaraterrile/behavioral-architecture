#!/usr/bin/env python

import roslib
import random
import rospy
import smach
import smach_ros
import time
import random
from std_msgs.msg import String

# INSTALLATION
# - create ROS package in your workspace:
#          $ catkin_create_pkg smach_tutorial std_msgs rospy
# - move this file to the 'smach_tutorial/scr' folder and give running permissions to it with
#          $ chmod +x state_machine.py
# - run the 'roscore' and then you can run the state machine with
#          $ rosrun smach_tutorial state_machine.py
# - install the visualiser using
#          $ sudo apt-get install ros-kinetic-smach-viewer
# - run the visualiser with
#          $ sudo apt-get install ros-kinetic-smach-viewer

flag_play = 0
flag_normal = 0
message = " "
home = "x=0.0 y=0.0"
person = "x=5.0 y=5.0"
x = random.randint(0,10)
y =random.randint(0,10)
random_coordinates = "x= "+str(x)+" y= "+str(y)


    
def callback(data):
   	 	rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
		global flag_play
		global falg_normal
		global message
		message = data.data
		if message == "none" :
			flag_play = 0
			flag_normal = 1
		else :
			flag_play = 1
		
		#flag_normal = 1
    
#def listener():
		

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    		#rospy.init_node('listener', anonymous=True)
		#rospy.Subscriber("command", String, callback)
		
		
    # spin() simply keeps python from exiting until this node is stopped
    		#rospy.spin()
def user_action():
			
			global flag_play
			global flag_normal 
			global message
                        rospy.Subscriber("command", String, callback)
		        if flag_play == 1 :
				flag_play = 0
				#pub = rospy.Publisher('target', String, queue_size=10)
    				#target = message
    				#rospy.loginfo(target)
   				#pub.publish(target)
				return('play')
			else : #flag_normal == 1 :
			
    				return random.choice(['sleep','normal'])
					#i = i+1
				#return ('normal')
				#flag_normal = 0
				#print (flag_normal)
				
				


        

# define state RandomlyGoing
class RandomlyGoing(smach.State):
    def __init__(self):
	global flag_play
	global message
	global random_coordinates
        # initialisation function, it should not wait
        smach.State.__init__(self, 
                             outcomes=['sleep','normal','play'],
                             input_keys=['randomlygoing_counter_in'],
                             output_keys=['randomlygoing_counter_out'])
        
    def execute(self, userdata):
        # function called when exiting from the node, it can be blacking
        time.sleep(5)
	pub = rospy.Publisher('target', String, queue_size=10)
    	target = random_coordinates
    	rospy.loginfo(target)
   	pub.publish(target)
        rospy.loginfo('Executing state RANDOMLYGOING (users = %f)'%userdata.randomlygoing_counter_in)
        userdata.randomlygoing_counter_out = userdata.randomlygoing_counter_in + 1
        return user_action()
    

# define state Sleeping
class Sleeping(smach.State):
    def __init__(self):
	global flag_play
	global message
	global home
        smach.State.__init__(self, 
                             outcomes=['normal','sleep','play'],
                             input_keys=['sleeping_counter_in'],
                             output_keys=['sleeping_counter_out'])
        self.sensor_input = 0
        self.rate = rospy.Rate(200)  # Loop at 200 Hz

    def execute(self, userdata):
        # simulate that we have to get 5 data samples to compute the outcome
        while not rospy.is_shutdown():  
            time.sleep(1)
            if self.sensor_input < 5: 
		pub = rospy.Publisher('target', String, queue_size=10)
    		target = home
    		rospy.loginfo(target)
   		pub.publish(target)
                rospy.loginfo('Executing state SLEEPING (users = %f)'%userdata.sleeping_counter_in)
                userdata.sleeping_counter_out = userdata.sleeping_counter_in + 1
                return user_action()
            self.sensor_input += 1
            self.rate.sleep

# define state Playing
class Playing(smach.State):
    def __init__(self):
	global flag_play
	global message
	global person
        smach.State.__init__(self, 
                             outcomes=['normal','sleep','play'],
                             input_keys=['playing_counter_in'],
                             output_keys=['playing_counter_out'])
        self.sensor_input = 0
        self.rate = rospy.Rate(200)  # Loop at 200 Hz

    def execute(self, userdata):
        # simulate that we have to get 5 data samples to compute the outcome
        while not rospy.is_shutdown():  
            time.sleep(1)
            if self.sensor_input < 5: 
		pub = rospy.Publisher('target', String, queue_size=10)
		target = person
		rospy.loginfo(target)
   		pub.publish(target)
    		target = message
    		rospy.loginfo(target)
   		pub.publish(target)
                rospy.loginfo('Executing state PLAYING (users = %f)'%userdata.playing_counter_in)
                userdata.playing_counter_out = userdata.playing_counter_in + 1
                return user_action()
            self.sensor_input += 1
            self.rate.sleep

#if __name__ == '__main__':
	#state_machine()
        
def main():
    #listener()
  
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['container_interface'])
    sm.userdata.sm_counter = 0

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('RANDOMLYGOING', RandomlyGoing(), 
                               transitions={'normal':'RANDOMLYGOING', 
                                            'sleep':'SLEEPING',
					    'play':'PLAYING'},
                               remapping={'randomlygoing_counter_in':'sm_counter', 
                                          'randomlygoing_counter_out':'sm_counter'})
        smach.StateMachine.add('SLEEPING', Sleeping(), 
                               transitions={'normal':'RANDOMLYGOING', 
                                            'sleep':'SLEEPING',
					    'play':'PLAYING'},
                               remapping={'sleeping_counter_in':'sm_counter',
                                          'sleeping_counter_out':'sm_counter'})
        smach.StateMachine.add('PLAYING', Playing(), 
                               transitions={'normal':'RANDOMLYGOING', 
                                            'sleep':'SLEEPING',
					    'play':'PLAYING'},
                               remapping={'playing_counter_in':'sm_counter',
                                          'plying_counter_out':'sm_counter'})


    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    
    # Execute the state machine
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()
    
    
    

if __name__ == '__main__':
	#state_machine()
        main()

