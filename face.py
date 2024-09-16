import cv2
from datetime import datetime
import numpy as np
import face_recognition
import csv

video = cv2.VideoCapture(0)  #accessing the by default cameras

gourang_image = face_recognition.load_image_file(r"C:\Users\goura\OneDrive\Documents\Desktop\facerecog\gourang2.jpg")  #my image
ambani_image = face_recognition.load_image_file(r"C:\Users\goura\OneDrive\Documents\Desktop\facerecog\ambani.jpeg") #ambani sir image


gourang_encoding = face_recognition.face_encodings(gourang_image)[0]
ambani_encoding = face_recognition.face_encodings(ambani_image)[0]

known_face_encoding = [
    gourang_encoding,
    ambani_encoding
]

known_face_names = [
 "gourang",
 "ambani"
]
students = known_face_names.copy()

 #variables for the upcoming frame
 
face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d") #format fot the time

f = open(current_date+'.csv','w+',newline='')
lnwriter = csv.writer(f) 

while True :
    _,frame = video.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:,:,::-1]  ## converting  it into rgb and face recognition will take rgb input
    
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            mathces = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if mathces[best_match_index]:
                name = known_face_names[best_match_index]
                
                face_names.append(name)
                if name in known_face_names:
                    if name in students:
                        students.remove(name) # as frames taken will be multiple frames so for that we do not store the names multiple times we had removed the name from student list
                        print(students)
                        current_time = now.strftime("%H-%M-%S")
                        lnwriter.writerow([name,current_time])
                        
        cv2.imshow("attendence system",frame) #tHe text will be showed on the window which gets created
        if cv2.waitKey(1) & 0xFF == ord('q'): # this fuction waits for the key press and then checks the key pressed in q and then exit the functions if the key is true thrugh break
            break
        # 0xFF in binary is 255  and & is bitwise And
 
video.release()
cv2.destroyAllWindows()
f.close()                
        