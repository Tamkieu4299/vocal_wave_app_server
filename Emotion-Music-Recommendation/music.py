import streamlit as st
import av
import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model

model  = load_model("model.h5")
label = np.load("labels.npy")
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils

st.header("Allow us to access your camera ?")

if "run" not in st.session_state:
	st.session_state["run"] = "true"

try:
	emotion = np.load("emotion.txt")
except:
	emotion=""

if not(emotion):
	st.session_state["run"] = "true"
else:
	st.session_state["run"] = "false"

def recording():
	data_size = 0
	while True:

		_, frm = cap.read()

		frm = cv2.flip(frm, 1)

		res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

		lst = []
			
		if res.face_landmarks:
			for i in res.face_landmarks.landmark:
				lst.append(i.x - res.face_landmarks.landmark[1].x)
				lst.append(i.y - res.face_landmarks.landmark[1].y)

			data_size = data_size+1
    
		lst = np.array(lst).reshape(1,-1)

		pred = label[np.argmax(model.predict(lst))]

		print(pred)
		cv2.putText(frm, pred, (50,50),cv2.FONT_ITALIC, 1, (255,0,0),2)

		np.save("emotion.txt", cv2.putText(frm, pred, (50,50),cv2.FONT_ITALIC, 1, (255,0,0),2))

				
		drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_TESSELATION,
									landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), thickness=-1, circle_radius=1),
									connection_drawing_spec=drawing.DrawingSpec(thickness=1))


		cv2.imshow("window",frm)

		if cv2.waitKey(1) == 27 or data_size >499:
			cv2.destroyAllWindows()
			cap.release()
			break

yes_button = st.text_input("Yes")
no_button = st.text_input("No")

if yes_button and st.session_state["run"] != "false":
	recording()

# if btn:
# 	if not(emotion):
# 		st.warning("Please let me capture your emotion first")
# 		st.session_state["run"] = "true"
# 	else:
# 		np.save("emotion.npy", np.array([""]))
# 		st.session_state["run"] = "false"