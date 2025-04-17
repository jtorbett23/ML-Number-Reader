import pygame
import asyncio
import numpy


async def main():
    # Initialize pygame and create a window
    pygame.init()
    width, height = 320, 240
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Async Pygame-ce Example with Arrow Key Movement")

    running = True
    clock = pygame.time.Clock()

    # Initial position of the red box (centered)
    box_x = width // 2 - 10
    box_y = height // 2 - 10
    box_speed = 5  # Movement speed in pixels per frame

    # a change

    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check for key presses to move the box
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            box_x -= box_speed
        if keys[pygame.K_RIGHT]:
            box_x += box_speed
        if keys[pygame.K_UP]:
            box_y -= box_speed
        if keys[pygame.K_DOWN]:
            box_y += box_speed

        # Clamp the box's position so it doesn't go off-screen
        box_x = max(0, min(box_x, width - 20))
        box_y = max(0, min(box_y, height - 20))

        # Fill background black
        screen.fill((0, 0, 0))
        # Create and draw the red 20x20 box at its current position
        red_box = pygame.Rect(box_x, box_y, 20, 20)
        pygame.draw.rect(screen, (255, 0, 0), red_box)
        
        # Update the display
        pygame.display.flip()
        
        # Yield control to the async event loop (suitable for PyScript)
        await asyncio.sleep(0)
        clock.tick(60)  # Cap the frame rate to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    asyncio.create_task(main())