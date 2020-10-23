#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random

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

def user_action():
   return random.choice(['sleep','normal','play'])
    
    

        

# define state RandomlyGoing
class RandomlyGoing(smach.State):
    def __init__(self):
        # initialisation function, it should not wait
        smach.State.__init__(self, 
                             outcomes=['sleep','normal','play'],
                             input_keys=['randomlygoing_counter_in'],
                             output_keys=['randomlygoing_counter_out'])
        
    def execute(self, userdata):
        # function called when exiting from the node, it can be blacking
        time.sleep(5)
        rospy.loginfo('Executing state RANDOMLYGOING (users = %f)'%userdata.randomlygoing_counter_in)
        userdata.randomlygoing_counter_out = userdata.randomlygoing_counter_in + 1
        return user_action()
    

# define state Sleeping
class Sleeping(smach.State):
    def __init__(self):
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
                rospy.loginfo('Executing state SLEEPING (users = %f)'%userdata.sleeping_counter_in)
                userdata.sleeping_counter_out = userdata.sleeping_counter_in + 1
                return user_action()
            self.sensor_input += 1
            self.rate.sleep

# define state Playing
class Playing(smach.State):
    def __init__(self):
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
                rospy.loginfo('Executing state PLAYING (users = %f)'%userdata.playing_counter_in)
                userdata.playing_counter_out = userdata.playing_counter_in + 1
                return user_action()
            self.sensor_input += 1
            self.rate.sleep

        
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
    main()
