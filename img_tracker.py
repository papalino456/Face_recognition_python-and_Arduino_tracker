#import required libraries
import cv2
import time
import serial

#uncomment for communication with arduino
#ser = serial.Serial("COM3",9600)

#point to the haar cascade file in the directory
cascPath = "haarcascade.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

#start the camera
video_capture = cv2.VideoCapture(0) 

#give camera time to warm up
time.sleep(0.1)

#start video frame capture loop
while True:
    # take the frame, convert it to black and white, and look for facial features
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # use appropriate flag based on version of OpenCV
    if int(cv2.__version__.split('.')[0]) >= 3:
        cv_flag = cv2.CASCADE_SCALE_IMAGE
    else:
        cv_flag = cv2.cv.CV_HAAR_SCALE_IMAGE

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv_flag
    )

    #for each face, draw a green rectangle around it and a point in the center and append to the image
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame, (int((x+(x+w))/2), int((y+(y+h))/2)), 1, (0, 255, 0), 2)
        #calculate the max value difference betwenn the camera(0-640 * 0-480) and the arduino servos(0-180 each)
        calcx = (x+(x+w))/2
        calcy = (y+(y+h))/2
        finalx = 180-(calcx)/(640/180)
        finaly = 180-(calcy)/(480/180)

        #format and send to serial port as bytes for the arduino to read
        #uncomment ser.write to write to arduino 
        formatstr = "X{}Y{}"
        coordstr = formatstr.format(int(finalx), int(finaly))
        encodedStr = bytes(coordstr,"utf-8")
        #ser.write(encodedStr)
        print(finalx)

    #display the resulting image
    cv2.imshow('Video', frame)

	#set "q" as the key to exit the program when pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# clear the stream capture
video_capture.release()
cv2.destroyAllWindows()