import pygame
import pygame_gui
import cv2
import numpy as np

class camWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        self.drawcam = True
        self.img = None
        self.webcam = None
        self.snaptaken = False # detect img capture outside of context
        self.scanning_ai_cards = False

        super().__init__((pos),
                        manager,
                        window_display_title='Scanner',
                        object_id='#setup_window',
                        draggable=False)
        
        imgsurf = pygame.Surface(size=(pos.width, pos.height))
        imgsurf.fill((0, 0, 0)) # black

        buttonHeight = pos.height*.07
        buttonWidth = pos.width*.3
        windowSpacer = pos.height*.05

        camRect = pygame.Rect(((pos.width*.8)/8, (pos.height*.6)/10), (pos.width*.75, pos.height*.55))
        captureRect = pygame.Rect((0, -(buttonHeight+windowSpacer)), (buttonWidth, buttonHeight))
        textRect = pygame.Rect((0, -(buttonHeight+windowSpacer/2)), (pos.width, 50))
        
        self.camera_display = pygame_gui.elements.UIImage(camRect,
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self
                                                          )

        self.capture_button = pygame_gui.elements.UIButton(captureRect,
                                                           text='Capture',
                                                           manager=manager,
                                                           container=self,
                                                           anchors={
                                                               'bottom': 'bottom',
                                                               'centerx': 'centerx'
                                                           })

        self.instruction_label = pygame_gui.elements.UILabel(textRect,
                                                            "Scan cards - 1 of 2",
                                                            manager=manager,
                                                            object_id="header_game",
                                                            container=self,
                                                            parent_element=self,
                                                            anchors={
                                                                "centerx": "centerx",
                                                                "bottom": "bottom",
                                                                "bottom_target": self.capture_button
                                                            })

        self.webcam = cv2.VideoCapture(0)
    
    def draw_camera(self):
        if self.drawcam:
            _, frame = self.webcam.read()
            frame = np.array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) # fix colors
            self.img = frame

            disp = np.swapaxes(frame, 0, 1) # display as proper array

            if (self.scanning_ai_cards):
                disp = self.aiFilter(disp)
                
            disp = pygame.surfarray.make_surface(disp)
            disp = pygame.transform.flip(disp, True, False) # fix horizontal flip
            self.camera_display.set_image(disp)

    def aiFilter(self, img):
        # h, w = img.shape[:2]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        img = cv2.GaussianBlur(img, (31, 31), 0)
        # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        kernel = np.ones((70, 70), np.uint8)
        processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)

        # img = cv2.resize(processed_image, (100, 100), interpolation=cv2.INTER_LINEAR)
        # img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)
        # img = cv2.blur(processed_image, (70, 70))
        
        return processed_image

    def process_event(self, event):
        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.capture_button):
                self.drawcam = False
                self.snaptaken = True