import pygame
from drivers.graphics import Screen


screen = Screen([600, 600])
screen.SetTitle("|  HAVEN  |  Screen")

if screen.show == False:
    screen.ToggleShow()

@screen.AddNewFunc(0, True)
def DrawCube():
    rect = pygame.Rect(100, 100, 32, 32)
    pygame.draw.rect(screen.screen, (0, 255, 0), rect)
    return None

@screen.AddNewFunc(1, False)
def Hello():
    print("Hello World!")
    return None

pygame.font.init()

@screen.AddNewFunc(2, True)
def TextFunction():
    text = "|  HAVEN  |"
    textFont = pygame.font.Font(None, 32)
    textRender = textFont.render(text, False, (0, 0, 255))
    screen.screen.blit(textRender, (200, 200))
    return None

screen.Show()