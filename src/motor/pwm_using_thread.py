import RPi.GPIO as GPIO
import time
import threading

# Pins for Motor Driver Inputs
GPIO_PWM = 13   # PWM
GPIO_DIR = 6    # DIR
GPIO_EN = 5    # ENABLE (False: ENABLE / True: DISABLE)
mode = 0

def setup():
    GPIO.setmode(GPIO.BCM)              #GPIO Numbering
    GPIO.setup(GPIO_PWM, GPIO.OUT)
    GPIO.setup(GPIO_DIR, GPIO.OUT)
    GPIO.setup(GPIO_EN, GPIO.OUT)

class thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

    def run(self):
        while True:
            while self.__suspend:
                time.sleep(0.5)
            print("Thread process !")
            if self.__exit:
                break

    def Suspend(self):
        self.__suspend = True
    def Resume(self):
        self.__suspend = False
    def Exit(self):
        self.__exit = True

class dc_motor():
    def __init__(self, direction, dutycycle):
        self.direction = direction
        self.dutycycle = dutycycle

    def drive(self):
        while True:
            if(self.dutycycle == 0):
                GPIO.output(GPIO_EN, True)
            elif(self.dutycycle != 0):
                if(self.direction == 1):
                    print("Direction: Forward, " + "Duty Cycle = %d%%" %self.dutycycle)
                elif(self.direction == 0):
                    print("Direction: Back, " + "Duty Cycle = %d%%" %self.dutycycle)
                #print("100HZ, Duty Cycle = %d%%" %self.dutycycle)
                GPIO.output(GPIO_PWM, True)
                GPIO.output(GPIO_DIR, self.direction)
                GPIO.output(GPIO_EN, False)
                time.sleep(self.dutycycle/100)
                GPIO.output(GPIO_EN, True)
                time.sleep((100-self.dutycycle)/100)
            if(mode == 0):
                time.sleep(1)
                threading.Thread.Suspend()

    def stop(self):
        print("stop")
        GPIO.output(GPIO_EN, True)


def loop():
    while True:
        mode = input("Input Mode : ")
        if(mode == 1):
            dir = input("Input Direction : ")
            duty = input("Input Duty Cycle : ")
            dc = dc_motor(dir, duty)
            th = threading.Thread(target = dc.drive())
        elif(mode == 2):
            time.sleep(1);
            exit(0)
        else:
            print("Input Mode, again")

def destroy():
    GPIO.output(GPIO_EN, True)  # motor stop
    GPIO.cleanup()              # Release resource

if __name__ == '__main__':   # Program start from here
        setup()
        try:
            loop()
        except KeyboardInterrupt: # When 'Crtl + C' is pressed, the child program destroy() will be executedself.
            destroy()
