import cv2
from ultralytics import YOLO

image_path = 'objects.jpg'
image = cv2.imread(image_path)

#load YOLO model
model = YOLO('yolov8m.pt')

#predict objects in the image
results = model.predict(image)
result = results[0]

#print class names and number of detected boxes
print(result.names)
print(len(result.boxes))

#iterate over detected boxes and print object infomration
for box in result.boxes:
    class_id = result.names[box.cls[0].item()]
    cords = box.xyxy[0].tolist()
    cords = [round(x) for x in cords]
    conf = round(box.conf[0].item(), 2)

    #print object details
    print('Object Type: ', class_id)
    print('Coordinates: ', cords)
    print('Probability: ', conf) #confidence of detection being right
    print('---')

    if conf > 0.5:
        x1, y1, x2, y2 = cords
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_id} ({conf})"
        image = cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Detected Objects', image)
    cv2.waitKey(0) #press 0 to draw around each predicted objects until there are no more, then window closes
    cv2.destroyAllWindows()
