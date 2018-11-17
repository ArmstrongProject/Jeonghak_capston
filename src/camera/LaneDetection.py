import cv2
import numpy

class Detect:
    img_max_x = 0
    img_max_y = 0

    def Img_ROI(self, img):
        canny = cv2.Canny(img, 50, 200)
        mimg = canny[int(self.img_max_y/2):self.img_max_x, int(self.img_max_x/2-self.img_max_x/4):int(self.img_max_x/2+self.img_max_x/4)]
        mimg_y, mimg_x = mimg.shape
        real_dot = numpy.array([0, 0])
        for y in range(0,mimg_y - 1):
            temp_dot = []
            for x in range(0, mimg_x - 1):
                #print(mimg[y, x])
                if(mimg[y,x] > 250):
                    temp_dot.append(int(x))
            if(temp_dot is not None):
                temp = numpy.array(temp_dot)
                if(temp.sum()/temp.size == temp.sum()/temp.size):
                    real_dot = numpy.append([real_dot],[int(temp.sum()/temp.size), int(y)])
        print(real_dot)
        real_dot = real_dot.reshape((-1, 1, 2))
        #numpy.resize(real_dot,(int(real_dot.size/2),2))
        #print(real_dot)
        mimg = cv2.cvtColor(mimg, cv2.COLOR_GRAY2RGB)
        #print(mimg_x, mimg_y)
        cv2.line(mimg, (int(mimg_x/2), mimg_y), (int(mimg_x/2), 0),(0, 0, 255), 3)
        cv2.polylines(mimg,[real_dot], False, (0, 255, 0), 3) 
        return mimg

    def __init__(self, img_x, img_y):
        #mimg = cv2.imread(img)
        #print(img.shape)
        self.img_max_y, self.img_max_x = img_x, img_y
