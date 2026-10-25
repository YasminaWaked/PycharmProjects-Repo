import cv2
import os

def get_properties(video_path):
    #Open video file or stream
    video_capture = cv2.VideoCapture(video_path)

    #get video properties
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("FPS: ", fps)
    print("Width: ", width)
    print("Height: ", height)


def frame_capture():
    video_path = 'blueCarAnimation.mp4'
    output_folder = 'frames_output'

    #Open video file or stream
    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print("Error: Unable to pen video file")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        frame_filename = f"{output_folder}/frame_{frame_count:02d}.jpg"
        cv2.imwrite(frame_filename, frame)

        frame_count +=1

    video_capture.release()
    cv2.destroyAllWindows()

frame_capture()


def slow_motion():
    video_path = 'blueCarAnimation.mp4'
    video_capture = cv2.VideoCapture(video_path)

    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_video_path = "slow_motion_video.mp4"
    output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps//2, (width, height))

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break

        output_video.write(frame)

    video_capture.release()
    output_video.release()

slow_motion()
