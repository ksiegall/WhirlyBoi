from encoded_motor import EncodedMotor
import time

motor_one = EncodedMotor.get_default_encoded_motor(1)

motor_two = EncodedMotor.get_default_encoded_motor(2)
motor_three = EncodedMotor.get_default_encoded_motor(3)
motor_four = EncodedMotor.get_default_encoded_motor(4)

motors = [motor_one, motor_two, motor_three, motor_four]

while True:
    whichMotor, speed = input("Which motor? "), input("Speed? ")
    whichMotor = int(whichMotor)-1
    speed = float(speed)
    motors[whichMotor].set_speed(speed)
    # print(f"Position: {motor_one.get_position_counts()}\tSpeed: {motor_one.get_speed()}")
    # time.sleep(0.1)