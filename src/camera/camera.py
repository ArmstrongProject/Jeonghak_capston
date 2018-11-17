import io
import socket
import struct
import time
import picamera
import cv2

# create socket and bind host
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect(('192.168.1.100', 8000))
#connection = client_socket.makefile('wb')
class pi_camera:

    def camera_control(self):
        try:
           with picamera.PiCamera() as camera:
                camera.resolution = (320, 240)      # pi camera resolution
                camera.framerate = 15               # 15 frames/sec
                time.sleep(2)                       # give 2 secs for camera to initilize
                start = time.time()
                stream = io.BytesIO()

                # send jpeg format video stream
                #for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                while True:
                    camera.capture_continuous(stream, 'jpeg', use_video_port = True)
                    #connection.write(struct.pack('<L', stream.tell()))
                    #connection.flush()
                    #stream.seek(0)
                    #connection.write(stream.read())
                    #if time.time() - start > 600:
                    #    break
                    grey = cv2.cvtColor(frame,cv2.CLOLR_RBG2GRAY)
                    cv2.imshow('video',grey);
                    stream.seek(0)
                    stream.truncate()
                    #connection.write(struct.pack('<L', 0))
        finally:
            time.sleep(1)
            #connection.close()
            #client_socket.close()

    def __init__(self):
        #connect_socket()
        self.camera_control()
