
Assignment 1
=========================

### Exercise Objectives ###

The robot shuld move through the maze by avoiding gold tokens. If the robot comes across a silver token, it has to grab it and move it behind itself.

### Chosen approach to complete objectives ### 

The main idea behind this solution is that the robot should keep driving straight until it gets 
too close to a block. When it does get too close, the robot can then decide what to do depending 
on which kind of block is closest and where it is positioned with respect to the robot. The 
robot is also programmed to complete the course in an anti-clockwise manner and to keep running 
until a keyboard interrupt is issued from the terminal.

All of the robot's sensor readings and consequent decisions get printed in a log file that gets
named with the date and time of when the program was started. Only key decisions and the current 
heading the robot has to avoid are printed on the terminal. 

### Pseudo-code for the solution that has been implemented ###

	create file name for log
	create and open the log file
	define master_speed

	while(forever):

		turn on both motors, speed set to master_speed

		while(both blocks are far enough):
			keep motors running for 3ms

		brake both motors

		if(silver token is closer):

			if(closest silver is in front of the robot):

				allign with token

				get within grabing distance

				try to grab it

					if succesful: start grab routine

					if not: note it in the log file


			else if(closest silver is at the back of the robot):

				if (there are no gold blocks directly in front of the bot):

					drive straight for 0.1s

				else if(the silver block is right behind the robot):

					push the silver block back 0.1m and go back to starting position

				else if(the silver block is behind the bot but to the sides):

					move forward 0.1m

		else if(gold token is closer):

			if(the closest gold token is in front of the robot):

				if (it's to the left):
					turn on the spot to the right

				else if (it's to the right):
					turn on the spot to the left

				check_and_correct_heading()

				if (the gold block is straight ahead and closer than 0.5m):

					backup until closest gold block is 1m away
					if(last decision was turning right):
						turn left of the initial heading
					if (last decision was to turn left):
						turn right of the initial heeading


				if (the robot is still far enough from the closest gold block):

					drive straight for 0.1s

			else if(the closest gold token is not in front of the robot):

				drive straight for 0.1s

				if(the current heading is pointing the robot to an acceptable 
				direction ):

					reset a counter so that the current heading can be saved later



	end of main while loop

Custom functions developed to implement this code 
----------------------------------------------------------

### Complete list of new functions added ###

* in_range() \n
* angle_correction()
* motors_on()
* brake()
* compass()
* dist_silver()
* a_dist_silver()
* dist_golden()
* a_dist_golden()
* P_control_angle()
* P_control_distance()
* check_and_correct_heading()


### Brief functionality and usage overview ###


* in_range(variable,minimum acceptable value, maximum acceptable value)
	
Is used just to have a more readable code, takes a float variable and checks if its value is in 
the range of two other values 


angle_correction(computed heading)
	
	headings can vary between [0+ , 180] and [0-,-180] so whenever new headings are 
	computed, the resulting values have to be within these ranges. If the computed vaule is 
	not in these ranges, the function converts it by adding +360 or -360 according to the 
	sign of the computed value 
	

* motors_on(speed)
	
Simply assigns the value passed as speed to both motors


* brake()

Sets both motor speeds to zero


* compass()
	
Converts the R.heading value from radians to degrees


* dist_silver()

Scans through all visible tokens and returns the distance of the closest silver token
spotted
	

* a_dist_silver()

Scans through all visible tokens and returns the relative angle (to the robot's 
orientation) of the closest silver token spotted
	

* dist_golden()

Scans through all visible tokens and returns the distance of the closest golden token
spotted
	

* a_dist_golden()

Scans through all visible tokens and returns the relative angle (to the robot's 
orientation) of the closest golden token spotted
	

* P_control_angle(new heading, precision of the maneuver, proportional constant, use specifier)

This function is used to either get the robot to turn for a specified number of 
degrees or to get it to point to a specific heading on the map, depending on what string
is passed to the last argument. It's a proportional controller that regulates the speed
that motors need to go at to close in on the requested heading.

The "precision" argument passes the accepted margin of error from the requested value. 
The higher this value gets and the quicker, but less precise will be the maneuver.

The proportinal constant is usually equal to 1 because overshooting the target value 
would be problematic for headings close to 180 (or -180). 

	
* P_control_distance()

Ths function is used to move the robot forwards or backwards of a precise amount. The 
arguments are structured like in P_control_angle(). Since there are no discontinuous 
intervals like in the case of P_control_angle(), the proportionality constant can be 
fairly high.
	

* check_and_correct_heading()
  
Checks if the last turning maneuver didn't turn the robot too far back
go back to the last heading that was saved before the robot started 
turning. Move to the left or to the right of that heading depending on
what direction the robot decided to take last.

Future Improvements
-------------------------------------
The current version of the command script for the simuated robot has some difficulties in traversing tight long 'hallways' (such as the top-most level of the 
arena). This behaviour can be greatly limited by changing the angle sector definition for the "front" of the robot from [-90,90] to [-80,80]. This does however 
partially blind the robot, thus reducing the reaction distance necessary for the robot to react in a timely manner to obstacles. This issue can be mitigated by 
fine-tuning the various maneuvering parameters in the code.

Another possible solution was considered before continuing development on this version, but it appeared to be too heavy to run on some machines. The main idea of 
this alternative solution is to have the robot go straight until the closest object appears directly in front of itself. The robot would then scan eclusively its 
left and right sies and decide to turn away from the side that returned the shortest distance. This solution wouldn't need the robot to constantly check what 
heading it has to avoid to prevent itself from going through the circuit the wrong way around, and would more easily help the robot keep the right distance from 
tokens. Development was stopped however on this approach to the solution because it appears that either for a lack of computing power or because of some issues 
with the installation of all the libraries on this current setup, the simulated environment can't react fat enough to the commands of the robot's navigation 
algorythhm. So after setting everything up in a better working machine, this alternative solution with a slightly 'heavier' program could be developed into a more 
efficient and stable solution for this exercise.



	
Running the Simulator
------------------------------------

This python script is written to control a robot inside a simulator developed by [Student Robotics](https://studentrobotics.org). The 'arena' where the robot is 
supposed to be tested was developed separately for this coding excercise. The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) 
library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

The folder shared in this repository contains all the necessary scripts to run the robot in its simulated environment. 
To launch the program move to this folder from terminal and launch both the script run.py and ASSIGNMENT1.py with a python2 command.

The sub-folder past_logs contains the log files of previous runs made by the robot. New log files are currently saved ouside of this sub_folder, directly into the 
main one.

Side note:
In the script sim_robot.py, found in sub-folder sr/robot, the MAX_Motor_SPEED value has been raised to 300. 







Key features of the Python Robotics Simulator
------------------------------------------------------------
Presented below are some of the key features of the Robot() class used in ASSIGNMENT1.py, and some brief explanations on how the robot is expected to move inside 
and sense its environment.



 ### Motors ### 


The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The 
left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by 
serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ### 


The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a 
token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an 
`AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot 
can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
        
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/
