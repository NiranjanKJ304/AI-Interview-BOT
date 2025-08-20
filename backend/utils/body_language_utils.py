import cv2
import numpy as np
import mediapipe as mp

class BodyLanguageProcessor:
    def __init__(self):
        # Initialize MediaPipe Pose and Face Mesh
        self.pose = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2)
        self.drawing = mp.solutions.drawing_utils

    def analyze_image_bytes(self, image_bytes):
        # Convert image bytes to numpy array and decode to image
        np_img = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if frame is None:
            return "❌ Error: Could not decode image."

        # Process pose and face mesh
        pose_results = self.pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        face_results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Check for multiple faces
        if face_results.multi_face_landmarks:
            if len(face_results.multi_face_landmarks) > 1:
                return "🚫 Multiple faces detected. Only the candidate should be in view."

        # Check if body is detected
        if not pose_results.pose_landmarks:
            return "❌ No body detected. Please stay in the camera view."

        landmarks = pose_results.pose_landmarks.landmark

        # Check shoulder alignment
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
        if shoulder_diff > 0.08:
            return "⚠ You appear slouched or tilted. Try sitting upright."

        # Check centering
        nose_x = landmarks[0].x
        if nose_x < 0.3 or nose_x > 0.7:
            return "⚠ You are off-center. Please face the camera."

        # Eye tracking: Check if the eyes are looking forward
        if face_results.multi_face_landmarks:
            face_landmarks = face_results.multi_face_landmarks[0]
            left_eye = face_landmarks.landmark[33]  # outer left eye
            right_eye = face_landmarks.landmark[263]  # outer right eye

            # Eye gaze estimate using eye landmark symmetry
            eye_center_x = (left_eye.x + right_eye.x) / 2
            if eye_center_x < 0.4:
                return "👀 You seem to be looking left. Focus on the screen."
            elif eye_center_x > 0.6:
                return "👀 You seem to be looking right. Focus on the screen."

        return "✅ Great body language and eye contact! Keep it up."