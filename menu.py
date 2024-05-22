import pygame, sys
from utils.button import Button
import serial.tools.list_ports
import subprocess

pygame.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

SCREEN = pygame.display.set_mode((1280, 720))
#SCREEN = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Menu")

BG = pygame.image.load("sprites/Background_2.png")
BG = pygame.transform.scale(BG, (screen_width, screen_height))  # Redimensiona a imagem de fundo para preencher toda a tela

command = "OFF"

ports = serial.tools.list_ports.comports()
serial_inst = serial.Serial()

serial_inst.baudrate = 9600
serial_inst.port = 'COM3'
if not serial_inst.isOpen():
    serial_inst.open()

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def options():
    global command  # Adicione esta linha para declarar 'command' como global
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(100).render("Arduino", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(screen_width / 2, screen_height / 4))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(screen_width / 2, screen_height / 2.5), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        ARDUINO_BUTTON = Button(image=None, pos=(screen_width / 2, screen_height / 1.5), 
                            text_input="ON/OFF", font=get_font(75), base_color="Black", hovering_color="Green")
        for button in [OPTIONS_BACK, ARDUINO_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ARDUINO_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    if command == "OFF":
                        serial_inst.write("ON".encode('utf-8'))
                        command = "ON"
                    elif command == "ON":
                        serial_inst.write("OFF".encode('utf-8'))
                        command = "OFF"

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))  # Desenha a imagem de fundo redimensionada

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(90).render("RABBIT RUNNER", True, "#a7f5ff")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width / 2, screen_height / 7))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(screen_width / 2, screen_height / 2.8), 
                            text_input="JOGAR", font=get_font(75), base_color="#a7f5ff", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(screen_width / 2, screen_height / 1.8), 
                            text_input="ARDUINO", font=get_font(75), base_color="#a7f5ff", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(screen_width / 2, screen_height / 1.3), 
                            text_input="SAIR", font=get_font(75), base_color="#a7f5ff", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    subprocess.run(["python", "gameplay.py"])
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
