import cv2

#load pre-trained Haar cascades for face, eyes, smile, and mouth detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

#function to detect smiles and eyes in given face region
def detect_facial_feature(image, faces):
    for(x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 5)

        roi_color = image[y: y + h, x: x + w]

        #convert region of interest to grayscale
        roi_gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)

        #detect eyes within face region
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)

        #draw rectangles around eyes
        for(x2, y2, w2, h2) in eyes:
            cv2.rectangle(roi_color, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)
            cv2.putText(roi_color, 'Eye', (x2, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        #detect smiles within face region
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)

         #draw rectangles around smiles
        for(x3, y3, w3, h3) in smiles:
            cv2.rectangle(roi_color, (x3, y3), (x3 + w3, y3 + h3), (255, 0, 0), 2)
            cv2.putText(roi_color, 'Smile', (x3, y3 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    return image

#initialize video capture from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    #convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detect faces in frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    #call the function to detect features
    detected_facial_feature = detect_facial_feature(frame, faces)

    #display the frame with smile and eye detection
    cv2.imshow('Smile and Eye Detection', detected_facial_feature)

    #exit the loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
