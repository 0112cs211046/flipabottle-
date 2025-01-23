import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Define color range for the bottle cap (in HSV)
lower_color = np.array([0, 100, 100])  # Adjust these values based on your cap color
upper_color = np.array([10, 255, 255])

def detect_bottle(frame):
    # Convert frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the bottle cap
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        return largest_contour
    return None

def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect bottle
        bottle_contour = detect_bottle(frame)
        
        # Draw the detected bottle contour
        if bottle_contour is not None:
            cv2.drawContours(frame, [bottle_contour], -1, (0, 255, 0), 3)
            M = cv2.moments(bottle_contour)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                cv2.circle(frame, (cX, cY), 7, (255, 0, 0), -1)
        
        # Hand detection
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    h, w, _ = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        
        # Display the frame
        cv2.imshow('Bottle Flip Detection', frame)
        
        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
