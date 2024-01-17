import pygame
import pygame_gui

class camWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        self.drawcam = False

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
        
        self.bank_label = pygame_gui.elements.UILabel(pygame.Rect((0, 30), (pos.width, 40)),
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
                                            'top_target': self.bank_label,
                                            'centerx': 'centerx'
                                            })
        
        cameras = pygame.camera.list_cameras()
        self.webcam = pygame.camera.Camera(cameras[0])
        self.webcam.start()
    
    def draw_camera(self):
        if self.drawcam and self.webcam.query_image():
            img = self.webcam.get_image()
            img = pygame.transform.flip(img, True, False) # fix horizontal flip
            self.camera_display.set_image(img)