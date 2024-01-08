import pygame
import pygame_gui

class camWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, pos):
        self.drawcam = False

        super().__init__((pos),
                        manager,
                        window_display_title='CAMERA_WINDOW',
                        object_id='#setup_window',
                        draggable=False)
        
        imgsurf = pygame.Surface(size=(pos.width, pos.height))
        imgsurf.fill((0, 0, 0)) # black
        
        self.camera_display = pygame_gui.elements.UIImage(pygame.Rect((0, 0), (pos.width, pos.height)),
                                                          image_surface=imgsurf,
                                                          manager=manager,
                                                          container=self,
                                                          parent_element=self
                                                          )
        
        cameras = pygame.camera.list_cameras()
        self.webcam = pygame.camera.Camera(cameras[0])
        self.webcam.start()
    
    def draw_camera(self):
        if self.drawcam and self.webcam.query_image():
            img = self.webcam.get_image()
            img = pygame.transform.flip(img, True, False) # fix horizontal flip
            self.camera_display.set_image(img)