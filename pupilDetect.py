import numpy as np
import cv2


# make simple blob detect object
params = cv2.SimpleBlobDetector_Params()

# set up parameters....those with true value are only affected
params.filterByColor = False
params.blobColor = 0

# Change thresholds
params.minThreshold = 50
params.maxThreshold = 200

# Filter by Area.
params.filterByArea = True
params.minArea = 150

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.5

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.9

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.5

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

# capture the frames from video
vc = cv2.VideoCapture('/home/rahul/Videos/eye1.mp4')

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

    rval, frame = vc.read() # grab a frame
    shape = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert to gray scale
    output = frame.copy()  #to show output
    ret,thresh = cv2.threshold(gray,5,255,cv2.THRESH_BINARY) #threshold only the darkest part
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


    # Detect blobs.
    keypoints = detector.detect(edge)
    im_with_keypoints = cv2.drawKeypoints(output, keypoints, np.array([]), (0, 255, 0),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    if (len(keypoints) > 0):

        for keyPoint in keypoints:
            x = int(keyPoint.pt[0])
            y = int(keyPoint.pt[1])
            s = int(keyPoint.size)
            ang = keyPoint.angle
            area1 = np.pi * (s / 2) ** 2
            print x, y, s, ang, "Area: ", area1

            cv2.circle(output, (x, y), int(s / 2), (0, 0, 255))
            cv2.circle(output, (x, y), 2, (0, 255, 255), -1)
            cv2.line(output,(int(shape[1]/2) ,int(shape[0]/2)),(x,y),(255,0,0)) # direction from center of the frame to the center of the pupil


    # cv2.imshow("preview", frame)
    # cv2.imshow("opening", opening)
    # cv2.imshow("sure_bg", sure_bg)
    # cv2.imshow("sure_fg", sure_fg)
    # cv2.imshow("unknown", unknown)
    cv2.imshow("output", output)
    key = cv2.waitKey(5) & 0xFF
    if key == 27:  # exit on ESC
        break
vc.release()
cv2.destroyAllWindows()
