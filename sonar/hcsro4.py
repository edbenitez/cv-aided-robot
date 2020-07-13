import Jetson.GPIO as GPIO
from datetime import datetime
import time

class HCSRO4():
    def __init__(self, trigger, echo, gpio_low_input):
        self.triggerPin = trigger
        self.echoPin = echo
        self.gpio_low_input = gpio_low_input
        self.max_distance = 500 # cm
        self.roundtrip_cm = 58 # rtt for 1cm distance in micro seconds
        self.max_sensor_delay = 5800 # micro seconds
        self.max_echo_time_us = self.max_distance * self.roundtrip_cm + self.max_sensor_delay # micro seconds
        self.max_echo_time_ms = self.max_echo_time_us // 3 # milli seconds
        self.t_before = -1
        self.t_after = -1
        self.t_duration = -1

    def triggerPing(self):
        
        GPIO.output(self.triggerPin, GPIO.LOW)
        time.sleep(4/1000000.0) # sleep 4 micro seconds
        
        GPIO.output(self.triggerPin, GPIO.HIGH)
        time.sleep(10/1000000.0) # sleep 10 micro seconds
        
        GPIO.output(self.triggerPin, GPIO.LOW)
        
        self.t_before = datetime.now()

        '''    
        #print('before', self.t_before)
        if GPIO.input(self.echoPin) == 1:
            return False

        while GPIO.input(self.echoPin) != 1:
            self.t_after = datetime.now()
            self.t_duration = self.t_after - self.t_before
            if self.t_duration.microseconds > self.max_echo_time_us:
                return False
        #print('after', self.t_after)
        return True

        '''

    def setPins(self):
        GPIO.setmode(GPIO.BOARD) # enable mode to use pin numbers 
        GPIO.setup(self.gpio_low_input, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)
        
    def cleanup(self):
        print('Cleaning channels')
        GPIO.cleanup()
    
    def callback_fn(self):
        echoVal = GPIO.input(self.echoPin)
        print(echoVal)
        #self.t_after = datetime.now().microsecond
        #self.t_duration = self.t_after - self.t_before
        #print(self.t_duration)

if __name__ == "__main__":
    sensor = HCSRO4(trigger=33, echo=31, gpio_low_input=32)
    sensor.setPins()
    print('ECHO INITIAL VALUE: ', GPIO.input(sensor.echoPin))
    GPIO.add_event_detect(sensor.echoPin, GPIO.RISING, callback=sensor.callback_fn()) 
    for i in range(999):
        sensor.triggerPing()
        #print(sensor.t_duration.microseconds/48.0)
        time.sleep(1/1000) # 1 milli seconds
    sensor.cleanup()

