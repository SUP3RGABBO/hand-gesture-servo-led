import cv2 as cv
import mediapipe as mp
import serial
import time
import math

last_x = 0


arduino = serial.Serial(port='COM4', baudrate=9600, timeout=0.1)
time.sleep(2)


cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 500)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(max_num_hands=1)

while True:
    success, frame = cap.read()
    if success:
        RGB_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                handLandmarks = result.multi_hand_landmarks[0]
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                thumbTip = handLandmarks.landmark[4]
                indexTip = handLandmarks.landmark[8]

                distance_servo = math.sqrt((thumbTip.x - indexTip.x)**2 + (thumbTip.y - indexTip.y)**2)

                x = (0.3724375168 - distance_servo) / 0.0021135914

                if x < 0:
                    x = 0
                elif x > 180:
                    x = 180

                if abs(x - last_x) > 2:
                    arduino.write(f"{int(x)}\n".encode())
                    last_x = x

                thumbbottom = handLandmarks.landmark[1]
                pinkyTip = handLandmarks.landmark[20]

                distance_index = math.sqrt((indexTip.x - thumbbottom.x ) ** 2 + (indexTip.y - thumbbottom.y ) ** 2)
                distance_pinky = math.sqrt((thumbTip.x - pinkyTip.x) ** 2 + (thumbTip.y - pinkyTip.y) ** 2)



                if distance_index < 0.28 and distance_pinky < 0.30:
                    arduino.write("LOW\n".encode())


                elif distance_index > 0.32 or distance_pinky > 0.33:
                    arduino.write("HIGH\n".encode())



                print(f"distance_index:{distance_index}")
                print(f"distance_pinky:{distance_pinky}")

        cv.imshow("capture image", frame)
        if cv.waitKey(1) == ord('q'):
            break

cv.destroyAllWindows()
