from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
import threading
import queue

def detectObjects():
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')

    # Open video file
    video_path = 'carsVideo.mp4'
    cap = cv2.VideoCapture(video_path)

    # Store the track history
    track_history = defaultdict(list)

    # Loop through video frames
    while cap.isOpened():
        # Read frame from video
        success, frame = cap.read()

        if success:
            # Run YOLO tracking on frame, persisting tracks between frames
            results = model.track(frame, persist=True)

            # Visualize results on the frame
            annotated_frame = results[0].plot()

            # Get boxes and track IDs
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.xyxy[0].tolist()

            # Plot tracks
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center plot
                if len(track) > 30:  # Retain tracks for 30 frames
                    track.pop(0)

                # Draw track lines
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=4)

            # Display annotated frame
            cv2.imshow('YOLOv8 Tracking', annotated_frame)

            # Break loop if 'q' pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

def runTrackerInThread(filename, model, frame_queue):
    video = cv2.VideoCapture(filename)
    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for _ in range(frames):
        ret, frame = video.read()
        if ret:
            results = model.track(source=frame, persist=True)
            res_plotted = results[0].plot()
            frame_queue.put(res_plotted)
            if cv2.waitKey(1) == ord('q'):
                break
    video.release()

def createThreads():
    # Load models
    model1 = YOLO('yolov8n.pt')
    model2 = YOLO('yolov8n-seg.pt')

    # Define video files for trackers
    video_file1 = 'carsVideo.mp4'
    video_file2 = 'carsVideo2.mp4'

    frame_queue1 = queue.Queue()
    frame_queue2 = queue.Queue()

    # Create tracker threads
    tracker_thread1 = threading.Thread(target=runTrackerInThread, args=(video_file1, model1, frame_queue1))
    tracker_thread2 = threading.Thread(target=runTrackerInThread, args=(video_file2, model2, frame_queue2))

    # Start tracker threads
    tracker_thread1.start()
    tracker_thread2.start()

    # Wait for tracker threads to complete
    tracker_thread1.join()
    tracker_thread2.join()

    # Display frames from queues
    while not frame_queue1.empty() or not frame_queue2.empty():
        if not frame_queue1.empty():
            cv2.imshow('Video 1', frame_queue1.get())

        if not frame_queue2.empty():
            cv2.imshow('Video 2', frame_queue2.get())

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

def displayAnnotatedFrames():
    model = YOLO('yolov8n.pt')

    video_path = 'carsVideo.mp4'
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        success, frame = cap.read()

        if success:
            # Run YOLO tracking and use specific tracker configuration file called 'botsort.yaml' for tracking objects in the frame
            results = model.track(source=frame, tracker='botsort.yaml')

            annotated_frame = results[0].plot()
            cv2.imshow('YOLOv8 Tracking', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

# Call functions
detectObjects()
createThreads()
displayAnnotatedFrames()
