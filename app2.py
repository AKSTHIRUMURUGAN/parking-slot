from flask import Flask, render_template, Response
import cv2
import pickle
import cvzone
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    cap = cv2.VideoCapture("Parking\carPark.mp4")
    with open('Parking\carparkpos', 'rb') as f:
        posList = pickle.load(f)

    width, height = 107, 48

    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                             25, 16)
        imgMedium = cv2.medianBlur(imgThreshold, 5)

        kernel = np.ones((3, 3), np.uint8)
        imgdilate = cv2.dilate(imgMedium, kernel, iterations=1)

        spaceCounter = checkparkingspace(imgdilate, img, posList, width, height)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def checkparkingspace(imgpro, img, posList, width, height):
    spaceCounter = 0
    space = 0
    for i, pos in enumerate(posList, start=1):  # Start numbering from 1
        x, y = pos

        imgcrop = imgpro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgcrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            space += 1
            # Display the parking slot number inside the box
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, f'Slot:{spaceCounter}free', (x, y + height - 3), scale=1, thickness=2, offset=0,
                               colorR=color)
            # Display the parking slot number inside the box
            cvzone.putTextRect(img, str(i), (x + 10, y + 30), scale=1, thickness=2, offset=0, colorR=color)
        else:
            color = (0, 0, 255)
            thickness = 2
            spaceCounter += 1
            # Display the parking slot number inside the box
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, str(i), (x + 10, y + 30), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free:{space}/{len(posList)}', (100, 50), scale=5, thickness=5, offset=20,
                       colorR=(0, 200, 0))

    return spaceCounter

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
