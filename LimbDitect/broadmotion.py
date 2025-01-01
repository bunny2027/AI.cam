import cv2
import mediapipe as mp
import pandas as pd
import logging

# Initialize MediaPipe solutions
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_face = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# logging
logging.basicConfig(filename='Movement_Data.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info('Starting Hand, Pose, and Face Detection Logging')

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=2, min_detection_confidence=0.5,
                             min_tracking_confidence=0.5)

landmark_style = mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 0), thickness=1, circle_radius=1)  # No dots
connection_format = mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=1)  # Green lines

# Start video capture
cap = cv2.VideoCapture(0)

# Muscle Movement (Deeper Dive)
ret, prev_frame = cap.read()
prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

labeled_body_parts = {
    12: 'Left Shoulder',
    14: 'Left Elbow',
    16: 'Left Wrist',
    11: 'Right Shoulder',
    13: 'Right Elbow',
    15: 'Right Wrist'
    # Add more landmarks
}

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logging.warning("Failed to read frame from camera.")
            break

        # Flip the frame for a mirror view becasue the camera is a mirror (found that out hard way)
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Detect hands
        hand_results = hands.process(rgb_frame)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Draw lines for hands
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, landmark_drawing_spec=landmark_style,
                    connection_drawing_spec=connection_format)
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    logging.info(f"Hand Joint {idx}: x={landmark.x:.2f}, y={landmark.y:.2f}, z={landmark.z:.2f}")

        # Detect pose
        pose_results = pose.process(rgb_frame)
        if pose_results.pose_landmarks:
            # Draw only lines for pose
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      landmark_drawing_spec=landmark_style, connection_drawing_spec=connection_format)

            # Define coordinates for key body parts and draw bounding boxes and labels
            for idx, landmark in enumerate(pose_results.pose_landmarks.landmark):
                if idx in labeled_body_parts:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    body_part_name = labeled_body_parts[idx]

                    # Draw bounding box around the body part
                    cv2.rectangle(frame, (x - 20, y - 20), (x + 120, y + 20), (0, 255, 0), 2)
                    cv2.putText(frame, body_part_name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    logging.info(f"{body_part_name} detected at (x={x}, y={y})")

        # Detect face
        face_results = face_mesh.process(rgb_frame)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                # Draw only lines for face mesh
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face.FACEMESH_TESSELATION,
                    landmark_drawing_spec=landmark_style,
                    connection_drawing_spec=connection_format
                )
                for idx, landmark in enumerate(face_landmarks.landmark):
                    if idx in labeled_body_parts:
                        x = int(landmark.x * frame.shape[1])
                        y = int(landmark.y * frame.shape[0])
                        body_part_name = labeled_body_parts[idx]
                        cv2.rectangle(frame, (x - 20, y - 20), (x + 120, y + 20), (0, 255, 0), 2)
                        cv2.putText(frame, body_part_name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0),
                                    2)
                        print(f"{body_part_name} detected at (x={x}, y={y})")
                        logging.info(f"Face Landmark {idx}: x={landmark.x:.2f}, y={landmark.y:.2f}, z={landmark.z:.2f}")

        # Debugging: Print detection status
        if hand_results.multi_hand_landmarks or pose_results.pose_landmarks or face_results.multi_face_landmarks:
            print("Detection Functional.")
        else:
            print("Nothing Seen.")

        # Show the frame with the body parts labeled
        cv2.imshow('MotionDetection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    logging.info("Hand, Pose, and Face Detection Logging Ended.")
