import RPi.GPIO as GPIO
import time
import socket
import threading

# Pins for Motor Driver Inputs
GPIO_PWM = 13   # PWM
GPIO_DIR = 6    # DIR
GPIO_EN = 5    # ENABLE (False: ENABLE / True: DISABLE)
mode = 0
dir = 0
duty = 0

def setup():
    GPIO.setmode(GPIO.BCM)              #GPIO Numbering
    GPIO.setup(GPIO_PWM, GPIO.OUT)
    GPIO.setup(GPIO_DIR, GPIO.OUT)
    GPIO.setup(GPIO_EN, GPIO.OUT)

class thread_socket(threading.Thread):
    def __init__(self, mode, dir, duty):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False
        self.mode = mode
        self.dir = dir
        self.duty = duty

    def run(self):
            global mode, dir, duty
            while True:
            ### Suspend ###
                while self.__suspend:
                    time.sleep(1)
                ### Process ###
                print("Socket process !\n")
                port = 4015
                host = ''
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind((host, port))
                sock.listen(1)
                conn, addr = sock.accept()
                while(True):
                    mode = conn.recv(1024)
                    if not mode:
                        break
                    print(mode.decode())
                    conn.sendall(mode)
                    mode = mode.decode()
                    return(mode, dir, duty)
                conn.close()
                ### Exit ###
                # if self.__exit:
                    # break

    def Suspend(self):
        self.__suspend = True
    def Resume(self):
        self.__suspend = False
    def Exit(self):
        self.__exit = True

class dcmotor_thread(threading.Thread):
    def __init__(self, direction, dutycycle):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False
        self.direction = direction
        self.dutycycle = dutycycle

    def run(self):
        while True:
            while self.__suspend:
                time.sleep(0.5)
            print("DC motor process !")
            pwm.start(0)
            if(self.dutycycle == '0'):
                GPIO.output(GPIO_EN, True)
            elif(self.dutycycle != '0'):
                GPIO.output(GPIO_EN, False)
                pwm.ChangeDutyCycle(self.dutycycle)
                if(self.direction == '1'):
                    print("Direction: Forward, " + "Duty Cycle = %d%%" %self.dutycycle)
                elif(self.direction == '0'):
                    print("Direction: Back, " + "Duty Cycle = %d%%" %self.dutycycle)
                else:
                    print("Input direction, again")
            if self.__exit:
                break

    def Suspend(self):
        self.__suspend = True
    def Resume(self):
        self.__suspend = False
    def Exit(self):
        self.__exit = True

# class dc_motor():
#     def __init__(self, direction, dutycycle):
#         self.direction = direction
#         self.dutycycle = dutycycle
#
#     def drive(self):
#
#             #     #print("100HZ, Duty Cycle = %d%%" %self.dutycycle)
#             #     GPIO.output(GPIO_PWM, True)
#             #     GPIO.output(GPIO_DIR, self.direction)
#
#             #     time.sleep(self.dutycycle/100)
#             #     GPIO.output(GPIO_EN, True)
#             #     time.sleep((100-self.dutycycle)/100)
#             #     mode = input()
#
#     def stop(self):
#         print("stop")
#         GPIO.output(GPIO_EN, True)

def loop():
    th_socket = thread_socket(mode, dir, duty)
    th_socket.start()
    time.sleep(5)
    # mode = input("Input Mode (Start: 1, Suspend: 2, Resume: 3, Exit: 4) \n")
    while True:
        if(mode == 1):
            dc = dcmotor_thread(dir, duty)
            dc.start()
            time.sleep(3)
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
    GPIO.output(GPIO_EN, True)  # motor stop
    GPIO.cleanup()              # Release resource

if __name__ == '__main__':   # Program start from here
        setup()
        pwm = GPIO.PWM(13,50)
        try:
            loop()
        except KeyboardInterrupt: # When 'Crtl + C' is pressed, the child program destroy() will be executedself.
            destroy()
