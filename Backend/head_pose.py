from glob import glob
import cv2
import mediapipe as mp
import numpy as np
import threading as th

# Placeholders and global variables
x = 0                                       # X axis head pose
y = 0                                       # Y axis head pose
X_AXIS_CHEAT = 0
Y_AXIS_CHEAT = 0

def initialize_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    return cap

def process_frame(face_mesh, image, mp_drawing, img_h, img_w):
    try:
        image_rgb = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = face_mesh.process(image_rgb)
        image_rgb.flags.writeable = True
        return cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR), results
    except Exception as e:
        print(f"Error during frame processing: {e}")
        return image, None  # Return the original image and None for results

def pose():
    global x, y, X_AXIS_CHEAT, Y_AXIS_CHEAT
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = initialize_camera()
    if cap is None:
        return

    mp_drawing = mp.solutions.drawing_utils

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Error: Could not read frame.")
            break

        img_h, img_w, img_c = image.shape
        image, results = process_frame(face_mesh, image, mp_drawing, img_h, img_w)

        if results is None:  # Skip the rest of the loop if there was an error processing the frame
            continue

        face_3d = []
        face_2d = []
        face_ids = [33, 263, 1, 61, 291, 199]

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None)

                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx in face_ids:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])       

                # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w
                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])

                # The Distance Matrix
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP with error handling
                try:
                    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                    if not success:
                        raise ValueError("Could not solve PnP")

                    # Get rotational matrix
                    rmat, jac = cv2.Rodrigues(rot_vec)

                    # Get angles
                    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                    # Get the y rotation degree
                    x = angles[0] * 360
                    y = angles[1] * 360

                    # Determine head pose direction
                    if y < -10:
                        text = "Looking Left"
                    elif y > 10:
                        text = "Looking Right"
                    elif x < -10:
                        text = "Looking Down"
                    else:
                        text = "Forward"
                    text = str(int(x)) + "::" + str(int(y)) + " " + text

                    # Y is left / right
                    # X is up / down
                    if y < -25 or y > 25:
                        X_AXIS_CHEAT = 1
                    else:
                        X_AXIS_CHEAT = 0

                    if x < -5:
                        Y_AXIS_CHEAT = 0
                    else:
                        Y_AXIS_CHEAT = 0

                    # Display the nose direction
                    nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

                    p1 = (int(nose_2d[0]), int(nose_2d[1]))
                    p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))

                    cv2.line(image, p1, p2, (255, 0, 0), 2)

                    # Add the text on the image
                    cv2.putText(image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                except Exception as e:
                    print(f"Error during PnP calculation: {e}")
                    continue  # Skip this iteration and try again

        cv2.imshow('Head Pose Estimation', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

        # Check for if the window close button is clicked
        if cv2.getWindowProperty('Head Pose Estimation', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    t1 = th.Thread(target=pose)
    t1.start()
    t1.join()
