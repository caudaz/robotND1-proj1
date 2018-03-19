import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:

    # Check for Rover.mode status
        if Rover.mode == 'forward': 
            # Enough navigable terrain pixels
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # Velocity is below max
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: 
                    # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steer average angle (clipped)
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            # Not enough navigable terrain pixels => 'stop' mode and hit brakes
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'
        # If in "stop" mode
        elif Rover.mode == 'stop':
            # Still moving => keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # Not moving (vel < 0.2)
            elif Rover.vel <= 0.2:
                # Turn to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -15 # Could be more clever here about which way to turn
                # If there is sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                    Rover.mode = 'forward'
                    
################ UNCOMMENT THE FOLLOWING BLOCK TO ENABLE ROCK PICKUP #########  

#        elif Rover.picking_up == 1:
#            Rover.brake = Rover.brake_set
#            Rover.throttle = 0
#            Rover.steer = 0
#            Rover.mode = 'stop'
#            print('Rover.picking_up == 1')
#
#        elif Rover.near_sample == 1:
#            Rover.brake = Rover.brake_set
#            Rover.steer = 0
#            Rover.mode = 'stop'
#            # 
#            Rover.send_pickup = True
#            Rover.samples_located += 1
#            print('Rover.near_sample == 1')
#
#        elif Rover.mode == 'rock_visible':
#            Rover.brake = 0
#            # set max throttle
#            if Rover.vel < Rover.max_vel:
#                Rover.throttle = Rover.throttle_set
#            # coast 
#            else:
#                Rover.throttle = 0
#            Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
#            print(Rover.mode == 'rock_visible')
            
#################################################

    # Just to make the rover do something even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover
