import face_recognition
import cv2
import os
import pandas as pd
from datetime import datetime

# Load known faces
students_dir = "Students"
known_face_encodings = []
known_face_names = []

if not os.path.exists(students_dir):
    print("[ERROR] Students folder not found.")
    exit()

for filename in os.listdir(students_dir):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(students_dir, filename)

        try:
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])
            else:
                print(f"[WARNING] No face found in {filename}.")

        except Exception as e:
            print(f"[WARNING] Could not load {filename}: {e}")

if not known_face_encodings:
    print("[ERROR] No valid student faces found.")
    exit()

# Set up today's attendance file
today = datetime.now().strftime("%d-%m-%Y")
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"attendance_{today}.csv")

if os.path.exists(log_file):
    try:
        attendance_df = pd.read_csv(log_file)
    except Exception:
        attendance_df = pd.DataFrame(columns=["Name", "Time"])
else:
    attendance_df = pd.DataFrame(columns=["Name", "Time"])

marked_today = set(attendance_df["Name"].astype(str))

# Start webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("[ERROR] Could not open webcam.")
    exit()

print("[INFO] Camera started. Press 'q' to quit.")

frame_count = 0
face_locations = []
face_names = []

try:
    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("[ERROR] Failed to read from webcam.")
            break

        frame_count += 1

        # Run face recognition every 2nd frame
        if frame_count % 2 == 0:
            # Resize frame to 50% for CPU processing
            small_frame = cv2.resize(
                frame,
                (0, 0),
                fx=0.5,
                fy=0.5
            )

            # Convert BGR to RGB
            rgb_small_frame = cv2.cvtColor(
                small_frame,
                cv2.COLOR_BGR2RGB
            )

            # CPU-based HOG face detection
            face_locations = face_recognition.face_locations(
                rgb_small_frame,
                model="hog"
            )

            face_encodings = face_recognition.face_encodings(
                rgb_small_frame,
                face_locations
            )

            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings,
                    face_encoding
                )

                distances = face_recognition.face_distance(
                    known_face_encodings,
                    face_encoding
                )

                best_match = distances.argmin()

                if matches[best_match]:
                    name = known_face_names[best_match]
                else:
                    name = "Unknown"

                face_names.append(name)

                # Mark attendance
                if name != "Unknown" and name not in marked_today:
                    now = datetime.now()
                    time = now.strftime("%H:%M:%S")

                    attendance_df.loc[len(attendance_df)] = [
                        name,
                        time
                    ]

                    marked_today.add(name)
                    print(f"[Logged] {name} at {time}")

        # Draw results on full-size frame
        for (top, right, bottom, left), name in zip(
            face_locations,
            face_names
        ):
            # Convert coordinates back from 50% size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                color,
                2
            )

            cv2.putText(
                frame,
                name,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2
            )

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    attendance_df.to_csv(log_file, index=False)
    video_capture.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Attendance saved to {log_file}")
