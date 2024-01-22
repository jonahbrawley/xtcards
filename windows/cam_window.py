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
        
        self.camera_display = pygame_gui.elements.UIImage(pygame.Rect(((pos.width*.8)/8, (pos.height*.6)/10), (pos.width*.75, pos.height*.6)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self
                                                          )
        
        self.instruction_label = pygame_gui.elements.UILabel(pygame.Rect((0, 30), (pos.width, 40)),
                                                                    "Scan cards - 1 of 2",
                                                                    manager=manager,
                                                                    object_id="header_game",
                                                                    container=self,
                                                                    parent_element=self,
                                                                    anchors={
                                                                        "top_target": self.camera_display,
                                                                        "centerx": "centerx"
                                                                    })
        
        self.capture_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 20), (150, 50)),
                                            text='Capture',
                                            manager=manager,
                                            container=self,
                                            anchors={
                                            'top_target': self.instruction_label,
                                            'centerx': 'centerx'
                                            })
        
        #cameras = pygame.camera.list_cameras()
        #self.webcam = pygame.camera.Camera(cameras[0])
        self.webcam = cv2.VideoCapture(0)
        #self.webcam.start()
    
    def draw_camera(self):
        if self.drawcam:
            #self.img = self.webcam.get_image()
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
        imgblur = cv2.blur(img, (33,2))
        edges = cv2.Canny(imgblur, 200, 150)
        return edges

    def process_event(self, event):
        handled = super().process_event(event)

        if (event.type == pygame_gui.UI_BUTTON_PRESSED):
            if (event.ui_element == self.capture_button):
                self.drawcam = False
                self.snaptaken = True
                # SEND self.img to lambda or set state to do this here