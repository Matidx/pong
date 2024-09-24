import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))  # Crear la ventana del juego
pygame.display.set_caption("Pong Matu")  # Título de la ventana

# Colores
white = (255, 255, 255)  # Color blanco
black = (0, 0, 0)  # Color negro
gray = (128, 128, 128)  # Color gris

# Variables del juego
ball_speed_x = 7  # Velocidad horizontal de la pelota
ball_speed_y = 7  # Velocidad vertical de la pelota
player_speed = 0  # Velocidad del jugador (controlado por las teclas)
opponent_speed = 10  # Velocidad del oponente (IA), ajustado para aumentar la dificultad
game_paused = False  # Variable para controlar si el juego está en pausa

# Sonidos
bounce_sound = pygame.mixer.Sound('assets/sounds/bounce.wav')  # Sonido de rebote
score_sound = pygame.mixer.Sound('assets/sounds/score.wav')  # Sonido al marcar un punto

# Rectángulos
ball = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 30, 30)  # Crear la pelota
player = pygame.Rect(screen_width - 20, screen_height // 2 - 70, 10, 140)  # Jugador
opponent = pygame.Rect(10, screen_height // 2 - 70, 10, 140)  # Oponente (IA)

# Botón de pausa
pause_button = pygame.Rect(screen_width - 100, 20, 80, 40)  # Crear el botón de pausa

# Reloj para el FPS
clock = pygame.time.Clock()  # Controlar los fotogramas por segundo

# Puntuaciones
player_score = 0  # Puntuación del jugador
opponent_score = 0  # Puntuación del oponente
font = pygame.font.Font(None, 48)  # Fuente para el texto

def show_menu():
    """Mostrar el menú principal del juego."""
    while True:
        screen.fill(black)  # Limpiar la pantalla con el color negro
        title_text = font.render("Pong", True, white)  # Renderizar el título del juego
        screen.blit(title_text, (screen_width // 2 - 50, screen_height // 2 - 100))  # Dibujar el título

        # Opción 1: Jugar contra IA
        ai_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)  # Crear botón de IA
        pygame.draw.rect(screen, gray, ai_button)  # Dibujar el botón
        ai_text = font.render("1 vs IA", True, white)  # Renderizar el texto del botón
        screen.blit(ai_text, (screen_width // 2 - 90, screen_height // 2 + 10))  # Dibujar el texto del botón

        # Opción 2: Jugar contra otro jugador
        pvp_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 60, 200, 50)  # Crear botón de PvP
        pygame.draw.rect(screen, gray, pvp_button)  # Dibujar el botón
        pvp_text = font.render("1 vs 1", True, white)  # Renderizar el texto del botón
        screen.blit(pvp_text, (screen_width // 2 - 90, screen_height // 2 + 70))  # Dibujar el texto del botón

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                pygame.quit()
                sys.exit()  # Salir del programa

            if event.type == pygame.MOUSEBUTTONDOWN:  # Si se hace clic con el ratón
                if ai_button.collidepoint(event.pos):  # Si se hace clic en el botón de IA
                    return 'ai'  # Volver para jugar contra la IA
                if pvp_button.collidepoint(event.pos):  # Si se hace clic en el botón PvP
                    return 'pvp'  # Volver para jugar contra otro jugador

        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)  # Limitar el FPS a 60

def ball_movement():
    """Actualizar la posición de la pelota y manejar colisiones."""
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    ball.x += ball_speed_x  # Mover la pelota en el eje X
    ball.y += ball_speed_y  # Mover la pelota en el eje Y

    # Colisiones con los bordes superior e inferior
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1  # Invertir la dirección vertical
        bounce_sound.play()  # Reproducir sonido de rebote
    if ball.left <= 0:  # Si la pelota sale por la izquierda
        player_score += 1  # Aumentar la puntuación del jugador
        score_sound.play()  # Reproducir sonido al marcar un punto
        ball_restart()  # Reiniciar la pelota
    if ball.right >= screen_width:  # Si la pelota sale por la derecha
        opponent_score += 1  # Aumentar la puntuación del oponente
        score_sound.play()  # Reproducir sonido al marcar un punto
        ball_restart()  # Reiniciar la pelota

    # Colisiones con los jugadores
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1  # Invertir la dirección horizontal
        bounce_sound.play()  # Reproducir sonido de rebote

def player_movement():
    """Actualizar la posición del jugador basado en la entrada."""
    player.y += player_speed  # Mover el jugador verticalmente

    # Limitar el movimiento del jugador dentro de la ventana
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai():
    """Controlar el movimiento del oponente (IA)."""
    if opponent.top < ball.y:
        opponent.y += opponent_speed  # Mover hacia abajo si la pelota está arriba
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed  # Mover hacia arriba si la pelota está abajo

    # Limitar el movimiento del oponente dentro de la ventana
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    """Reiniciar la posición de la pelota."""
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width // 2, screen_height // 2)  # Colocar la pelota en el centro

    # Generar dirección aleatoria para la pelota
    ball_speed_x = random.choice([-7, 7])  # La pelota se moverá a la izquierda o derecha
    ball_speed_y = random.randint(-7, 7)  # La velocidad vertical puede ser aleatoria

def draw_pause_button():
    """Dibujar el botón de pausa."""
    pygame.draw.rect(screen, gray, pause_button)  # Dibuja el botón
    pause_text = font.render("Pausa", True, white)  # Renderizar el texto de pausa
    screen.blit(pause_text, (pause_button.x + 5, pause_button.y + 5))  # Dibujar el texto en el botón

# Definir una fuente para el texto de pausa (si es necesario)
pause_font = pygame.font.Font(None, 8)  # Puedes cambiar el tamaño de fuente según lo desees
# Bucle principal del juego
mode = show_menu()  # Llama a la función show_menu y guarda el modo de juego seleccionado ('ai' o 'pvp')

while True:  # Comienza el bucle principal del juego
    # Manejo de eventos
    for event in pygame.event.get():  # Itera sobre todos los eventos que se han producido
        if event.type == pygame.QUIT:  # Si se cierra la ventana
            pygame.quit()  # Cierra Pygame
            sys.exit()  # Termina el programa

        # Manejo de teclas presionadas
        if event.type == pygame.KEYDOWN:
            if mode == 'pvp':  # Si el modo de juego es 'pvp'
                if event.key == pygame.K_DOWN:  # Si se presiona la tecla hacia abajo
                    player_speed += 7  # Aumenta la velocidad del jugador
                if event.key == pygame.K_UP:  # Si se presiona la tecla hacia arriba
                    player_speed -= 7  # Disminuye la velocidad del jugador
            elif mode == 'ai':  # Si el modo de juego es contra la IA
                if event.key == pygame.K_DOWN:  # Si se presiona la tecla hacia abajo
                    player_speed += 7  # Aumenta la velocidad del jugador
                if event.key == pygame.K_UP:  # Si se presiona la tecla hacia arriba
                    player_speed -= 7  # Disminuye la velocidad del jugador

        # Manejo de teclas liberadas
        if event.type == pygame.KEYUP:
            if mode == 'pvp':  # Si el modo de juego es 'pvp'
                if event.key == pygame.K_DOWN:  # Si se libera la tecla hacia abajo
                    player_speed -= 7  # Disminuye la velocidad del jugador
                if event.key == pygame.K_UP:  # Si se libera la tecla hacia arriba
                    player_speed += 7  # Aumenta la velocidad del jugador
            elif mode == 'ai':  # Si el modo de juego es contra la IA
                if event.key == pygame.K_DOWN:  # Si se libera la tecla hacia abajo
                    player_speed -= 7  # Disminuye la velocidad del jugador
                if event.key == pygame.K_UP:  # Si se libera la tecla hacia arriba
                    player_speed += 7  # Aumenta la velocidad del jugador

        # Detectar clic en el botón de pausa
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.collidepoint(event.pos):  # Si se hace clic en el botón de pausa
                game_paused = not game_paused  # Cambia el estado de pausa

    if not game_paused:  # Solo mueve la pelota si el juego no está pausado
        # Lógica del juego
        ball_movement()  # Mueve la pelota
        player_movement()  # Mueve al jugador

        # Lógica para el oponente IA o jugador
        if mode == 'ai':
            opponent_ai()  # Controla la IA del oponente
        elif mode == 'pvp':  # Si el modo de juego es 'pvp'
            # Control del segundo jugador
            keys = pygame.key.get_pressed()  # Obtiene el estado de las teclas
            if keys[pygame.K_s]:  # Si se presiona la tecla 'S'
                opponent.y += 7  # Mueve al oponente hacia abajo
            if keys[pygame.K_w]:  # Si se presiona la tecla 'W'
                opponent.y -= 7  # Mueve al oponente hacia arriba

            # Limita el movimiento del oponente dentro de la pantalla
            if opponent.top <= 0:  # Si el oponente está en la parte superior de la pantalla
                opponent.top = 0  # Coloca al oponente en el borde superior
            if opponent.bottom >= screen_height:  # Si el oponente está en la parte inferior de la pantalla
                opponent.bottom = screen_height  # Coloca al oponente en el borde inferior

    # Dibujar en la pantalla
    screen.fill(black)  # Rellena la pantalla con el color negro
    pygame.draw.rect(screen, white, player)  # Dibuja el rectángulo del jugador
    pygame.draw.rect(screen, white, opponent)  # Dibuja el rectángulo del oponente
    pygame.draw.ellipse(screen, white, ball)  # Dibuja la pelota
    pygame.draw.aaline(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))  # Dibuja una línea divisoria en el medio

    # Dibujar las puntuaciones
    player_text = font.render(f"{player_score}", True, white)  # Renderiza la puntuación del jugador
    screen.blit(player_text, (screen_width // 2 + 20, screen_height // 2))  # Dibuja la puntuación del jugador en la pantalla

    opponent_text = font.render(f"{opponent_score}", True, white)  # Renderiza la puntuación del oponente
    screen.blit(opponent_text, (screen_width // 2 - 50, screen_height // 2))  # Dibuja la puntuación del oponente en la pantalla

    # Dibujar botón de pausa
    draw_pause_button()  # Llama a la función para dibujar el botón de pausa

    # Mensaje de pausa
    if game_paused:  # Si el juego está en pausa
        pause_text = font.render("PAUSED", True, white)  # Renderiza el texto "PAUSED"
        screen.blit(pause_text, (screen_width // 2 - 100, screen_height // 2 - 100))  # Dibuja el texto "PAUSED" en la pantalla

    # Actualizar pantalla
    pygame.display.flip()  # Actualiza la pantalla
    clock.tick(60)  # Mantiene el bucle a 60 cuadros por segundo
