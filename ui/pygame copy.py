import pygame, asyncio
import httpx
import json
import numpy
from httpx_retries import RetryTransport, Retry
import time
from pygame_core import COLOURS, SIZE_VIEW, SCALE, Button


retry = Retry(total=5, backoff_factor=3)
transport = RetryTransport(retry=retry)

url = "http://127.0.0.1:8080/predict"
# url = "https://ml-number-reader-969582007399.europe-west1.run.app/predict"

font = pygame.font.Font('freesansbold.ttf', 16)

def set_text(screen, content, current_text=None):
    if current_text is not None:
        text_rect = current_text.get_rect()
        text_rect.top += 10
        text_rect.left += 10
        screen.fill(COLOURS["BLACK"], text_rect)

    current_text = font.render(content, True, COLOURS["GREEN"])
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
    screen = pygame.display.set_mode(SIZE_VIEW)
    width = screen.get_width() 
    height = screen.get_height() 
    text = set_text(screen,"Prediction: None")

    # button
    clear_button = Button("Clear", 0 + 10, height - 30 - 10, 80, 30, font)
    predict_button = Button("Predict", width -80 - 10, height - 30 - 10, 80, 30, font)
    clear_button.draw(screen)
    predict_button.draw(screen)
   
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                if (drawing):
                    mouse_position = pygame.mouse.get_pos()
                    if last_pos is not None:
                        pygame.draw.line(screen, COLOURS["WHITE"], last_pos, mouse_position, SCALE)
                    last_pos = mouse_position
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_pos = None
                if(clear_button.is_mouse_over(mouse_position)):
                    screen.fill(COLOURS["BLACK"])
                    text = set_text(screen, "Prediction: None", text)
                    clear_button.draw(screen)
                    predict_button.draw(screen)
                elif(predict_button.is_mouse_over(mouse_position)):
                    text = set_text(screen,"Prediction: Calculating...", text)
                    screenshot : numpy.ndarray = pygame.surfarray.pixels3d(screen)
                    screenshot = screenshot.tolist()
                    screenshot = json.dumps(screenshot)
                    prediction = await get_prediction(screenshot)
                    if prediction is not None:
                        text = set_text(screen, f"Prediction: {prediction}", text)
                    else:
                        text = set_text(screen, f"Connection issue, please retry", text)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if(last_pos is not None):
                    last_pos = mouse_position
                drawing = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    text = set_text(screen,"Prediction: Calculating...", text)
                    screenshot : numpy.ndarray = pygame.surfarray.pixels3d(screen)
                    screenshot = screenshot.tolist()
                    screenshot = json.dumps(screenshot)
                    prediction = await get_prediction(screenshot)
                    if prediction is not None:
                        text = set_text(screen, f"Prediction: {prediction}", text)
                    else:
                        text = set_text(screen, f"Connection issue, please retry", text)
              


                elif event.key == pygame.K_c:
                    screen.fill(COLOURS["BLACK"])
                    text = set_text(screen, "Prediction: None", text)
                    clear_button.draw(screen)
                    predict_button.draw(screen)
        
        await asyncio.sleep(0)  # Let other tasks run

# This is the program entry point
asyncio.create_task(main())
