import RPi.GPIO as GPIO
import time
import socket
import threading

# Pins for Motor Driver Inputs
GPIO_PWM = 13
GPIO_DIRECTION = 6
GPIO_ENABLE = 5    # ENABLE (False: ENABLE / True: DISABLE)
mode = 0
duty = 0

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
            global mode, duty
            print("Socket process !\n")
            port = 4010
            host = ''
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))
            sock.listen(1)
            conn, addr = sock.accept()
            while(True):
                mode = conn.recv(10)
                duty = conn.recv(10)
                if not mode or duty:
                    conn.sendall(mode)
                    conn.sendall(duty)
                    break
                print(mode.decode())
                print(duty.decode())
                mode = mode.decode()
                duty = duty.decode()

class dcmotor_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

    def run(self):
        print("Input Mode (Start: 1, Suspend: 2, Resume: 3, Exit: 4) \n")
        pwm.start(0)
        while True:
            if(duty == '0'):
                GPIO.output(GPIO_ENABLE, True)
            elif(duty != '0'):
                GPIO.output(GPIO_ENABLE, False)
                pwm.ChangeDutyCycle(int(duty))
                print("Duty Cycle = %s%%" %duty)
                # else:
                    # print("Input direction, again")

    def Suspend(self):
        self.__suspend = True
    def Resume(self):
        self.__suspend = False
    def Exit(self):
        self.__exit = True

def loop():
    th_socket = thread_socket()
    th_socket.start()
    time.sleep(1)
    dc = dcmotor_thread()
    while True:
        if(mode == 1):
            dc.start()
            time.sleep(1)
        elif(mode == 2):
            dc.Suspend()
            time.sleep(1);
        elif(mode == 3):
            dc.Resume()
            time.sleep(1)
        elif(mode == 4):
            dc.Exit()
            time.sleep(1)
            exit(0)
        # else:
            # print("Input Mode, again")

def destroy():
    pwm.stop()
    GPIO.output(GPIO_ENABLE, True)  # motor stop
    GPIO.cleanup()              # Release resource

if __name__ == '__main__':   # Program start from here
        setup()
        pwm = GPIO.PWM(13,50)
        try:
            loop()
        except KeyboardInterrupt: # When 'Crtl + C' is pressed, the child program destroy() will be executedself.
            destroy()
