from __future__ import print_function

import time
import math
from datetime import datetime
from sr.robot import *

a_th = 0.1
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()

#naming log file with the date and time at which the simulation was started
current_date_and_time = datetime.now()
current_date_and_time_string = str(current_date_and_time)
extension = ".txt"
file_name = current_date_and_time_string + extension
#creating and opening the log file
log = open(file_name, 'w')

def in_range(variable,minimum,maximum):
    
    if minimum<=variable<=maximum :

        return 1
    else:
        return 0

def angle_correction(angle):
    log.write("   elaborating angle:")
    log.write("   requested angle= "+str(angle)+"\n")

    if -180>angle>=-360:
        angle=angle+360
        log.write("   corrected to: "+str(angle)+"\n")
    elif 180<angle<=360:
        angle=angle-360
        log.write("   corrected to: "+str(angle)+"\n")
    else:
        log.write("   no correction applied\n")

    return angle


def drive(speed, seconds):
    
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
   
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def dist_golden():     
    dist=100

    for token in R.see():    
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist

    if dist==100:

        return -1, -1
    else:
        return dist


def dist_silver():     
    dist=100

    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER :
            dist=token.dist

    if dist==100:
        return -1, -1
    else:
        return dist

def a_dist_silver():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
            angle=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return angle

def a_dist_golden():
    
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
            angle=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return angle

def compass():
    angle=R.heading*180/math.pi
  
    return angle

def P_control_angle(angle,precision,kp,use):

    log.write("using P_control_angle:\n")
    if use == "relative":
        angle=compass() + angle
        
    
    angle=angle_correction(angle)
    log.write("   I'm aiming for: "+str(angle)+"\n")

    error=1

    while error<=-precision or error >=precision:
        error=angle-compass()    

        speed = error*kp
        R.motors[0].m0.power = speed
        R.motors[0].m1.power = -speed

    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    log.write("   I arrived at: "+str(compass())+"\n")    
    
    return 1
        
def P_control_distance(distance,precision,kp):
    log.write("using P_control_distance:\n")
    error=1
    x_initial,y_initial = R.location

    while error<=-precision or error >=precision:
        x,y = R.location
        distance_travelled= math.sqrt((x-x_initial)**2+(y-y_initial)**2)
        
        if distance>0:
            error=distance-distance_travelled
        elif distance<0:
            error=distance+distance_travelled
        speed = error*kp
        R.motors[0].m0.power = speed
        R.motors[0].m1.power = speed

    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    log.write("   I've moved: "+str(distance_travelled)+"m\n")

    return 1

def check_and_correct_heading(initial_heading,avoid,last_decision):
    log.write("checking if I haven't turned too far:\n")
    if abs(angle_correction(compass()-avoid))<70:

        #check if the last maneuver hasn't taken the bot too far to the left

        print("I'm too close to this heading"+str(avoid))
        log.write("I'm too close to this heading"+str(avoid)+"\n")
        if last_decision=="left":
            P_control_angle(initial_heading-45,0.1,1,"absolute")
        elif last_decision=="right":
            P_control_angle(initial_heading+45,0.1,1,"absolute")
        
        P_control_distance(-(0.8-dist_golden()),0.01,90)
    else:
        log.write("   I haven't\n")


    return 1

def motors_on(speed):
    R.motors[0].m0.power=speed
    R.motors[0].m1.power=speed

def brake():
    R.motors[0].m0.power=0
    R.motors[0].m1.power=0



def main():


    time.sleep(4) 
    death=0
    golden_counter=0
    master_speed=100
    decision=""
    

    
    while 1:
        
        print("-------------------------------------------------------------------")
        log.write("-------------------------------------------------------------------\n")
        #time.sleep(2.5)
        motors_on(master_speed)
        while (dist_golden()>1 and dist_silver()>0.6):
            time.sleep(0.003)
            golden_counter=0    
        brake()
                    
        log.write("\nI got too close to a block, golden is at: "+str(dist_golden())+"m and silver is at: "+str(dist_silver())+"m\n")
        if dist_golden()>=dist_silver():
            
            print("SILVER is closer")
            log.write("SILVER is closer\n")
            golden_counter=0

            if in_range(a_dist_silver(),-90,90):
                

                log.write("silver in front of me \n")
                P_control_angle(a_dist_silver(),0.001,1,"relative")

                log.write("distance to silver: "+str(dist_silver())+", closing in at 0.35m\n")
                P_control_distance(dist_silver()-0.35,0.01,90)                

                log.write("starting grab routine\n")
                if R.grab()==1 :
                    log.write("grab() succeful\n")
                    time.sleep(0.5)
                    log.write("starting angle "+str(compass()))
                    P_control_angle(-180,0.001,1,"relative")          
                    log.write("stopped at "+str(compass()))
                    R.release()
                    P_control_distance(-0.3,0.01,90)
                    P_control_angle(180,0.001,1,"relative")
                    time.sleep(0.5)
                else:
                    log.write("grab() failed\n")
                
                log.write("back to main loop\n\n")  

            else:

                log.write("silver not in front of me\n")
                if not in_range(a_dist_golden(),-10,10):

                    #silver is closer than the closest golden but not in front of the robot
                    #and the closest golden is not in front of the robot
                    print("Silver token is behind me, I'll go on\n")
                    log.write("Silver token is behind me, I'll go on\n")
                    drive(master_speed,0.1)
                    log.write("back to main loop\n\n")            
                elif in_range(a_dist_silver(),-180,-175) or in_range(a_dist_silver(),175,180) :

                    #silver is closer than golden but right behind the robot
                    #there are also gold blocks on the front sides of the robot
                    #the robot will try to push it back a bit and goback to whereit started the maneuver
                    print("I'll try to get some space by backing up \n and getting closer to a golden token")
                    log.write("I'll try to get some space by backing up \n and getting closer to a golden token\n")
                    backup_distance=dist_silver()+0.1
                    P_control_distance(-backup_distance,0.01,90)
                    P_control_distance(backup_distance,0.01,90)
                    log.write("back to main loop\n\n")
                else:
                    #silver is in any other angle at the back of the robot
                    log.write("careful maneuver to get some distance from silver\n")
                    P_control_distance(0.1,0.01,100)
                    log.write("back to main loop\n\n")
                
            

        else:
            print("GOLDEN is closer")
            log.write("GOLDEN is closer\n")

            if golden_counter==0 :

                #if it's the first ime the robot has to deal with a gold token after having encountered a silver token 
                #or after having driven staight for  while, the robot saves its initial heading and makes sure to 
                #stop its  maneuvers if the new heading it has reached is pointing the robot back from where it came

                initial_heading=compass()
                log.write("saving initial heading: "+str(initial_heading)+"\n")
                avoid=angle_correction(initial_heading+180)
                print(str(avoid))
                max_avoid=angle_correction(avoid+70)
                min_avoid=angle_correction(avoid-70)
                if(min_avoid>max_avoid):
                    #this is here to write  reasonable interval
                    temp=min_avoid
                    min_avoid=max_avoid
                    max_avoid=temp

                log.write("I will avoid going between "+str(min_avoid)+" and "+str(max_avoid)+"\n")
                            
            print(str(avoid))

            golden_counter=golden_counter+1;



            if in_range(a_dist_golden(),-90,90):

                #closest gold token is "in sight" of the bot


                if a_dist_golden()<=0  :



                    #token to the left
                    print("closest gold token is to the left, turning right")
                    log.write("closest gold token is to the left, turning right\n")
                    turn(20,0.1)
                    log.write("current heading: "+str(compass())+" min_avoid: "+str(min_avoid)+" max_avoid: "+str(max_avoid)+"\n")
                    log.write("I can still turn "+str(abs(angle_correction(compass()-avoid)))+" degrees\n")
                    decision="left"
                            
                    
                else:

                    #token to the right
                    print("closest gold token to the right, I'm turning left")
                    log.write("closest gold token to the right, I'm turning left\n")
                    turn(-20,0.1)
                    log.write("current heading: "+str(compass())+" min_avoid: "+str(min_avoid)+" max_avoid: "+str(max_avoid)+"\n")
                    log.write("I can still turn "+str(abs(angle_correction(compass()-avoid)))+"\n")
                    last_decision="right"
                
                check_and_correct_heading(initial_heading,avoid,decision)   

                
                   

                if dist_golden()<=0.5 and in_range(a_dist_golden(),-30,30):

                    #the bot got wound up in a logic loop and is getting too close to the walls 

                    print("[EMERGENCY MANEUVER]")
                    log.write("[EMERGENCY MANEUVER]\n")
                    print("Backing up to 1m from the closest golden block")
                    log.write("Backing up to 1m from the closest golden block")
                    P_control_distance(-(1-dist_golden()),0.01,90)
                    if last_decision=="right":
                        log.write("turning to the left of the initial heading\n")
                        P_control_angle(initial_heading+45,0.1,1,"absolute")
                    elif last_decision=="left":
                        log.write("turning to the right of the initial heading\n")
                        P_control_angle(initial_heading-45,0.1,1,"absolute")
                    log.write("back to main loop\n\n")

                    if dist_golden()>0.5:
                        drive(master_speed,0.01)
                        log.write("back to main loop\n\n")


            else:

                #there's a gold token close by but it's not in the way of the robot
                log.write("The closest gold token is behind me\n")
                log.write("I'm this close to the wrong heading:  "+str(abs(angle_correction(compass()-avoid)))+"\n")
                log.write("current heading is: "+str(compass())+" min_avoid: "+str(min_avoid)+" max_avoid: "+str(max_avoid)+"\n")
                log.write("I'll keep driving straight\n")
                print("driving straight")
                drive(master_speed,0.1)
                if abs(angle_correction(compass()-avoid))>110:
                    golden_counter=0
                log.write("back to main loop\n\n")






 
main()
