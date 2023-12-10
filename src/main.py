
# import time
# import select
# import sys
# from machine import Pin, PWM
# from encoded_motor import EncodedMotor
# from board import Board

# board = Board.get_default_board()
# motor_one = EncodedMotor.get_default_encoded_motor(1)

# motor_two = EncodedMotor.get_default_encoded_motor(2)
# motor_three = EncodedMotor.get_default_encoded_motor(3)
# motor_four = EncodedMotor.get_default_encoded_motor(4)

# motors = [motor_one, motor_two, motor_three, motor_four]

# for motor in motors:
#     motor.set_speed(0)

# # Default speed of the motors per pico
# defaultSpeed = 265

# # Dictionary of notes and their corresponding motor, pico and speed
# noteDictionary = {

#     # Hard Stop
#     36: (0, 2, 0), # Pico 0, Motor Three (index 2), 0 rpm
#     38: (0, 2, 100), # Pico 0, Motor Four (index 2), 100 rpm

#     # Fundamentals

#     65: (0, 0, 200), # Pico 0, Motor One (index 0), 230 rpm
#     66: (0, 1, 200), # Pico 0, Motor Two (index 1), 230 rpm
#     67: (0, 2, 200), # Pico 0, Motor Three (index 2), 230 rpm
#     68: (0, 3, 200), # Pico 0, Motor Four (index 3), 230 rpm

#     69: (1, 0, 230), # Pico 1, Motor One (index 0), 230 rpm
#     70: (1, 1, 230), # Pico 1, Motor Two (index 1), 230 rpm
#     71: (1, 2, 230), # Pico 1, Motor Three (index 2), 230 rpm
#     72: (1, 3, 230), # Pico 1, Motor Four (index 3), 230 rpm

#     73: (2, 0, 230), # Pico 2, Motor One (index 0), 230 rpm
#     74: (2, 1, 230), # Pico 2, Motor Two (index 1), 230 rpm
#     75: (2, 2, 230), # Pico 2, Motor Three (index 2), 230 rpm
#     76: (2, 3, 230), # Pico 2, Motor Four (index 3), 230 rpm
    
#     # First Harmonics

#     77: (0, 0, 460), # Pico 0, Motor One (index 0), 460 rpm
#     78: (0, 1, 460), # Pico 0, Motor Two (index 1), 460 rpm
#     79: (0, 2, 460), # Pico 0, Motor Three (index 2), 460 rpm
#     80: (0, 3, 460), # Pico 0, Motor Four (index 3), 460 rpm

#     81: (1, 0, 460), # Pico 1, Motor One (index 0), 460 rpm
#     82: (1, 1, 460), # Pico 1, Motor Two (index 1), 460 rpm
#     83: (1, 2, 460), # Pico 1, Motor Three (index 2), 460 rpm
#     84: (1, 3, 460), # Pico 1, Motor Four (index 3), 460 rpm

#     85: (2, 0, 460), # Pico 2, Motor One (index 0), 460 rpm
#     86: (2, 1, 460), # Pico 2, Motor Two (index 1), 460 rpm
#     87: (2, 2, 460), # Pico 2, Motor Three (index 2), 460 rpm
#     88: (2, 3, 460), # Pico 2, Motor Four (index 3), 460 rpm
# }

# thisPico = 0 # This is the index of the pico that this script is running on

# # Create an instance of a polling object 
# poll_obj = select.poll()
# # Register sys.stdin (standard input) for monitoring read events with priority 1
# poll_obj.register(sys.stdin,1)
# # Pin object for controlling onboard LED

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
        
#         # If the character is a valid note
#         if note in noteDictionary.keys():
#             noteData = noteDictionary[note]
#             # If the note can be played on this pico
#             if noteData[0] == thisPico:
#                 # If the velocity is 0, stop the note by setting a default speed
#                 if velocity == 0:
#                     motors[noteData[1]].set_speed(defaultSpeed)
#                 else:
#                     # Set the speed of the motor based on the dictionary
#                     motors[noteData[1]].set_speed(noteData[2])
#     # # Small delay to avoid high CPU usage in the loop
#     # time.sleep(0.1)


from encoded_motor import EncodedMotor

motor_one = EncodedMotor.get_default_encoded_motor(1)
motor_two = EncodedMotor.get_default_encoded_motor(2)
motor_three = EncodedMotor.get_default_encoded_motor(3)
motor_four = EncodedMotor.get_default_encoded_motor(4)

motors = [motor_one, motor_two, motor_three, motor_four]

while True:
    whichMotor = int(input("Which motor? ")) - 1
    speed = float(input("Speed? "))

    print(f"Speed: {motors[whichMotor].get_speed()}, Position: {motors[whichMotor].get_position_counts()}")

    motors[whichMotor].set_speed(speed)
