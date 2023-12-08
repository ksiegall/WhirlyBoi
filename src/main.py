
import time
import select
import sys
from machine import Pin, PWM
from encoded_motor import EncodedMotor
from board import Board

board = Board.get_default_board()
motor_one = EncodedMotor.get_default_encoded_motor(1)

motor_two = EncodedMotor.get_default_encoded_motor(2)
motor_three = EncodedMotor.get_default_encoded_motor(3)
motor_four = EncodedMotor.get_default_encoded_motor(4)

motors = [motor_one, motor_two, motor_three, motor_four]

# while True:
#     whichMotor, speed = input("Which motor? "), input("Speed? ")
#     whichMotor = int(whichMotor)-1
#     speed = float(speed)
#     motors[whichMotor].set_speed(speed)
#     # print(f"Position: {motor_one.get_position_counts()}\tSpeed: {motor_one.get_speed()}")
#     # time.sleep(0.1)

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
        # Toggle the state of the LED
        # Print a message indicating that the LED has been toggled
        print (f"Note: {ord(ch[0])} Velocity: {ord(ch[1])}")
        board.led_blink(ord(ch[0]))
    # Small delay to avoid high CPU usage in the loop
    time.sleep(0.1)