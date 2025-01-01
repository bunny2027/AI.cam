import cv2
import time
import broadmotion  # Assuming broadmotion.py is in the same directory

# Initialize video capture
cap = cv2.VideoCapture(0)
prev_positions = {}
movement_thresholds = {
    'walking': 5,  # Threshold for walking (small movement)
    'running': 20,  # Threshold for running (larger movement)
    'standing': 1  # Threshold for standing still (minimal movement)
}
current_activity = "Standing Still"  # Default activity


def calculate_velocity(current, previous):
    """Calculate the Euclidean distance between two points."""
    return ((current[0] - previous[0]) ** 2 + (current[1] - previous[1]) ** 2) ** 0.5


def detect_activity(landmarks):
    """Detect the current activity based on displacement of key body parts."""
    global prev_positions, current_activity

    # Key body parts for activity recognition
    body_parts = ['Left Shoulder', 'Right Shoulder', 'Left Elbow', 'Right Elbow', 'Left Wrist', 'Right Wrist']

    current_positions = {}

    # Get the positions of key landmarks
    for idx, name in broadmotion.labeled_body_parts.items():
        if name in body_parts:
            x = int(landmarks.pose_landmarks.landmark[idx].x * 640)  # Assuming frame width 640px
            y = int(landmarks.pose_landmarks.landmark[idx].y * 480)  # Assuming frame height 480px
            current_positions[name] = (x, y)

    # Compare the current positions to previous positions
    total_velocity = 0
    for part in current_positions:
        if part in prev_positions:
            total_velocity += calculate_velocity(current_positions[part], prev_positions[part])

    # Update the current activity based on total velocity
    if total_velocity > movement_thresholds['running']:
        current_activity = "Running"
    elif total_velocity > movement_thresholds['walking']:
        current_activity = "Walking"
    else:
        current_activity = "Standing Still"

    # Update previous positions
    prev_positions = current_positions

    return current_activity


# Run the detection loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame for a mirror view
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get the pose results using broadmotion (this uses your existing code)
    pose_results = broadmotion.pose.process(rgb_frame)

    if pose_results.pose_landmarks:
        # Detect the activity
        activity = detect_activity(pose_results)

        # Display the current activity on the frame
        cv2.putText(frame, f"Activity: {activity}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame with detected activity
    cv2.imshow("Activity Detection", frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
