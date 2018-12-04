import RPi.GPIO as GPIO
import time
import socket
import threading

# Pins for Motor Driver Inputs
GPIO_DC = 13       # DC_MOTOR_PWM
GPIO_DIRECTION = 6  # DIRECTION (True: Forward / False: Backward)
GPIO_ENABLE = 5     # ENABLE (False: ENABLE / True: DISABLE)
GPIO_SERVO = 18     # SERVO_MOTOR_PWM
data = 0            # Initial input data

def setup():
    GPIO.setmode(GPIO.BCM)              #GPIO Numbering Method
    GPIO.setup(GPIO_DC, GPIO.OUT)
    GPIO.setup(GPIO_DIRECTION, GPIO.OUT)
    GPIO.setup(GPIO_ENABLE, GPIO.OUT)
    GPIO.setup(GPIO_SERVO, GPIO.OUT)

class thread_motor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

    def run(self):
        #########################SOCKET#########################
        port = 4000
        host = ''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(1)
        connect, address = sock.accept()
        ########################################################
        global data
        print("Input Data: ")
        dc.start(0)
        servo.start(0)
        while True:
            data = connect.recv(10)
            if not data or (data.decode() == '1'):
                connect.sendall(data)
                connect.close()
                break
            data = data.decode()
            data = float(data)
            if(isfloat(data) == True):
                if(data == 0):
                    GPIO.output(GPIO_DIRECTION, False)
                    dc.ChangeDutyCycle(50)
                    time.sleep(0.2)
                    GPIO.output(GPIO_ENABLE, True)
                elif(0<data<=100):
                    if(data == 1):
                        break
                    elif(data == 2):
                        servo.ChangeDutyCycle(2)    # Right
                    elif(data == 3):
                        servo.ChangeDutyCycle(3.4)    # Middle
                    elif(data == 4):
                        servo.ChangeDutyCycle(6)    # Left
                    else:
                        GPIO.output(GPIO_ENABLE, False)
                        GPIO.output(GPIO_DIRECTION, True)
                        dc.ChangeDutyCycle(data)

def isfloat(value):
  try:
      float(value)
      return True
  except ValueError:
      return False

def run():
    motor = thread_motor()
    motor.start()

def destroy():
    dc.stop()
    servo.stop()
    GPIO.cleanup()              # Release resource

if __name__ == '__main__':   # Program start from here
        setup()
        dc = GPIO.PWM(GPIO_DC, 50)
        servo = GPIO.PWM(GPIO_SERVO, 50)
        try:
            run()
        except KeyboardInterrupt:
            destroy()
