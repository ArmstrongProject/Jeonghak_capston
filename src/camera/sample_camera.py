import cv2
import LaneDetection

class sample_cv:
    def process_video(self):
        Vedio_size_x = 720
        Vedio_size_y = 1280
        cap = cv2.VideoCapture('test.mp4')
        dectector = LaneDetection.Detect(720, 1280)
        while(cap.isOpened()):
            ret, frame = cap.read()
            grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            ROI = dectector.Img_ROI(grey)

            edge1 = cv2.Canny(grey, 50, 200)
            cv2.imshow('video', grey)
            cv2.imshow('Canny', edge1)
            cv2.imshow('ROI', ROI)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def __init__(self):
        self.process_video()
