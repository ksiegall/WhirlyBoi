import time
import select
import sys
from machine import Pin, PWM
from encoded_motor import EncodedMotor
from pid import PID

motor_one = EncodedMotor.get_default_encoded_motor(1)
motor_two = EncodedMotor.get_default_encoded_motor(2)
motor_three = EncodedMotor.get_default_encoded_motor(3)
motor_four = EncodedMotor.get_default_encoded_motor(4)

motors = [motor_one, motor_two, motor_three, motor_four]

# Stop all motors at the start of the program
for motor in motors:
    motor.set_speed(0)


# Default speed of the motors per pico
defaultSpeedPerMotor = [[150, 160, 150, 165], # pico 0
                        [185, 180, 260, 240], # pico 1
                        [135, 135, 160, 150]] # pico 2


def startup_sequence(thisPico):
    startup_time = 3

    # Set the speed of each motor to half of the default speed
    for motor in motors:
        print(f"Motor {motor.index} speed: {(1/2)*defaultSpeedPerMotor[thisPico][motor.index]}")
        motor.set_speed((1/2)*defaultSpeedPerMotor[thisPico][motor.index])
        time.sleep(1)
    
    # Increase the speed of each motor progressively with a 1 second delay
    for i in range(1, startup_time):
        for motor in motors:
            print(f"Motor {motor.index} speed: {((startup_time+i)/(2*startup_time))*defaultSpeedPerMotor[thisPico][motor.index]}")
            motor.set_speed(((startup_time+i+1)/(2*startup_time))*defaultSpeedPerMotor[thisPico][motor.index])
        time.sleep(1)


# Dictionary of notes and their corresponding motor, pico and speed
noteDictionary = {
    # Fundamentals

    63: (0, 3, 115), # Pico 0, Motor Four (index 3), Note D#4

    64: (1, 0, 135), # Pico 1, Motor One (index 0), Note E4
    65: (1, 1, 170), # Pico 1, Motor Two (index 1), Note F4
    66: (1, 2, 165), # Pico 1, Motor Three (index 2), Note F#4
    67: (1, 3, 175), # Pico 1, Motor Four (index 3), Note G4

    68: (2, 0, 185), # Pico 2, Motor One (index 0), Note G#4
    69: (2, 1, 195), # Pico 2, Motor Two (index 1), Note A4
    70: (2, 2, 230), # Pico 2, Motor Three (index 2), Note A#4
    71: (2, 3, 240), # Pico 2, Motor Four (index 3), Note B4

    72: (0, 0, 300), # Pico 0, Motor One (index 0), Note C5
    73: (0, 1, 320), # Pico 0, Motor Two (index 1), Note C#5
    74: (0, 2, 350), # Pico 0, Motor Three (index 2), Note D5

    # First Harmonics

    75: (0, 3, 220), # Pico 0, Motor Four (index 3), Note D#5

    76: (1, 0, 235), # Pico 1, Motor One (index 0), Note E5
    77: (1, 1, 250), # Pico 1, Motor Two (index 1), Note F5
    78: (1, 2, 285), # Pico 1, Motor Three (index 2), Note F#5
    79: (1, 3, 290), # Pico 1, Motor Four (index 3), Note G5

    # 80: (2, 0, 300), # Pico 2, Motor One (index 0), Note G#5
}


def midiInput():
    # Create an instance of a polling object 
    poll_obj = select.poll()
    # Register sys.stdin (standard input) for monitoring read events with priority 1
    poll_obj.register(sys.stdin,1)
    # Pin object for controlling onboard LED

    # Read the index of the pico from the config file
    with open('config.txt') as f:
        thisPico = int(f.read())
    
    while True:
        # Check if there is any data available on sys.stdin without blocking
        if poll_obj.poll(0):
            ch = sys.stdin.read(2)
            note = ord(ch[0])
            velocity = ord(ch[1])

            # Print a message indicating that the LED has been toggled
            print (f"Note: {ord(ch[0])} Velocity: {ord(ch[1])}")
            
            if note == 97 or note == 36:
                # run startup_sequence at the end of the start note
                if velocity == 0:
                    startup_sequence(thisPico)
            elif note == 38:
                # Stop all motors at the start of the kill note
                if velocity != 0:
                    for motor in motors:
                        motor.set_speed(0)
            elif note in noteDictionary.keys():
                noteData = noteDictionary[note] # noteData is in the form (pico, motor, speed)

                # If the note can't be played on this pico, continue
                if noteData[0] != thisPico:
                    continue
                
                # If the velocity is 0, stop the note by setting a default speed
                if velocity == 0:
                    motors[noteData[1]].set_speed(defaultSpeedPerMotor[thisPico][noteData[1]])
                else:
                    # Set the speed of the motor based on the dictionary
                    motors[noteData[1]].set_speed(noteData[2])
        
        # Small delay to avoid high CPU usage in the loop
        time.sleep(0.005)


def manualInput():
    while True:
        usr_input = input()
        
        usr_input = usr_input.split(" ")
        if len(usr_input) == 1:
             print(f"Motor {usr_input[0]}: Speed (rpm) - {motors[int(usr_input[0])].get_speed()}, Target Speed (enc/20ms) - {motors[int(usr_input[0])].target_speed}. Speed (enc/20ms) {motors[int(usr_input[0])].speed}")
        elif len(usr_input) == 2:
            motors[int(usr_input[0])].set_speed(int(usr_input[1]))
        elif len(usr_input) == 3:
            motors[int(usr_input[0])].set_speed_controller(PID(kp=float(usr_input[1]), ki=float(usr_input[2])))


# midiInput()
manualInput()
