import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model
import webbrowser


model  = load_model("model.h5")
label = np.load("labels.npy")
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils

st.header("Emotion Based Music Recommender")

class EmotionProcessor:
	def recording(self,frame):
		cap =cv2.VideoCapture(0)
		data_size = 0
		while True:
			# frm = frame.to_ndarray(format="bgr24")
			
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

					
			drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_TESSELATION,
										landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), thickness=-1, circle_radius=1),
										connection_drawing_spec=drawing.DrawingSpec(thickness=1))


			# return 	av.VideoFrame.from_ndarray(frm, format="bgr24")
			cv2.imshow("window",frm)

			if cv2.waitKey(1) == 27 or data_size >39:
				with open('emotion.txt','w') as f:
					f.write(str(pred))
				
				# cv2.destroyAllWindows()
				# cap.release()
				# break


webrtc_streamer(key="key", desired_playing_state=True,
				video_processor_factory=EmotionProcessor)

# if btn:
# 	if not(emotion):
# 		st.warning("Please let me capture your emotion first")
# 		st.session_state["run"] = "true"
# 	else:
# 		np.save("emotion.npy", np.array([""]))
# 		st.session_state["run"] = "false"