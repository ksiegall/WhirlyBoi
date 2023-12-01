from encoded_motor import EncodedMotor
import time

motor_one = EncodedMotor.get_default_encoded_motor(1)

while True:
    user_input = int(input(f"Current Speed: {motor_one.get_speed()}\tEnter a speed (rpm): "))
    motor_one.set_speed(user_input)
    # print(f"Position: {motor_one.get_position_counts()}\tSpeed: {motor_one.get_speed()}")
    # time.sleep(0.1)