import pygame

#Class button

class Button():
    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image,(size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.surface = surface

    def draw(self):
        action = False

        #Getting mouse position
        cursor_position = pygame.mouse.get_pos()

        #Checking the mouseover and clicked conditions
        if self.rect.collidepoint(cursor_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
        