# USAGE
# python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat --video blink_detection_demo.mp4
# python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat

# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
from spellchecker import SpellChecker
spell = SpellChecker()
from tkinter import *
from PIL import ImageTk , Image
import os
def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear
#to chech the morse code
def checkKey(lang, key):
    if key in lang.keys():
        print(key ,'= ', lang[key])
    else:
        print('not present')

def checkKey1(hospital, key):
    if key in lang.keys():
        print(key ,'= ', hospital[key])
    else:
        print('not present')
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="",
	help="path to input video file")
args = vars(ap.parse_args())
 
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.25
EYE_AR_SHORT = 2
EYE_AR_LONG = 7
EYE_OPEN = 100

# initialize the frame counters and the total number of blinks
COUNTER = 0
COUNT_OPEN = 0
TOTAL_SHORT = 0
TOTAL_LONG = 0

array_count = 0

check = 0
check_open = 0

#print("\nEnter 1 for normal english language")
#print("\nEnter 2 for hospital environment")
#choice = int(input("\n\nEnter the choice : "))

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = FileVideoStream(args["video"]).start()
fileStream = True
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
fileStream = False
time.sleep(1.0)

#creatin array
import array

arr = [None]*0
ar=''
s=''
# loop over frames from the video stream
while True:
        
	# if this is a file video stream, then we need to check if
	# there any more frames left in the buffer to process
	if fileStream and not vs.more():
		break

	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale
	# channels)
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)
        
	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# extract the left and right eye coordinates, then use the
		# coordinates to compute the eye aspect ratio for both eyes
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)

		# average the eye aspect ratio together for both eyes
		ear = (leftEAR + rightEAR) / 2.0

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 0), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < EYE_AR_THRESH:
			COUNTER += 1
			check=1

		# otherwise, the eye aspect ratio is not below the blink
		# threshold
		else:
			# if the eyes were closed for a sufficient number of
			# then increment the total number of blinks
			if ((COUNTER >= EYE_AR_SHORT) and (COUNTER <=EYE_AR_LONG)):
				TOTAL_SHORT += 1
				print ("\n0")
				check = 0
				if(check==0):
                                        ar1='0'
                                        ar=ar+ar1
                                        array_count+=1
                                        check = 1
			if(COUNTER > EYE_AR_LONG):
                                TOTAL_LONG +=1
                                print ("\n1")
                                if(check!=0):
                                        ar1='1'
                                        ar=ar+ar1
                                        array_count+=1
                                        check = 1
			# reset the eye frame counter
			COUNTER = 0

		if ear > EYE_AR_THRESH:
                        COUNT_OPEN +=1
                        check_open=0
                        if((COUNT_OPEN >= EYE_OPEN) and (check_open == 0)):
                                print("\n Break")
                                ar1='B'
                                ar=ar+ar1
                                array_count+=1
                                check_open=1
                                COUNT_OPEN = 0
		# draw the total number of blinks on the frame along with
		# the computed eye aspect ratio for the frame
		
		cv2.putText(frame, "Blink Count long: {}".format(TOTAL_LONG), (30, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
		cv2.putText(frame, "Blink Count short: {}".format(TOTAL_SHORT), (30, 60),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
		cv2.putText(frame, "Ratio: {:.2f}".format(ear), (300, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (40, 80, 255), 2)
		# show the frame
	
	cv2.imshow("Frame", frame)
	
	key = cv2.waitKey(1) & 0xFF
        
  
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
w1=[0]
w2=[[0],[1],[0,1]]
w3=[[0],[1],[2],[0,1],[1,2],[0,2],[0,1,2]]
w4=[[0],[1],[2],[3],[0,1],[1,2],[2,3],[0,3],[0,2],[1,3],[0,1,2],[1,2,3],[0,2,3],[0,1,3],[0,1,2,3]]
w5=[[0],[1],[2],[3],[4],[0,1],[1,2],[2,3],[3,4],[0,2],[1,3],[2,4],[0,3],[1,4],[0,4],[0,1,2],[1,2,3],[2,3,4],[0,1,3],[1,2,4],[0,2,3],[1,3,4],[0,1,4],[0,3,4],[0,2,4],[0,1,2,3],[1,2,3,4],
    [0,1,2,4],[0,1,3,4],[0,2,3,4],[1,2,3,4],[0,1,2,3,4]]

nlangf={'0':'E',
       '1':'T',
       '00':'A',
       '11':'I',
       '01':'N',
       '10':'O',
       '000':'S',
       '001':'H',
       '100':'R',
       '010':'D',
       '011':'L',
       '110':'U',
       '111':'C'}

nlangs={'E':'Z',
       'T':'J',
       'A':'X',
       'I':'Q',
       'N':'K',
       'O':'V',
       'S':'B',
       'H':'G',
       'R':'P',
       'D':'W',
       'L':'Y',
       'U':'F',
       'C':'M'}

print(ar)
al=''
s=''

s=''
arr = ar.split('BB')
a=len(arr)-1
i=0
temp1=0
while (i<a):
    arrr= arr[i].split('B')
    j=0
    b=len(arrr)
    new=[None]*b
    while (j<b):
        key=arrr[j]
        if key in nlangf.keys():
            temp=nlangf[key]
            s=s+temp
        else:
            print('not present')
        j=j+1
    print ('Input sting is : ',s)
    i+=1
    length= len(s)
clone=[None]*0
i=0

while(i<length):
    clone.append(s[i])
    i+=1
dic=[]
if(length==1):
    dic = w1.copy()
elif(length==2):
    dic = w2.copy()
elif(length==3):
    dic = w3.copy()
elif(length==4):
    dic = w4.copy()
elif(length==5):
    dic = w5.copy()
temp_length=length
times=1
while temp_length>0:
    times=times*2
    temp_length-=1
i=0
words=[]
words.append(s)
temp_letter=''
while(i<times-1):
    temp=dic[i]
    temp_leng=len(temp)
    clone1=clone.copy()
    j=0
    new=''
    while(j<length):
        if j in temp:
            key=clone[j]
            temp_letter=nlangs[key]
            clone1[j]=temp_letter
        j+=1
    for x in clone1: 
        new += x
    words.append(new)
    i+=1

length=len(words)
i=0
corrections=[]
while(i<length):
    s=words[i]
    misspelled = spell.unknown([s])
    for word in misspelled:
        print(spell.correction(s))
        corrections.append(spell.correction(s))
    i+=1
length=len(corrections)
i=0
numbers=[]
occ=0
while(i<length):
    a=corrections[i]
    numbers.append(corrections.count(a))
    i+=1

maxpos = numbers.index(max(numbers))
print("\n\n\n It may be : ",corrections[maxpos])
a=''
b=''
a=corrections[maxpos]
temp=corrections[maxpos]

corrections.remove(temp)

occ=0
i=0
length-=1
numbers=[]
while(i<length):
    a=corrections[i]
    numbers.append(corrections.count(a))
    i+=1
    
maxpos = numbers.index(max(numbers))

print("\n Or else it can be : ",corrections[maxpos])
b=corrections[maxpos]
f = open(r"C:\xampp\htdocs\text.txt", "w")
f.write(a)
f.close()
f = open(r"C:\xampp\htdocs\text.txt", "a")
f.write("\n or else %s"%b)
f.close()
# do a bit of cleanup

cv2.destroyAllWindows()
vs.stop()

# E A
