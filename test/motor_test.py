from __future__ import print_function
import time
import sys
import math
import qwiic_scmd

myMotor = qwiic_scmd.QwiicScmd()

def run_motor_test():
    print("Start: ")
    motor_left = 0
    motor_right = 1
    forward = 0
    backward = 1
    #print(dir(myMotor))
    if not myMotor.is_connected():
        print("Motor driver not connected!", file=sys.stderr)
    else:
        print("Motor driver connection establedished.")

if __name__ == "__main__":
    try:
        run_motor_test()
    except(KeyboardInterrupt, SystemExit) as exErr:
        print("Ending test.")
        myMotor.disable()
        sys.exit(0)


