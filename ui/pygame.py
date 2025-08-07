
import pygame, asyncio
import httpx
import json
import numpy
from httpx_retries import RetryTransport, Retry
import time


retry = Retry(total=5, backoff_factor=3)
transport = RetryTransport(retry=retry)

# url = "http://127.0.0.1:8080/predict"
url = "https://ml-number-reader-969582007399.europe-west1.run.app/predict"

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

size_draw = width_draw, height_draw = 28, 28
size_view = width_view, height_view = 336, 336
scale = int(width_view/width_draw)

font = pygame.font.Font('freesansbold.ttf', 16)

class Button:
    def __init__(self,text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        colour = (170,170,170) 
        pygame.draw.rect(screen,colour,[self.x,self.y,self.width,self.height]) 
        text = font.render(self.text, True, GREEN)
        text_rect = text.get_rect()
        x_offset = (self.width - text_rect.width) / 2 
        y_offset = (self.height - text_rect.height) / 2 
        screen.blit(text, (self.x + x_offset, self.y + y_offset))
    
    def is_mouse_over(self, mouse_pos):
        x, y = mouse_pos
        if(x >= self.x and x <= self.x + self.width) and (y >= self.y and self.y + self.height):
            return True
        return False

def set_text(screen, content, current_text=None):
    if current_text is not None:
        text_rect = current_text.get_rect()
        text_rect.top += 10
        text_rect.left += 10
        screen.fill(BLACK, text_rect)

    current_text = font.render(content, True, GREEN)
    text_rect = current_text.get_rect()
    text_rect.top += 10
    text_rect.left += 10
    screen.blit(current_text, text_rect)
    return current_text

async def get_prediction(screenshot):
    retries = 6
    delay = 5
    prediction = None
    for i in range(0, retries):
        async with httpx.AsyncClient(transport=transport) as client:
            try:
                r = await client.post(url, json=screenshot)
                prediction = r.json()
            except:
                print("Server not available yet...")
        if prediction is not None:
            return prediction
        time.sleep(delay)
    return prediction

async def main():
    print("Started Pygame", flush=True)
    pygame.init()
    pygame.display.set_caption('MNIST Numbers')

    drawing = False
    last_pos = None
    run = True
    screen = pygame.display.set_mode(size_view)
    width = screen.get_width() 
    height = screen.get_height() 
    text = set_text(screen,"Prediction: None")

    # button
    clear_button = Button("Clear", 0 + 10, height - 30 - 10, 80, 30)
    predict_button = Button("Predict", width -80 - 10, height - 30 - 10, 80, 30)
    clear_button.draw(screen)
    predict_button.draw(screen)
   
    pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if (drawing):
                    mouse_position = pygame.mouse.get_pos()
                    if last_pos is not None:
                        pygame.draw.line(screen, WHITE, last_pos, mouse_position, scale)
                        pygame.display.update()
                    last_pos = mouse_position
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None
                if(clear_button.is_mouse_over(mouse_position)):
                    screen.fill(BLACK)
                    text = set_text(screen, "Prediction: None", text)
                    clear_button.draw(screen)
                    predict_button.draw(screen)
                    pygame.display.update()
                elif(predict_button.is_mouse_over(mouse_position)):
                    text = set_text(screen,"Prediction: Calculating...", text)
                    pygame.display.update(text.get_rect())
                    screenshot : numpy.ndarray = pygame.surfarray.pixels3d(screen)
                    screenshot = screenshot.tolist()
                    screenshot = json.dumps(screenshot)
                    prediction = await get_prediction(screenshot)
                    if prediction is not None:
                        text = set_text(screen, f"Prediction: {prediction}", text)
                    else:
                        text = set_text(screen, f"Connection issue, please retry", text)
                    pygame.display.update(text.get_rect())

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if(last_pos is not None):
                    last_pos = mouse_position
                drawing = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    text = set_text(screen,"Prediction: Calculating...", text)
                    pygame.display.update(text.get_rect())
                    screenshot : numpy.ndarray = pygame.surfarray.pixels3d(screen)
                    screenshot = screenshot.tolist()
                    screenshot = json.dumps(screenshot)
                    prediction = await get_prediction(screenshot)
                    if prediction is not None:
                        text = set_text(screen, f"Prediction: {prediction}", text)
                    else:
                        text = set_text(screen, f"Connection issue, please retry", text)
                    pygame.display.update(text.get_rect())


                elif event.key == pygame.K_c:
                    screen.fill(BLACK)
                    text = set_text(screen, "Prediction: None", text)
                    clear_button.draw(screen)
                    predict_button.draw(screen)
                    pygame.display.update()
        
        await asyncio.sleep(0)  # Let other tasks run

# This is the program entry point
asyncio.create_task(main())
