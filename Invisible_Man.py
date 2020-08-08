import cv2
import numpy as np
import time

print("""

Harry :  Hey !! Would you like to try my invisibility cloak ??

         Its awesome !!


         Prepare to get invisible .....................
    """)


cap = cv2.VideoCapture(0)
time.sleep(3)
background=0
for i in range(30):
	ret,background = cap.read()

background = np.flip(background,axis=1)

video_FourCC = cv2.VideoWriter_fourcc(*'XVID')
video_fps       = cap.get(cv2.CAP_PROP_FPS)
video_size      = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
output_path = "output.mp4"
isOutput = True if output_path != "" else False

if isOutput:
    print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
    out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)

while(cap.isOpened()):
    ret, img = cap.read()

	# Flipping the image (Can be uncommented if needed)
    img = np.flip(img,axis=1)

	# Converting image to HSV color space.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    value = (35, 35)

    blurred = cv2.GaussianBlur(hsv, value,0)

	# Defining lower range for red color detection.
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv,lower_red,upper_red)

	# Defining upper range for red color detection
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)

	# Addition of the two masks to generate the final mask.
    mask = mask1+mask2
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))

	# Replacing pixels corresponding to cloak with the background pixels.
    img[np.where(mask==255)] = background[np.where(mask==255)]

    cv2.imshow('Display',img)

    if isOutput:
        out.write(img)
    k = cv2.waitKey(10)
    if k == 27:
	    break
