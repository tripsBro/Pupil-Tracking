import numpy as np
import cv2


# create surf object
surf = cv2.xfeatures2d.SURF_create()

# capture the frames from video
vc = cv2.VideoCapture('/home/rahul/Videos/eye_for _tracking.mp4')

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

    rval, frame = vc.read() # grab a frame
    shape = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to gray scale
    output = frame.copy()  #to show output
    ret,thresh = cv2.threshold(gray,45,255,cv2.THRESH_BINARY) #threshold only the darkest part
    # steps for noise removal
    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    opening = cv2.erode(opening, (3, 3), iterations=1)
    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=1)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    # try
    erode = cv2.erode(sure_bg, (5, 5), iterations=1, borderType=2, borderValue=cv2.MORPH_HITMISS)
    edge = cv2.Canny(erode, 35, 55, apertureSize=5, L2gradient=True)

    

    (kps, descs) = surf.detectAndCompute(erode, None)

    # zipped = zip(kps,descs)
    # print "kps",kps[0]

    if (len(kps) > 0):
        ls = list(np.zeros((len(kps),1)))

        for (i,keyPoint) in enumerate(kps):
            print "kp", keyPoint
            x = int(keyPoint.pt[0])
            y = int(keyPoint.pt[1])
            s = int(keyPoint.size)
            ang = keyPoint.angle
            area1 = np.pi * (s / 2) ** 2
            print x, y, s, ang, "Area: ", area1
            ls.insert(i,s)
            m = max(ls)
            if m==s:
                key = kps[i]
                x1 = int(key.pt[0])
                y1 = int(key.pt[1])
                s1 = int(key.size)
                ang1 = key.angle
                aream = np.pi * (s1 / 2) ** 2

                cv2.circle(output, (x1, y1), int(s1 / 2), (0, 0, 255))
                cv2.circle(output, (x1, y1), 2, (0, 255, 255), -1)

    

    
    cv2.imshow("output", output)
    key = cv2.waitKey(5) & 0xFF
    if key == 27:  # exit on ESC
        break
vc.release()
cv2.destroyAllWindows()

