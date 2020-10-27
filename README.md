# behavioral-architecture
The aim of this project is to send commands to a simulated robot which enters in a certain behaviour according to what it receives. 

SOFTWARE ARCHITECTURE:
The architecture is composed of three components:
 - Perception: which is a ROS node publishing to a topic /command and sends a string of 2D coordinates every time we want to send the command 'play' to the robot
 - Behaviour : which is a ROS node composed of a finite state machine. This state machine subscribe to the topic /command in order to receive the command every time it arrives. The machine can reach three states : 'randomlygoing','sleeping' and 'playing' (which correspond to the commands 'normal','sleep' and 'play'), and when is in a certain state it publishes the position (always represented as a string) to the topic /target
 - Motion Control : which is a ROS node subscribing to the topic /target in order to recive the actual postion of the robot 

PACKAGES and FILES:
Inside the workspace behavioral_architecture there are three packages (one for each component).
Inside perception/src there's the executable talker.py which is the publisher.
Inside behaviour/src there's the executable state_machine.py which is the finite state machine
Inside motion_control there's the executable control.py which is the subscriber that will communicate that the robot has reached the target position.

INSTALLATION and RUNNING PROCEDURE:
To run the procedure it's necessary to follow these steps:
1) catkin_make of the workspace
2) run the motion control with $rosrun motion_control control.py
3) run the state machine with $rosrun behaviour state_machine.py
4) run the talker every time we want to send the command 'play' to the robot with $rosrun perception talker.py

WORKING HYPOTHESIS and ENVIROMENT :
It's assumed that in absence of command (not running the talker) the robot goes in the state 'sleep' where it stays for a certain amount of time remaining in the 'home' postion (x=0.0 y=0.0) and then goes in the state 'normal' in which it reaches a random position.
If we send the command 'play', the robot goes to the 'user' postion ( fixed at x=5.0 y=5.0), then reaches the position inside the command, then again the 'user' postion and at the end comes back to the 'normal' state.
It's assumed that the command 'play' is not a real command, but simply a string of coordinates, that when arrives makes the state changing from 'normal' to 'play'.
In the component Motion Control the subscriber receives immediately the target position, but waits until the transition to the next state to communicate it, simulating the time that would be necessary to the robot to reach a postion. 

SYSTEM'S LIMITATIONS:
In the system the user needs to interact 'manually' with the robot running every time the talker in case he wants to send the command 'play'.
AUTHOR and CONTACT
Chiara Terrile 
chiaraterrile97@gmail.com

