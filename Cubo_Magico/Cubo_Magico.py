from ursina import *
import numpy as np
import time
from datetime import timedelta
import random

app = Ursina()

camera.position = (-9, 7, -9)
camera.rotation_z = 0 
camera.look_at(Vec3(0, 0, 0))
window.title = "Projeto Cubo Mágico"
window.color = color.hex('#e8e8e8')

cubinhos = []
for x in range(-1, 2):
    for y in range(-1, 2):
        for z in range(-1, 2):
            a, b, c = str(x), str(y), str(z)
            cubinho = Entity(
                model=f'modelos_cubos/cubinho({a}, {b}, {c}).obj',
                position=(x, y, z),
                scale=0.5,
                collider = 'box'
            )
            cubinhos.append(cubinho)
front = Entity(model='quad', position=(0, 0, -1.1), scale=(2, 2), rotation_y=0, visible=False)
left = Entity(model='quad', position=(-1.1, 0, 0), scale=(2, 2), rotation_y=90, visible=False)
top = Entity(model='quad', position=(0, 1.1, 0), scale=(2, 2), rotation_x=90, visible=False)
grupo_rotacao = Entity()
titulo = Text(text='Cubo Mágico', scale=3, y=0.35, origin=(0,0), color=color.hex('#220a4d'), font='Fonte.ttf', z=-4)
titulo_parabens = Text(text='Parabéns por\nconcluir o cubo!!!', scale=3, origin=(0,0), y=0.1, color=color.hex('#220a4d'), font='Fonte.ttf', z=-4, enabled=False)
texto_timer = Text(text='00:00:00.00', position=(-0.8, 0.45), scale=3, color=color.hex('#220a4d'), font='Fonte.ttf', visible=False)
menu_fundo = Panel(scale=(1,0.9), color=color.hex('#c8c8c8'), z=-2)
menu_fundo_borda = Panel(scale=(1.05,0.95), color=color.hex('#959595'), z=-1)
botao_jogar = Button(text='Iniciar', scale=(0.3,0.08), y=0, color=color.hex('#959595'), z=-4)
botao_jogar_borda = Panel(scale=(0.32, 0.1), y=0, color=color.hex('#6e6e6e'), z=-3)
botao_voltar = Button(text='Voltar', scale=(0.3,0.08), y=-0.1, color=color.hex('#959595'), z=-4, enabled=False)
botao_voltar_borda = Panel(scale=(0.32, 0.1), y=-0.1, color=color.hex('#6e6e6e'), z=-3, enabled=False)
botao_sair = Button(text='X', model='circle', scale=(0.05,0.05), y=0.38, x=0.43, color=color.hex('ff4343'), z=-4)
botao_sair_borda = Panel(scale=(0.06,0.06), model='circle', y=0.38, x=0.43, color=color.hex('#d51616'), z=-3)

botao_jogar.text_entity.font = 'Fonte.ttf'
botao_jogar.text_entity.color = color.black
botao_voltar.text_entity.font = 'Fonte.ttf'
botao_voltar.text_entity.color = color.black
botao_sair.text_entity.font = 'Fonte.ttf'

area_cubo = [
    Vec2(0, 0.4),
    Vec2(-0.395, 0.25),
    Vec2(-0.35, -0.25),
    Vec2(0, -0.45),
    Vec2(0.35, -0.25),
    Vec2(0.395, 0.25)
]
mouse_click = mouse_click_fora = primeiro_movimento_detectado = time_on = congelado = window.exit_button.enabled = window.entity_counter.enabled = window.collider_counter.enabled = window.fps_counter.enabled = False
start_position = direcao_movimento = movimento = face_selecionada = cubo_selecionado = None
congelado = window.fullscreen = True
tempo_passado = 0

def update():
    global movimento, congelado, start_position, primeiro_movimento_detectado, direcao_movimento, face_selecionada, cubo_selecionado, mouse_click_fora, tempo_passado, time_on
    if congelado: 
            return
    if mouse_click and not mouse_click_fora:
        movimento = mouse.position - start_position
        if not primeiro_movimento_detectado and (abs(movimento[0]) > 0.01 or abs(movimento[1]) > 0.01):
            count = sum(coord == 0 for coord in (cubo_selecionado.x, cubo_selecionado.y, cubo_selecionado.z))
            if count == 2: # meio
                if face_selecionada == 'frente':
                    if abs(movimento[1]) > abs(movimento[0]):
                        direcao_movimento = 'vertical_x'
                        for c in cubinhos:
                            pos = round(c.position)
                            if pos[0] == 0:
                                c.parent = grupo_rotacao
                    elif abs(movimento[1]) < abs(movimento[0]):
                        direcao_movimento = 'horizontal'
                        for c in cubinhos:
                            pos = round(c.position)
                            if pos[1] == 0:
                                c.parent = grupo_rotacao
                    primeiro_movimento_detectado = True
                elif face_selecionada == 'esquerda':
                    if abs(movimento[1]) > abs(movimento[0]):
                        direcao_movimento = 'vertical_z'
                        for c in cubinhos:
                            pos = round(c.position)
                            if pos[2] == 0:
                                c.parent = grupo_rotacao
                    elif abs(movimento[1]) < abs(movimento[0]):
                        direcao_movimento = 'horizontal'
                        for c in cubinhos:
                            pos = round(c.position)
                            if pos[1] == 0:
                                c.parent = grupo_rotacao
                    primeiro_movimento_detectado = True
                elif face_selecionada == 'cima':
                    if movimento[0] > 0 and movimento[1] > 0 or (movimento[0] < 0 and movimento[1] < 0):
                        direcao_movimento = 'vertical_z'
                        for c in cubinhos:
                            pos = round(c.position)
                            if pos[2] == 0:
                                c.parent = grupo_rotacao
                    elif movimento[0] > 0 and movimento[1] < 0 or (movimento[0] < 0 and movimento[1] > 0):
                        direcao_movimento = 'vertical_x'
                        for c in cubinhos:
                            pos = round(c.position)
                            if pos[0] == 0:
                                c.parent = grupo_rotacao
                    primeiro_movimento_detectado = True
            elif count == 1: # cantos meio
                if face_selecionada == 'frente':
                    if abs(movimento[1]) > abs(movimento[0]):
                        direcao_movimento = 'vertical_x'
                        if cubo_selecionado[0] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[0] == 0:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == 0:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[0] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == 1:
                                    c.parent = grupo_rotacao
                    elif abs(movimento[1]) < abs(movimento[0]):
                        direcao_movimento = 'horizontal'
                        if cubo_selecionado[1] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[1] == 0:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == 0:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[1] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == 1:
                                    c.parent = grupo_rotacao
                    primeiro_movimento_detectado = True
                elif face_selecionada == 'esquerda':
                    if abs(movimento[1]) > abs(movimento[0]):
                        direcao_movimento = 'vertical_z'
                        if cubo_selecionado[2] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[2] == 0:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == 0:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[2] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == 1:
                                    c.parent = grupo_rotacao
                    elif abs(movimento[1]) < abs(movimento[0]):
                        direcao_movimento = 'horizontal'
                        if cubo_selecionado[1] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[1] == 0:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == 0:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[1] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == 1:
                                    c.parent = grupo_rotacao
                    primeiro_movimento_detectado = True
                elif face_selecionada == 'cima':
                    if movimento[0] > 0 and movimento[1] > 0 or (movimento[0] < 0 and movimento[1] < 0):
                        direcao_movimento = 'vertical_z'
                        if cubo_selecionado[2] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[2] == 0:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == 0:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[2] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == 1:
                                    c.parent = grupo_rotacao
                    elif movimento[0] > 0 and movimento[1] < 0 or (movimento[0] < 0 and movimento[1] > 0):
                        direcao_movimento = 'vertical_x'
                        if cubo_selecionado[0] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[0] == 0:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == 0:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[0] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == 1:
                                    c.parent = grupo_rotacao
                    primeiro_movimento_detectado = True
            elif count == 0: # cantos
                if face_selecionada == 'frente':
                    if abs(movimento[1]) > abs(movimento[0]):
                        direcao_movimento = 'vertical_x'
                        if cubo_selecionado[0] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[0] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == 1:
                                    c.parent = grupo_rotacao
                    elif abs(movimento[1]) < abs(movimento[0]):
                        direcao_movimento = 'horizontal'
                        if cubo_selecionado[1] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[1] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == 1:
                                    c.parent = grupo_rotacao
                    primeiro_movimento_detectado = True
                elif face_selecionada == 'esquerda':
                    if abs(movimento[1]) > abs(movimento[0]):
                        direcao_movimento = 'vertical_z'
                        if cubo_selecionado[2] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[2] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == 1:
                                    c.parent = grupo_rotacao
                    elif abs(movimento[1]) < abs(movimento[0]):
                        direcao_movimento = 'horizontal'
                        if cubo_selecionado[1] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[1] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[1] == 1:
                                    c.parent = grupo_rotacao
                    primeiro_movimento_detectado = True
                elif face_selecionada == 'cima':
                    if movimento[0] > 0 and movimento[1] > 0 or (movimento[0] < 0 and movimento[1] < 0):
                        direcao_movimento = 'vertical_z'
                        if cubo_selecionado[2] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[2] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[2] == 1:
                                    c.parent = grupo_rotacao
                    elif movimento[0] > 0 and movimento[1] < 0 or (movimento[0] < 0 and movimento[1] > 0):
                        direcao_movimento = 'vertical_x'
                        if cubo_selecionado[0] == -1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == -1:
                                    c.parent = grupo_rotacao
                        elif cubo_selecionado[0] == 1:
                            for c in cubinhos:
                                pos = round(c.position)
                                if pos[0] == 1:
                                    c.parent = grupo_rotacao
                    primeiro_movimento_detectado = True
        if direcao_movimento == 'horizontal':
            grupo_rotacao.rotation_y -= movimento[0] * 140
        elif direcao_movimento == 'vertical_x':
            grupo_rotacao.rotation_x += movimento[1] * 140
        elif direcao_movimento == 'vertical_z':
            grupo_rotacao.rotation_z += movimento[1] * 140

    elif mouse_click and mouse_click_fora:
        for c in cubinhos:
            c.parent = grupo_rotacao
        movimento = mouse.position - start_position
        if not primeiro_movimento_detectado and (abs(movimento[0]) > 0.01 or abs(movimento[1]) > 0.01): 
            if start_position[0] > 0:
                if abs(movimento[1]) > abs(movimento[0]):
                    direcao_movimento = 'vertical_x'
            if start_position[0] < 0:
                if abs(movimento[1]) > abs(movimento[0]):
                    direcao_movimento = 'vertical_z'
            if abs(movimento[1]) < abs(movimento[0]):
                direcao_movimento = 'horizontal'
            primeiro_movimento_detectado = True
        if direcao_movimento == 'horizontal':
            grupo_rotacao.rotation_y -= movimento[0] * 140
        elif direcao_movimento == 'vertical_x':
            grupo_rotacao.rotation_x += movimento[1] * 140
        elif direcao_movimento == 'vertical_z':
            grupo_rotacao.rotation_z += movimento[1] * 140
    start_position = mouse.position
    
    if time_on:
        tempo_passado += time.dt
        tempo_formatado = str(timedelta(seconds=tempo_passado))[:-3] 
        texto_timer.text = tempo_formatado.zfill(11)

def mouse_sobre_face():
    projections = {
        'frente': np.dot(mouse.world_point, front.position),
        'esquerda': np.dot(mouse.world_point, left.position),
        'cima': np.dot(mouse.world_point, top.position)
    }
    return max(projections, key=projections.get)
   
def point_in_polygon(point, poly):
    x, y = point
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / ((yj - yi) + 1e-10) + xi):
            inside = not inside
        j = i
    return inside

def verifica_pronto():
    global lado_verificado, normalf, normalb
    cubo_verificado = 0
    lado_verificado = False
    for c in cubinhos:
        if verifica_lados(c):
            cubo_verificado += 1
        else:
            normalf = None
            normalb = None
            return False
    if cubo_verificado == 27:
        return True

def verifica_lados(cubo):
    global lado_verificado, normalf, normalb
    if not lado_verificado:
        normalf = round(cubo.forward)
        normalb = round(cubo.down)
        lado_verificado = True
    if normalf == round(cubo.forward) and normalb == round(cubo.down):
        return True
    else:
        return False

def input(key):
    global mouse_click, congelado, start_position, primeiro_movimento_detectado, direcao_movimento, face_selecionada, cubo_selecionado, mouse_click_fora, time_on, tempo_passado, congelado
    if congelado:
        return
    mouse_pos = Vec2(mouse.position[0], mouse.position[1])

    if key == 'left mouse down':
        time_on = True
        if point_in_polygon(mouse_pos, area_cubo):
            mouse_click = True
            start_position = mouse.position
            cubo_selecionado = None
            cubo_selecionado = round(mouse.hovered_entity.position)
            face_selecionada = mouse_sobre_face()
        else:
            mouse_click = mouse_click_fora = True
            start_position = mouse.position
    elif key == 'left mouse up':
        mouse_click = mouse_click_fora = primeiro_movimento_detectado = False  
        direcao_movimento = face_selecionada = cubo_selecionado = start_position = None
        grupo_rotacao.rotation_x = round(grupo_rotacao.rotation_x / 90) * 90
        grupo_rotacao.rotation_y = round(grupo_rotacao.rotation_y / 90) * 90
        grupo_rotacao.rotation_z = round(grupo_rotacao.rotation_z / 90) * 90
        limpar_grupo()
        if verifica_pronto():
            botao_voltar.enabled = botao_voltar_borda.enabled = titulo_parabens.enabled = menu_fundo.enabled = menu_fundo_borda.enabled = congelado = True
            menu_fundo.scale = (1,0.5)
            menu_fundo_borda.scale=(1.05,0.55)
            texto_timer.visible = time_on = False
            tempo_passado = 0
            texto_timer.text = '00:00:00.00'
    if key == 'escape':
        menu_fundo.enabled = titulo.enabled = botao_jogar.enabled = botao_sair.enabled = botao_jogar_borda.enabled = botao_sair_borda.enabled = True
        texto_timer.visible = time_on = False
        tempo_passado = 0

def limpar_grupo():
    for c in cubinhos:
        world_pos = c.world_position
        world_rot = c.world_rotation
        c.parent = scene
        c.position = world_pos
        c.rotation = world_rot
    grupo_rotacao.position = (0, 0, 0)
    grupo_rotacao.rotation = (0, 0, 0)

def sair():
    application.quit()

def jogar():
    global congelado, index, i
    menu_fundo.enabled = menu_fundo_borda.enabled = titulo.enabled = botao_jogar.enabled = botao_sair.enabled = botao_jogar_borda.enabled = botao_sair_borda.enabled = False
    index = i = 0
    embaralhar()

def voltar():
    botao_voltar.enabled = botao_voltar_borda.enabled = titulo_parabens.enabled = False
    titulo.enabled = botao_jogar.enabled = botao_sair.enabled = botao_jogar_borda.enabled = botao_sair_borda.enabled = True
    menu_fundo.scale = (1,0.9)
    menu_fundo_borda.scale=(1.05,0.95)

def embaralhar():
    global index, congelado, time_on, i

    if index >= 4:
        congelado = False
        time_on = True
        texto_timer.visible = True
        return
    if i < 5:
        movimentos()
        limpar_grupo()
        invoke(embaralhar, delay=0.5)
        i += 1
        return
    for c in cubinhos:
        c.parent = grupo_rotacao
    grupo_rotacao.rotation_y += 90
    limpar_grupo()
    i = 0
    index += 1
    invoke(embaralhar, delay=1)

def movimentos():
    orientacao = random.choice([-1, 1])
    eixo = random.randint(0, 2)
    camada = random.randint(-1, 1)
    for c in cubinhos:
        pos = round(c.position)
        if pos[eixo] == camada: 
            c.parent = grupo_rotacao
        if eixo == 1:  # Rotação em Y
            grupo_rotacao.rotation_y += 90 * orientacao
        elif eixo == 0:  # Rotação em X
            grupo_rotacao.rotation_x += 90 * orientacao
        elif eixo == 2:  # Rotação em Z
            grupo_rotacao.rotation_z += 90 * orientacao

botao_sair.on_click = sair
botao_jogar.on_click = jogar
botao_voltar.on_click = voltar

app.run()