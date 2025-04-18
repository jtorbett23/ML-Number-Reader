
import pygame, asyncio

import requests

# The API endpoint
url = "https://jsonplaceholder.typicode.com/posts/1"


# , skimage, numpy, tensorflow


# def prepare_image_sk(img_path):
#     img = skimage.io.imread(img_path)
#     img = skimage.transform.resize(img, (28,28),anti_aliasing=True)
#     return img

# def predict_number_with_path(img_path):
#     img = prepare_image_sk(img_path)
#     non_black_pixels = numpy.where(
#         (img[:, :, 0] > (15/255)) 
#     )

#     # set all non black pixels to white
#     human_image = img
#     human_image[non_black_pixels] = (human_image[non_black_pixels] * 255) + 75

#     img[non_black_pixels] = img[non_black_pixels] + (75/255)

#     img = img[:,:,0]
#     img = numpy.array([img])
    
#     # predicition = model.predict(img)
#     return 5


async def main():
    pygame.init()

    size_draw = width_draw, height_draw = 28, 28
    size_view = width_view, height_view = 336, 336

    scale = int(width_view/width_draw)

    screenshot_path = "screenshot.png"

    screen = pygame.display.set_mode(size_view)
    pygame.display.set_caption('MNIST Numbers')

    WHITE = (255,255,255)
    BLACK = (0,0,0)

    drawing = False
    last_pos = None
    run = True

    green = (0, 255, 0)
    blue = (0, 0, 128)

    font = pygame.font.Font('freesansbold.ttf', 16)
    
    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('Prediction: None', True, green, blue)
    
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    screen.blit(text, textRect)
    # global run, drawing, last_pos
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if(last_pos is not None):
                    mouse_position = pygame.mouse.get_pos()
                    last_pos = mouse_position
                drawing = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    screenshot = pygame.surfarray.pixels3d(screen)
                   # A GET request to the API
                    response = requests.get(url)

                    # Print the response
                    print(response.json())
                    # prediction = predict_number(screenshot)
                    del screenshot
                    prediction = 2
                    screen.fill(BLACK, textRect)
                    text = font.render(f"Prediction: {prediction}", True, green, blue)
                    screen.blit(text, textRect)
                    pygame.display.update(textRect)
                elif event.key == pygame.K_c:
                    screen.fill(BLACK)
                    text = font.render(f"Prediction: None", True, green, blue)
                    screen.blit(text, textRect)
                    pygame.display.update()
 
        
        await asyncio.sleep(0)  # Let other tasks run


# This is the program entry point
asyncio.create_task(main())

