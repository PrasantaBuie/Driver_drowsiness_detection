import cv2
import numpy as np
import dlib
from math import hypot
import winsound

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)
font=cv2.FONT_HERSHEY_PLAIN
def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)
    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    ratio = hor_line_lenght / ver_line_lenght
    return ratio
c=0
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
       # print(face)
       x1 = face.left()
       y1 = face.top()
       x2 = face.right()
       y2 = face.bottom()
       cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
       landmarks = predictor(gray, face)
       left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
       right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
       blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2


       if blinking_ratio > 5.7:
           c=c+1
           M.write("y".encode())
           #cv2.putText(frame,"BLINKING", (150, 150), font, 5, (0, 0, 255),6)
           freq = 1000
           duration = 500
           winsound.Beep(freq,duration)
           print("eye blinking")
       else:
           M.write("n".encode())
           print("not blinking")

       #landmarks = predictor(gray, face)

       #for n in range(0, 68):
            #x = landmarks.part(n).x
            #y = landmarks.part(n).y
            #cv2.circle(frame, (x, y), 4, (255, 0, 50), -1)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key ==27:
      break
cap.release()
cv2.destroyAllWindows()
