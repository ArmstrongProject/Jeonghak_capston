import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_RP = 13   # PWM
GPIO_RN = 6    # DIR
GPIO_EN = 5    # ENABLE (False: ENABLE / True: DISABLE)

GPIO.setup(GPIO_RP, GPIO.OUT)
GPIO.setup(GPIO_RN, GPIO.OUT)
GPIO.setup(GPIO_EN, GPIO.OUT)


try:
    while True:
        for i in range(0,100):
            print("100HZ, duty bee = 20%")
            GPIO.output(GPIO_RP, True)
            GPIO.output(GPIO_RN, True)
            GPIO.output(GPIO_EN, False)
            time.sleep(0.002)


            GPIO.output(GPIO_EN, True)
            time.sleep(0.008)

        for i in range(0,100):
            print("100HZ, duty bee = 50%")
            GPIO.output(GPIO_RP, True)
            GPIO.output(GPIO_RN, True)
            GPIO.output(GPIO_EN, False)
            time.sleep(0.005)


            GPIO.output(GPIO_EN, True)
            time.sleep(0.005)


        for i in range(0,100):
            print("100HZ, duty bee = 80%")
            GPIO.output(GPIO_RP, True)
            GPIO.output(GPIO_RN, True)
            GPIO.output(GPIO_EN, False)
            time.sleep(0.008)


            GPIO.output(GPIO_EN, True)
            time.sleep(0.002)


        for i in range(0,100):
            print("100HZ, duty bee = 100%")
            GPIO.output(GPIO_RP, True)
            GPIO.output(GPIO_RN, True)
            GPIO.output(GPIO_EN, False)
            time.sleep(0.01)

finally:
    GPIO.cleanup()
