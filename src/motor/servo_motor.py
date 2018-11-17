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
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False
        self.data = data

    def run(self):
            global data
            print("Socket process !\n")
            port = 4052
            host = ''
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, port))
            sock.listen(1)
            conn, addr = sock.accept()
            while True:
                data = conn.recv(1024)
                if not data:
                    conn.sendall(data)
                    conn.close()
                    break
                print(data.decode())
                data = data.decode()
                return(data)

class thread_servo(threading.Thread):
    def __init__(self, direction):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False
        self.direction = direction

    def run(self):
        print("Input Direction (Right: 2, Middle: 3, Left: 4)")
        p.start(0)
        if(self.direction =='2'):
            p.ChangeDutyCycle(2)    # Right
            print("angle : 2")
        elif(self.direction =='3'):
            p.ChangeDutyCycle(3)    # Middle
            print("angle : 3")
        elif(self.direction =='4'):
            p.ChangeDutyCycle(4)    # Left
            print("angle : 4")
        else:
            print("Please Input number, again")

def loop():
        th_socket = thread_socket(data)
        th_socket.start()
        time.sleep(3)
        while True:
            time.sleep(3)
            while True:
                th_servo = thread_servo(data)
                th_servo.start()
                time.sleep(3)

def destroy():
    p.stop()                    # motor stop
    GPIO.cleanup()              # Release resource

if __name__ == '__main__':   # Program start from here
        setup()
        p = GPIO.PWM(GPIO_SERVO, 50)
        try:
            loop()
        except KeyboardInterrupt:
# When 'Crtl + C' is pressed, the child program destroy() will be executedself.
            destroy()
