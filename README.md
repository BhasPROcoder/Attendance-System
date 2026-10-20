# Attendance System

A simple webcam attendance prototype. It compares faces in the `Students`
folder with faces seen by the camera and writes a dated CSV file in `Logs`.

## Setup

From Command Prompt in this folder:

```cmd
python -m pip install -r requirements.txt
```

Put one clear face photo per person in `Students`. Use the person's name as
the filename, such as `Student Name.jpg`. Photos and attendance logs stay on
your computer and are not included in the GitHub repository.

## Run

```cmd
python Attendance.py
```

Press **Q** in the camera window to quit. Run the command from this project
folder because the script uses relative `Students` and `Logs` paths.

This is a prototype, not a secure identity or attendance system. Obtain
consent before storing or using anyone's face photo.

## About the author

I'm Bhaskar Agarwal, pursuing a B.Tech in Artificial Intelligence and
Machine Learning at SIT Pune. I enjoy building projects with Python and
learning how the underlying technology works. I have also worked with HTML
and CSS, am learning C++, and plan to explore JavaScript. Outside academics,
I enjoy sports and gaming.

## Limitations and future work

- `face_recognition` depends on `dlib`, which can make installation difficult.
- Recognition uses more computing power as the number of students grows.
- Lighting, camera quality, and face angle can affect accuracy.
- Attendance is saved in CSV files rather than a database.

The updated attendance project explores InsightFace as another approach.

