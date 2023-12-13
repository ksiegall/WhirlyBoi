
import time
import select
import sys
from machine import Pin, PWM
from encoded_motor import EncodedMotor
from board import Board
from encoded_motor import EncodedMotor
from pid import PID

board = Board.get_default_board()
motor_one = EncodedMotor.get_default_encoded_motor(1)
motor_two = EncodedMotor.get_default_encoded_motor(2)
motor_three = EncodedMotor.get_default_encoded_motor(3)
motor_four = EncodedMotor.get_default_encoded_motor(4)

motors = [motor_one, motor_two, motor_three, motor_four]

for motor in motors:
    motor.set_speed(0)

# Default speed of the motors per pico
defaultSpeedPerMotor = [[135, 140, 150, 165],
                        [185, 180, 220, 240],
                        [135, 135, 160, 150]]

thisPico = 0 # This is the index of the pico that this script is running on

def startup_sequence():
    startup_time = 5
    for motor in motors:
            # Start each progressively with a 1 second delay
            print(f"Motor {motor.index} speed: {(1/2)*defaultSpeedPerMotor[thisPico][motor.index]}")
            motor.set_speed((1/2)*defaultSpeedPerMotor[thisPico][motor.index])
            time.sleep(1)
    for i in range(1,startup_time):
        # take variable seconds to start up
        for motor in motors:
            print(f"Motor {motor.index} speed: {((startup_time+i)/(2*startup_time))*defaultSpeedPerMotor[thisPico][motor.index]}")
            motor.set_speed(((startup_time+i+1)/(2*startup_time))*defaultSpeedPerMotor[thisPico][motor.index])
        time.sleep(1)

# Dictionary of notes and their corresponding motor, pico and speed
noteDictionary = {

    # Fundamentals

    60: (0, 0, 100), # Pico 0, Motor One (index 0), 230 rpm
    61: (0, 1, 100), # Pico 0, Motor Two (index 1), 230 rpm
    62: (0, 2, 105), # Pico 0, Motor Three (index 2), 230 rpm
    63: (0, 3, 115), # Pico 0, Motor Four (index 3), 230 rpm

    64: (1, 0, 130), # Pico 1, Motor One (index 0), 230 rpm
    65: (1, 1, 150), # Pico 1, Motor Two (index 1), 230 rpm
    66: (1, 2, 160), # Pico 1, Motor Three (index 2), 230 rpm
    67: (1, 3, 170), # Pico 1, Motor Four (index 3), 230 rpm

    68: (2, 0, 185), # Pico 2, Motor One (index 0), 230 rpm
    69: (2, 1, 195), # Pico 2, Motor Two (index 1), 230 rpm
    70: (2, 2, 230), # Pico 2, Motor Three (index 2), 230 rpm
    71: (2, 3, 240), # Pico 2, Motor Four (index 3), 230 rpm
    
    # First Harmonics

    72: (0, 0, 170), # Pico 0, Motor One (index 0), 460 rpm
    73: (0, 1, 180), # Pico 0, Motor Two (index 1), 460 rpm
    74: (0, 2, 210), # Pico 0, Motor Three (index 2), 460 rpm
    75: (0, 3, 220), # Pico 0, Motor Four (index 3), 460 rpm

    76: (1, 0, 235), # Pico 1, Motor One (index 0), 460 rpm
    77: (1, 1, 250), # Pico 1, Motor Two (index 1), 460 rpm
    78: (1, 2, 265), # Pico 1, Motor Three (index 2), 460 rpm
    79: (1, 3, 290), # Pico 1, Motor Four (index 3), 460 rpm
}

# Create an instance of a polling object 
poll_obj = select.poll()
# Register sys.stdin (standard input) for monitoring read events with priority 1
poll_obj.register(sys.stdin,1)
# Pin object for controlling onboard LED

while True:
    # Check if there is any data available on sys.stdin without blocking
    if poll_obj.poll(0):
        # Read one character from sys.stdin
        ch = sys.stdin.read(2)
        note = ord(ch[0])
        velocity = ord(ch[1])
        if note == 97 or note == 36:
            startup_sequence()
            break

# while True:
#     # Check if there is any data available on sys.stdin without blocking
#     if poll_obj.poll(0):
#         # Read one character from sys.stdin
#         ch = sys.stdin.read(2)
#         note = ord(ch[0])
#         velocity = ord(ch[1])
#         # Toggle the state of the LED
#         # Print a message indicating that the LED has been toggled
#         print (f"Note: {ord(ch[0])} Velocity: {ord(ch[1])}")
        
#         if note == 37:
#             for motor in motors:
#                 motor.set_speed(0)

#         # If the character is a valid note
#         if note in noteDictionary.keys():
#             noteData = noteDictionary[note]
#             # If the note can be played on this pico
#             if noteData[0] == thisPico:
#                 # If the velocity is 0, stop the note by setting a default speed
#                 if velocity == 0:
#                     motors[noteData[1]].set_speed(defaultSpeedPerMotor[thisPico][noteData[1]])
#                 else:
#                     # Set the speed of the motor based on the dictionary
#                     motors[noteData[1]].set_speed(noteData[2])
#     # # Small delay to avoid high CPU usage in the loop
#     time.sleep(0.005)

while True:
    usr_input = input()
    
    usr_input = usr_input.split(" ")
    if len(usr_input) == 1:
         print(f"Motor {usr_input[0]}: Speed (rpm) - {motors[int(usr_input[0])].get_speed()}, Target Speed (enc/20ms) - {motors[int(usr_input[0])].target_speed}. Speed (enc/20ms) {motors[int(usr_input[0])].speed}")
    elif len(usr_input) == 2:
        motors[int(usr_input[0])].set_speed(int(usr_input[1]))
    elif len(usr_input) == 3:
        motors[int(usr_input[0])].set_speed_controller(PID(kp=float(usr_input[1]), ki=float(usr_input[2])))