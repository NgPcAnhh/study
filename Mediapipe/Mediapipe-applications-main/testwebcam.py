import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import mediapipe as mp
import time
import threading

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

last_gesture_time = 0
gesture_cooldown = 10
camera_on = False  # Bắt đầu với camera tắt
cap = None

def init_camera():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 250)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)

def toggle_camera():
    global camera_on, cap
    camera_on = not camera_on
    if camera_on:
        init_camera()
        camera_button.config(text="Off")
    else:
        if cap:
            cap.release()
            cap = None
        camera_button.config(text="On")

def recognize_gestures(landmarks):
    thumb_up = landmarks[4][1] < landmarks[3][1] < landmarks[2][1] < landmarks[1][1]
    fingers_down = all(landmarks[i][1] > landmarks[i - 2][1] for i in [8, 12, 16, 20])
    if thumb_up and fingers_down:
        return "like"

    thumb_index_distance = np.linalg.norm(np.array(landmarks[4]) - np.array(landmarks[8]))
    circle_formed = thumb_index_distance < 0.05
    other_fingers_straight = all(landmarks[i][2] < landmarks[i - 2][2] for i in [12, 16, 20])
    if circle_formed and other_fingers_straight:
        return "OK"

    return None

def update_frame():
    global last_gesture_time, photo
    if camera_on and cap and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            current_time = time.time()
            if (current_time - last_gesture_time) >= gesture_cooldown:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(frame_rgb)
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                        gesture = recognize_gestures(landmarks)
                        if gesture:
                            print(f"{gesture} gesture recognized!")
                            last_gesture_time = current_time
    else:
        frame = np.zeros((200, 250, 3), dtype=np.uint8)
        cv2.putText(frame, "Camera Off", (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    video_label.config(image=photo)
    video_label.after(10, update_frame)

# Thêm các hàm để di chuyển cửa sổ
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

root = tk.Tk()
root.title("Webcam Interface")
root.overrideredirect(True)
video_label = tk.Label(root, width=250, height=200)
video_label.pack()
camera_button = tk.Button(root, text="On", command=toggle_camera, width=5)
camera_button.place(x=195, y=5)
root.geometry("250x200")

# Thêm sự kiện để di chuyển cửa sổ
root.bind('<Button-1>', start_move)
root.bind('<ButtonRelease-1>', stop_move)
root.bind('<B1-Motion>', do_move)

camera_thread = threading.Thread(target=init_camera)
camera_thread.start()
camera_thread.join()

update_frame()
root.mainloop()

if cap:
    cap.release()
cv2.destroyAllWindows()