from encoded_motor import EncodedMotor
import time

motor_one = EncodedMotor.get_default_encoded_motor(1)
motor_three = EncodedMotor.get_default_encoded_motor(3)

while True:
    user_input = float(input(f"Motor 1 - Current Speed: {motor_one.get_speed()}\tEnter a speed (rpm): "))
    motor_one.set_speed(user_input)
    user_input = float(input(f"Motor 3 - Current Speed: {motor_three.get_speed()}\tEnter a speed (rpm): "))
    motor_three.set_speed(user_input)
    # print(f"Position: {motor_one.get_position_counts()}\tSpeed: {motor_one.get_speed()}")
    # time.sleep(0.1)