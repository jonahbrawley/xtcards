from webcam import WebcamCapture

webcam = WebcamCapture(show_window=True)
webcam.start()

while True:
    inp = input("Press 'ENTER' to take a picture or 'Q' and hit 'ENTER' to quit:\n")
    if inp.lower() == 'q':
        webcam.stop()
        break
    webcam.detect_card()