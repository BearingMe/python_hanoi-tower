import sys
import time
import pygame
from datetime import datetime
from run import Question
from algorithm import Solver

# inicializador do modo de depuração 
question = Question()
solver = Solver()
question.debug_mode()
debug = question.DEBUG

# inicializa o módulo, define o nome da janela, e o tamanho.
pygame.init()
pygame.display.set_caption('Torre de Hanoi')
surface = pygame.display.set_mode((640, 480)) # surface é a área onde o jogo será contruido  

# configurações de jogo
clock = pygame.time.Clock()
game_done = False
framerate = 30
steps = 0
n_disks = 3
disks = []
towers_midx = [120, 320, 520]
pointing_at = 0
floating = False
floater = 0

# cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78,162,196) 
grey = (170, 170, 170)
green = (77, 206, 145)


# variáveis de fonte
def blit_text(surface, text, midtop, aa=True, font=None, font_name = None, size = None, color=(255,0,0)):
    if font is None:                                
        font = pygame.font.SysFont(font_name, size)   
    font_surface = font.render(text, aa, color)
    font_rect = font_surface.get_rect()
    font_rect.midtop = midtop
    surface.blit(font_surface, font_rect)


# cria os discos e permite ter seus valores de posição alterados
def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 397 - height
    width = n_disks * 23
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (120, ypos)
        disk['val'] = n_disks-i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height+3
        width -= 23


# mostra a pontuação
def draw_ptr():
    ptr_points = [(towers_midx[pointing_at]-7 ,440), (towers_midx[pointing_at]+7, 440), (towers_midx[pointing_at], 433)]
    pygame.draw.polygon(surface, red, ptr_points)
    return


# desenha os discos na tela
def draw_disks():
    global surface, disks
    for disk in disks:
        pygame.draw.rect(surface, blue, disk['rect'])
    return


# tela de menu
def menu_surface():
    # chama as variáveis de jogo
    global surface, n_disks, game_done
    menu_done = False

    while not menu_done:  
        # cor de fundo da tela inicial
        surface.fill(white)

        # define os textos presentes no menu
        blit_text(surface, 'Torre de Hanoi', (323,122), font_name='sans serif', size=90, color=grey)
        blit_text(surface, 'Torre de Hanoi', (320,120), font_name='sans serif', size=90, color=blue)
        blit_text(surface, 'Use as setas para selecionar a dificuldade: ', (320, 220), font_name='sans serif', size=30, color=black)
        blit_text(surface, str(n_disks), (320, 260), font_name='sans serif', size=40, color=grey)
        blit_text(surface, 'Aperte ENTER para continuar...', (320, 320), font_name='sans_serif', size=30, color=black)
      
        # recebe os input do teclado no meu inicial
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu_done = True
                    game_done = True
                if event.key == pygame.K_RETURN:
                    menu_done = True
                if event.key in [pygame.K_RIGHT, pygame.K_UP]:
                    n_disks += 1
                    if n_disks > 6:
                        n_disks = 6
                if event.key in [pygame.K_LEFT, pygame.K_DOWN]:
                    n_disks -= 1
                    if n_disks < 1:
                        n_disks = 1
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
        pygame.display.flip()

        # mantém a taxa de frames em 60fps
        clock.tick(60)

    if debug and menu_done:
        solver.tower(n_disks)
        solver.command_disk()


# desenho das torres
def draw_towers():
    global surface
    for xpos in range(40, 460+1, 200):
        # desenha as torres através de retangulos
        pygame.draw.rect(surface, green, pygame.Rect(xpos, 400, 160 , 20))
        pygame.draw.rect(surface, grey, pygame.Rect(xpos+75, 200, 10, 200))

    # coloca as legendas abaixo das torres
    blit_text(surface, 'Inicio', (towers_midx[0], 403), font_name='mono', size=14, color=black)
    blit_text(surface, 'Fim', (towers_midx[2], 403), font_name='mono', size=14, color=black)


# verifica as posições dos discos para definir a vitória
def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        game_over()


# tela de game over
def game_over(): 
    global surface, steps
    surface.fill(white)
    min_steps = 2**n_disks-1
    blit_text(surface, 'Você ganhou!', (320, 200), font_name='sans serif', size=72, color=blue)
    blit_text(surface, 'Você ganhou!', (322, 202), font_name='sans serif', size=72, color=blue)
    blit_text(surface, 'Seus movimentos: '+str(steps), (320, 360), font_name='mono', size=30, color=black)
    blit_text(surface, 'Passos minimos: '+str(min_steps), (320, 390), font_name='mono', size=30, color=red)
    if min_steps==steps:
        blit_text(surface, 'Finalizado com o minímo de movimentos!', (320, 300), font_name='mono', size=26, color=green)
    pygame.display.flip()

    # espera n segundos antes de finalizar
    time.sleep(2)  

    # finaliza o pygame 
    pygame.quit()   

    # finaliza o programa 
    sys.exit()  


# reinicia as variáveis de jogo
def reset():
    global steps,pointing_at,floating,floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_surface()
    make_disks()


# cria a superficie, os disco e manipula a variável de controle de tempo
menu_surface()
make_disks()
interval = (10**6)*(framerate-1)/framerate

print(solver.all_moves)
print(len(solver.all_moves))
print(len(solver.all_commands))

# loop de depuração 
if debug:
    all_commands = iter(solver.all_commands)
    command = next(all_commands)

    while not game_done:
        print(datetime.now().microsecond)
        up, down, right, left = False, False, False, False

        if command == 'up': up = True
        if command == 'down': down = True
        if command == 'right': right = True
        if command == 'left': left = True

        if up and not floating: # comando com a tecla cima
            if interval < datetime.now().microsecond < 999999:
                print(command, 'executado')
                command = next(all_commands)
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers_midx[pointing_at], 100)
                        break


        if right: # comando com a tecla direita
            if interval < datetime.now().microsecond < 999999:
                print(command, 'executado')
                command = next(all_commands)
                pointing_at = (pointing_at+1)%3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at

        if left: # comando com a tecla esquerda
            if interval < datetime.now().microsecond < 999999:
                print(command, 'executado')
                command = next(all_commands)
                pointing_at = (pointing_at-1)%3
                if floating:
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                    disks[floater]['tower'] = pointing_at

        if down and floating: # comando com a tecla baixo
            if interval < datetime.now().microsecond < 999999:
                print(command, 'executado')
                try:
                    command = next(all_commands)
                except: Exception
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                        if disk['val']>disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                            steps += 1
                        break
                else: 
                    floating = False
                    disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                    steps += 1


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_done = True
                        
        surface.fill(white)
        draw_towers()
        draw_disks()
        draw_ptr()
        blit_text(surface, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
        pygame.display.flip()
        if not floating: check_won()
        clock.tick(framerate)


# loop principal do jogo
else:
    while not game_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset()
                if event.key == pygame.K_q:
                    game_done = True

                if event.key == pygame.K_RIGHT: # comando com a tecla direita
                    pointing_at = (pointing_at+1)%3
                    if floating:
                        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                        disks[floater]['tower'] = pointing_at

                if event.key == pygame.K_LEFT: # comando com a tecla esquerda
                    pointing_at = (pointing_at-1)%3
                    if floating:
                        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 100)
                        disks[floater]['tower'] = pointing_at

                if event.key == pygame.K_UP and not floating: # comando com a tecla cima
                    for disk in disks[::-1]:
                        if disk['tower'] == pointing_at:
                            floating = True
                            floater = disks.index(disk)
                            disk['rect'].midtop = (towers_midx[pointing_at], 100)
                            break

                if event.key == pygame.K_DOWN and floating: # comando com a tecla baixo
                    for disk in disks[::-1]:
                        if disk['tower'] == pointing_at and disks.index(disk)!=floater:
                            if disk['val']>disks[floater]['val']:
                                floating = False
                                disks[floater]['rect'].midtop = (towers_midx[pointing_at], disk['rect'].top-23)
                                steps += 1
                            break
                    else: 
                        floating = False
                        disks[floater]['rect'].midtop = (towers_midx[pointing_at], 400-23)
                        steps += 1
        surface.fill(white)
        draw_towers()
        draw_disks()
        draw_ptr()
        blit_text(surface, 'Steps: '+str(steps), (320, 20), font_name='mono', size=30, color=black)
        pygame.display.flip()
        if not floating: check_won()
        clock.tick(framerate)

