# Pupil-Tracking
This repository is to organize and share my project on Eye Pupil Tracking using openCV library with Python. 
Pupil tracking is the most common challenge for a beginner in computer Vision. I have stumbled upon the idea a lot myself and came up with a neat algorithm to track pupil. 
This code has been tested on some videos upto now but all of them had clear magnified eyes in frame.
The purpose of using eye close-up as the basis of pupil tracking was because this project is mainly focused on use on VR Headset.


ALGORITHM:

1. Grab the frame and convert to gray scale.
2. Threshold the darkest part and binarize it.
3. Segment the binarized frame using series of segmentation.
4. Detect the edges
5. create a blob detector and apply on the edge frame
6. create a keypoint object and extract the coordinates from it.
7. Find the center of the frame and joint the line from it to the keypoint cordinate.
8. Draw a circle around the keypoint to mark the pupil.
9. Show the output frame.

Note: The key to this algorithm is to find a suitable set of parameters for the blob detection. The process is highly mannual as of now and I would like the suggestion of the open source community to create further versions of it by making it automatic.

