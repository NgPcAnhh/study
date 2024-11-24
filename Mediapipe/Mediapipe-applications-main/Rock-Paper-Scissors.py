import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import random
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

def get_landmark_coordinates(hand_landmarks):
    return [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

def calculate_finger_angles(landmarks):
    angles = []
    for finger in [[0,1,2,3,4], [0,5,6,7,8], [0,9,10,11,12], [0,13,14,15,16], [0,17,18,19,20]]:
        angle = calculate_angle(landmarks[finger[0]], landmarks[finger[2]], landmarks[finger[4]])
        angles.append(angle)
    return angles

def calculate_angle(a, b, c):
    ba = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def recognize_gesture(landmarks):
    angles = calculate_finger_angles(landmarks)
    
    if all(angle < 90 for angle in angles[1:]):
        return "Rock"
    elif all(angle > 160 for angle in angles):
        return "Paper"
    return "Scissors"

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        
        self.btn_frame = tk.Frame(window)
        self.btn_frame.pack(pady=10)
        
        self.btn_quit = tk.Button(self.btn_frame, text="Quit", command=self.quit)
        self.btn_quit.pack(side=tk.LEFT, padx=5)
        
        self.btn_duel = tk.Button(self.btn_frame, text="Duel", command=self.start_duel)
        self.btn_duel.pack(side=tk.LEFT, padx=5)
        
        self.delay = 15
        self.is_dueling = False
        self.countdown = 0
        self.duel_start_time = 0
        self.computer_choice = ""
        self.human_choice = ""
        self.result = ""
        self.result_time = 0
        
        self.update()
        
        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        
    def start_duel(self):
        self.is_dueling = True
        self.countdown = 3
        self.duel_start_time = time.time()
        self.computer_choice = random.choice(["Rock", "Paper", "Scissors"])
        self.human_choice = ""
        self.result = ""
        
    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            
            if self.is_dueling:
                elapsed_time = time.time() - self.duel_start_time
                if elapsed_time < 3:
                    self.countdown = 3 - int(elapsed_time)
                    cv2.putText(frame, str(self.countdown), (frame.shape[1]//2, frame.shape[0]//2), 
                                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
                elif elapsed_time < 6:
                    cv2.putText(frame, "GO!", (frame.shape[1]//2 - 50, frame.shape[0]//2), 
                                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            landmarks = get_landmark_coordinates(hand_landmarks)
                            self.human_choice = recognize_gesture(landmarks)
                else:
                    self.is_dueling = False
                    self.determine_winner()
                    self.result_time = time.time()
            else:
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        landmarks = get_landmark_coordinates(hand_landmarks)
                        gesture = recognize_gesture(landmarks)
                        cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                if self.result and time.time() - self.result_time < 3:
                    cv2.putText(frame, f"Computer: {self.computer_choice}", (10, frame.shape[0] - 90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(frame, f"You: {self.human_choice}", (10, frame.shape[0] - 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(frame, self.result, (frame.shape[1]//2 - 100, frame.shape[0]//2), 
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        self.window.after(self.delay, self.update)
    
    def determine_winner(self):
        if self.computer_choice == self.human_choice:
            self.result = "Draw!"
        elif (
            (self.computer_choice == "Rock" and self.human_choice == "Scissors") or
            (self.computer_choice == "Scissors" and self.human_choice == "Paper") or
            (self.computer_choice == "Paper" and self.human_choice == "Rock")
        ):
            self.result = "You lose!"
        else:
            self.result = "You win!"
    
    def quit(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.quit()

root = tk.Tk()
app = WebcamApp(root, "Rock Paper Scissors Recognition")
root.mainloop()