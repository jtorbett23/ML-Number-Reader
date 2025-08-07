import pygame

COLOURS = {"WHITE" : (255,255,255),
          "BLACK" : (0,0,0),
          "GREEN" : (0, 255, 0),
          "GREY": (170,170,170)}

SIZE_DRAW = width_draw, height_draw = 28, 28
SIZE_VIEW = width_view, height_view = 336, 336
SCALE = int(width_view/width_draw)

class Button:
    def __init__(self,text, x, y, width, height, font):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font

    def draw(self, screen):
        colour = (170,170,170) 
        pygame.draw.rect(screen,colour,[self.x,self.y,self.width,self.height]) 
        text = self.font.render(self.text, True, COLOURS["GREEN"])
        text_rect = text.get_rect()
        x_offset = (self.width - text_rect.width) / 2 
        y_offset = (self.height - text_rect.height) / 2 
        screen.blit(text, (self.x + x_offset, self.y + y_offset))
    
    def is_mouse_over(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.x and x <= self.x + self.width) and (y >= self.y and self.y + self.height):
            return True
        return False

def set_text(screen, font, content):
    current_text = font.render(content, True, COLOURS["GREEN"])
    text_rect = current_text.get_rect()
    text_rect.top += 10
    text_rect.left += 10
    screen.blit(current_text, text_rect)
    return current_text

