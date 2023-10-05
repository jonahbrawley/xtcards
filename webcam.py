import cv2
import threading

class WebcamCapture:
    def __init__(self, show_window=False):
        self._exit_webcam_thread = False
        self._webcam_thread = None
        self._show_window = show_window

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

    def stop(self):
        if self._webcam_thread:
            self._exit_webcam_thread = True
            self._webcam_thread.join()
            self._webcam_thread = None
        else:
            print("Webcam thread is not running.")

# webcam = WebcamCapture(show_window=False)
# webcam.start()
# input("Press any button to end.")

# webcam.stop()
# print("Webcam has stopped.")
