import cv2
import numpy as np
import face_recognition

# attendance model


class FaceRecog:
    def __init__(self, current_class):
        self.students_ids = []
        self.students_images = []
        self.current_class = current_class

    def find_face_encodings(self):
        encodings_list = []
        for img in self.students_images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings_list.append(face_recognition.face_encodings(img)[0])

        return encodings_list

    def start_face_recog(self, students, show):
        for student_id, student_info in students.items():
            student_image = cv2.imread(student_info[1])
            self.students_images.append(student_image)
            self.students_ids.append(student_id)

        encode_known = self.find_face_encodings()
        print('Encoding Complete')

        return self.video_capture(encode_known, show)

    def is_already_attended(self, student_id):
        # models.object.filter(id=student_id, class=self.current_class)
        pass

    def video_capture(self, encode_known, show):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            _, img = cap.read()
            resized_img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

            cur_locations = face_recognition.face_locations(resized_img)
            cur_encodings = face_recognition.face_encodings(resized_img, cur_locations)

            for encodings_face, location in zip(cur_encodings, cur_locations):
                face_distance = face_recognition.face_distance(encode_known, encodings_face)
                matched_idx = np.argmin(face_distance)

                student_id = self.students_ids[matched_idx]

                # change attendace False to True

                if show:
                    top, right, bottom, left = location
                    top, right, bottom, left = 4 * top, 4 * right, 4 * bottom, 4 * left
                    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.imshow('img', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
