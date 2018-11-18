import RPi.GPIO as GPIO
import time
import socket
import threading

GPIO_SERVO = 18     # Pins for Motor Inputs
data = 0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_SERVO, GPIO.OUT)

class thread_socket(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

    def run(self):
        global data
        print("Socket process !\n")
        port = 4011
        host = ''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(1)
        conn, addr = sock.accept()
        while True:
            data = conn.recv(10)
            if not data:
                conn.sendall(data)
                conn.close()
                break
            print(data.decode())
            data = data.decode()

class thread_servo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

    def run(self):
        print("Input Direction (Right: 2, Middle: 3, Left: 4)")
        s.start(0)
        while True:
            if(data == '1'):
                s.stop()                # motor stop
                GPIO.cleanup()          # Release resource
                break
            elif(data == '2'):
                s.ChangeDutyCycle(2)    # Right
            elif(data == '3'):
                s.ChangeDutyCycle(3)    # Middle
            elif(data == '4'):
                s.ChangeDutyCycle(4)    # Left
            else:
                s.ChangeDutyCycle(3)    # Middle

def servo():
    th_socket = thread_socket()
    th_socket.start()
    th_servo = thread_servo()
    th_servo.start()

def destroy():
    s.stop()                    # motor stop
    GPIO.cleanup()              # Release resource

if __name__ == '__main__':   # Program start from here
        setup()
        s = GPIO.PWM(GPIO_SERVO, 50)
        try:
            servo()
        except KeyboardInterrupt:
            destroy()
