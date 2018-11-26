import RPi.GPIO as GPIO
import time
import socket
import threading

# Pins for Motor Driver Inputs
GPIO_PWM = 13
GPIO_DIRECTION = 6
GPIO_ENABLE = 5    # ENABLE (False: ENABLE / True: DISABLE)

def setup():
    GPIO.setmode(GPIO.BCM)              #GPIO Numbering
    GPIO.setup(GPIO_PWM, GPIO.OUT)
    GPIO.setup(GPIO_DIRECTION, GPIO.OUT)
    GPIO.setup(GPIO_ENABLE, GPIO.OUT)

class thread_socket(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

    def run(self):
            print("Socket process !\n")
            port = 4021
            host = ''
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))
            sock.listen(1)
            conn, addr = sock.accept()
            while(True):
                data = conn.recv(10)
                if not data:
                    conn.sendall(data)
                    break
                data = data.decode()
                print(data)

class dcmotor_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

    def run(self):

        print("Input Duty: ")
        pwm.start(0)
        GPIO.output(GPIO_DIRECTION, True)
        GPIO.output(GPIO_ENABLE, False)
        while True:
            if(isfloat(data)==True):
                if(data == 0):
                    pwm.ChangeDutyCycle(0)
                elif(0<data<=100):
                    pwm.ChangeDutyCycle(data)

    def Suspend(self):
        self.__suspend = True
    def Resume(self):
        self.__suspend = False
    def Exit(self):
        self.__exit = True

def str_to_float(s):
    f = float(s)
    return f

def float_to_str(f):
    s = str(f)
    return s

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def isstr(value):
  try:
    str(value)
    return True
  except ValueError:
    return False

def loop():
    global data
    data = ""
    socket = thread_socket()
    socket.start()
    dc = dcmotor_thread()
    while True:
        if(isstr(data)==True):
        # print("Input Mode (Start: 1, Suspend: 2, Resume: 3, Exit: 4) \n")
            if(data == 'start'):
                data = str_to_float(data)
                dc.start()
                # float_to_str(data)
            elif(data == 'suspend'):
                dc.Suspend()
            elif(data == 'resume'):
                dc.Resume()
            elif(data == 'exit'):
                time.sleep(1)
                dc.Exit()
            else:
                None

def destroy():
    pwm.stop()
    GPIO.output(GPIO_ENABLE, True)  # motor stop
    GPIO.cleanup()              # Release resource

if __name__ == '__main__':   # Program start from here
        setup()
        pwm = GPIO.PWM(13,50)
        try:
            loop()
        except KeyboardInterrupt:
            destroy()
