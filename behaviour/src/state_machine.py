#!/usr/bin/env python

import roslib
import random
import rospy
import smach
import smach_ros
import time
import random
from std_msgs.msg import String


flag_play = 0
message = " "
#fixed position of the user and of the home
home = "x=0.0 y=0.0 (home)"
person = "x=5.0 y=5.0 (user)"


    
def callback(data):
   	 	
		global flag_play
		global message
		message = data.data
		#checking that there's actually a message from the publisher
		if message == " " :
			flag_play = 0
		else :
			flag_play = 1
		

def user_action():
			
			global flag_play 
			global message
                        rospy.Subscriber("command", String, callback)
		        if flag_play == 1 :
				flag_play = 0
				return('play')
			else : 
				return ('sleep')
				


        

# define state RandomlyGoing
class RandomlyGoing(smach.State):
    def __init__(self):
	global flag_play
	global message
	
        smach.State.__init__(self, 
                             outcomes=['sleep','normal','play'],
                             input_keys=['randomlygoing_counter_in'],
                             output_keys=['randomlygoing_counter_out'])
        
    def execute(self, userdata):
	x = random.randint(0,10)
	y =random.randint(0,10)
	random_coordinates = "x= "+str(x)+" y= "+str(y)
        
        #defining the publisher
	pub = rospy.Publisher('target', String, queue_size=10)
    	target = random_coordinates
    	pub.publish(target)

        rospy.loginfo('Executing state RANDOMLYGOING (users = %f)'%userdata.randomlygoing_counter_in)
        userdata.randomlygoing_counter_out = userdata.randomlygoing_counter_in + 1
	time.sleep(10)
        return user_action()
    

# define state Sleeping
class Sleeping(smach.State):
    def __init__(self):
	global flag_play
	global message
	global home
        smach.State.__init__(self, 
			     outcomes=['normal'],
                             input_keys=['sleeping_counter_in'],
                             output_keys=['sleeping_counter_out'])
        
    def execute(self, userdata):
        
	#defining the publisher
	pub = rospy.Publisher('target', String, queue_size=10)
    	target = home
   	pub.publish(target)
	#remains in the sleeping state for a certain amount of time
        time.sleep(15)

        rospy.loginfo('Executing state SLEEPING (users = %f)'%userdata.sleeping_counter_in)
        userdata.sleeping_counter_out = userdata.sleeping_counter_in + 1
	
        #after being in the sleeping state it comes back to normal
        return ('normal')

# define state Playing
class Playing(smach.State):
    def __init__(self):
	global flag_play
	global message
	global person
        smach.State.__init__(self, 
                             outcomes=['normal'],
                             input_keys=['playing_counter_in'],
                             output_keys=['playing_counter_out'])
       

    def execute(self, userdata):
       
        #defining the publisher
   	pub = rospy.Publisher('target', String, queue_size=10)
	target = person
   	pub.publish(target)
	time.sleep(5)
    	target = message
   	pub.publish(target)
	time.sleep(5)
	target = person
   	pub.publish(target)

        rospy.loginfo('Executing state PLAYING (users = %f)'%userdata.playing_counter_in)
        userdata.playing_counter_out = userdata.playing_counter_in + 1
	time.sleep(10)
	#after being in the playing state it comes back to normal
        return ('normal')
        


        
def main():
  
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
                               transitions={'normal':'RANDOMLYGOING' 
                                            
					    },
                               remapping={'sleeping_counter_in':'sm_counter',
                                          'sleeping_counter_out':'sm_counter'})

        smach.StateMachine.add('PLAYING', Playing(), 
                               transitions={'normal':'RANDOMLYGOING'}, 
                                            
							
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

