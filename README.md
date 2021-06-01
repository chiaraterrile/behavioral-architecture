# Assignment 1 od ExpRob

### Introduction
The aim of this project is to send commands to a simulated robot which enters in a certain behavioural state according to what it receives. 

### Software Architecture
The architecture is composed of three components:
 - **Perception**: which is a ROS node publishing to a topic _/command_ and sending a string of 2D coordinates every time we want to send the command 'play' to the robot
 - **Behaviour** : which is a ROS node composed of a finite state machine. This state machine subscribes to the topic _/command_ in order to receive the command every time it arrives. 
 The machine can reach three states : **randomlygoing**, **sleeping** and **playing** (which correspond to the commands 'normal','sleep' and 'play'), and when is in a certain state it publishes the position (always represented as a string) to the topic _/target_
 - **Motion Control** : which is a ROS node subscribing to the topic _/target_ in order to recive the actual postion of the robot 

### Packages and files
Inside the directory _behavioral_architecture_ there are three packages (one for each component).

Inside `perception/src` there's the executable _talker.py_ which is the publisher.

Inside `behaviour/src `there's the executable _state_machine.py_ which is the finite state machine.

Inside `motion_control/src` there's the executable _control.py_ which is the subscriber that will communicate that the robot has reached the target position.

### Installation and running procedure
To run the procedure it's necessary to follow these steps:
1) clone this repository into the _src_ directory of a workspace

2) Build the workspace with the following command :
 ```
$ catkin_make
```
3) run the roscore
 ```
$ roscore
```

4) run the motion control with :
 ```
$ rosrun motion_control control.py
```
5) in another terminal run the state machine with :
 ```
 $rosrun behaviour state_machine.py
```

6) in another terminal run the talker every time we want to send the command 'play' to the robot with
 ```
$rosrun perception talker.py

```


### Working hypothesis and enviroment
It's assumed that in absence of command (not running the talker) the robot goes in the state _sleep_ where it stays for a certain amount of time remaining in the home postion (0,0) and then it goes in the state _normal_ in which it reaches a random position.

If we send the command _play_, the robot goes to the user postion ( fixed at x=5.0 y=5.0), then reaches the position inside the command, then again the user postion and at the end comes back to the _normal_ state.

It's assumed that the command 'play' is not a real command, but simply a string of coordinates, that when arrives makes the state changing from _normal_ to _play_.

In the component Motion Control the subscriber receives immediately the target position, but waits until the transition to the next state to communicate it, simulating the time that would be necessary to the robot to reach a postion. 

### System's limitations
In the system the user needs to interact 'manually' with the robot running every time the talker in case he wants to send the command 'play'.


### Author and contact
Terrile Chiara
mail: **chiaraterrile97@gmail.com**
