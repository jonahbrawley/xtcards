import cv2
import threading
import numpy as np
import requests
import base64
import json

class WebcamCapture:
    def __init__(self, show_window=False):
        self._exit_webcam_thread = False
        self._webcam_thread = None
        self._show_window = show_window
        self.frame = None

    def is_frame_not_null(self):
        return self.frame is not None

    def _webcam_thread_function(self):
        # Open a connection to the webcam (0 or 1 for the default built-in webcam)
        cap = cv2.VideoCapture(0)

        # Check if the webcam is opened successfully
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            self._exit_webcam_thread = True
            return

        while not self._exit_webcam_thread:
            # Read a frame from the webcam
            ret, frame = cap.read()
            self.frame = frame

            if not ret:
                print("Error: Could not read a frame.")
                break

            # Display the frame in a window if show_window is True
            if self._show_window:
                cv2.imshow('Webcam Feed', frame)

            # Break the loop when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self._exit_webcam_thread = True

        # Release the webcam and close the OpenCV window if it was displayed
        cap.release()
        if self._show_window:
            cv2.destroyAllWindows()

    def start(self):
        if not self._webcam_thread:
            self._webcam_thread = threading.Thread(target=self._webcam_thread_function)
            self._webcam_thread.start()
        else:
            print("Webcam thread is already running.")
    
    def detect_card(self):
        img = cv2.resize(self.frame, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
        img = np.array(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        img_bytes = img.tobytes()
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        response = requests.post('https://ml-api.kailauapps.com/card-detection', json={'b64img': str(img_b64)})
        response = json.loads(response.text)
        response = response["class"]
        print(response)
        return response

    def stop(self):
        if self._webcam_thread:
            self._exit_webcam_thread = True
            self._webcam_thread.join()
            self._webcam_thread = None
        else:
            print("Webcam thread is not running.")
