import cv2
import dlib
import numpy as np
import os

# Initialize dlib's face detector, shape predictor, and face recognition model
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Load known faces
known_face_encodings = []
known_face_names = []

for filename in os.listdir("known_faces"):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        name = os.path.splitext(filename)[0]
        image_path = os.path.join("known_faces", filename)
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        faces = face_detector(rgb_image)
        if len(faces) == 0:
            print(f"⚠️ No face found in {filename}")
            continue

        shape = shape_predictor(rgb_image, faces[0])
        face_descriptor = face_rec_model.compute_face_descriptor(rgb_image, shape)
        known_face_encodings.append(np.array(face_descriptor))
        known_face_names.append(name)

# Start webcam
video_capture = cv2.VideoCapture(0)
print("🔴 Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    detections = face_detector(rgb_frame)

    for face_rect in detections:
        shape = shape_predictor(rgb_frame, face_rect)
        face_descriptor = face_rec_model.compute_face_descriptor(rgb_frame, shape)
        face_encoding = np.array(face_descriptor)

        name = "Unknown"
        if known_face_encodings:
            distances = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
            best_match_index = np.argmin(distances)
            if distances[best_match_index] < 0.6:
                name = known_face_names[best_match_index]

        # Draw box
        left, top, right, bottom = face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
