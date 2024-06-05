import pygame
import sys
import math

# Dimensiones del tablero
BOARD_SIZE = 5  # 5x5 tablero
TILE_SIZE = 100
WINDOW_SIZE = BOARD_SIZE * TILE_SIZE

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Gato y Ratón")

# Cargar imágenes
cat_image = pygame.image.load("cat.png")
mouse_image = pygame.image.load("mouse.png")
cat_image = pygame.transform.scale(cat_image, (TILE_SIZE, TILE_SIZE))
mouse_image = pygame.transform.scale(mouse_image, (TILE_SIZE, TILE_SIZE))

# Posiciones iniciales
cat_pos = (0, 4)
mouse_pos = (4, 0)
escape_activo = True # Modificar si no se desea al casilla de escape
escape_pos = (2, 2)  # Opcional, se puede modificar para establecer una casilla de escape

#Contador de movimientos en caso de empate
mov_max = BOARD_SIZE * BOARD_SIZE / 2
cont_mov = 0

# Función para dibujar el tablero y las piezas
def draw_board():
    for x in range(0, WINDOW_SIZE, TILE_SIZE):
        for y in range(0, WINDOW_SIZE, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    
    # Dibujar el gato
    screen.blit(cat_image, (cat_pos[0] * TILE_SIZE, cat_pos[1] * TILE_SIZE))
    # Dibujar el ratón
    screen.blit(mouse_image, (mouse_pos[0] * TILE_SIZE, mouse_pos[1] * TILE_SIZE))
    # Dibujar la casilla de escape
    if escape_activo: 
        pygame.draw.rect(screen, BLUE, (escape_pos[0] * TILE_SIZE, escape_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

# Función para verificar si una posición está dentro del tablero
def is_valid_pos(pos):
    return 0 <= pos[0] < BOARD_SIZE and 0 <= pos[1] < BOARD_SIZE

# Función para obtener las posibles jugadas desde una posición
def get_possible_moves(pos, is_cat=False):
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    possible_moves = []
    for move in moves:
        new_pos = (pos[0] + move[0], pos[1] + move[1])
        if is_valid_pos(new_pos):
            if is_cat and new_pos == escape_pos and escape_activo:
                continue  # Saltar la casilla de escape si es el gato
            possible_moves.append(new_pos)
    return possible_moves

# Función para evaluar el tablero
def evaluate(cat_pos, mouse_pos):
    if cat_pos == mouse_pos:
        return 1000  # Gato gana
    elif mouse_pos == escape_pos:
        return -1000  # Ratón gana
    else:
        # Heurística: distancia entre gato y ratón, y ratón a casilla de escape
        if escape_activo:
            mouse_to_escape = math.dist(mouse_pos, escape_pos) if escape_pos else float('inf')
        else: 
            mouse_to_escape = math.dist(mouse_pos, cat_pos)
        
        cat_to_mouse = math.dist(cat_pos, mouse_pos)
        return cat_to_mouse - mouse_to_escape

# Algoritmo Minimax
def minimax(cat_pos, mouse_pos, depth, is_cat_turn):
    if escape_activo:
        if depth == 0 or cat_pos == mouse_pos or mouse_pos == escape_pos:
            return evaluate(cat_pos, mouse_pos)
    else:
        if depth == 0 or cat_pos == mouse_pos:
            return evaluate(cat_pos, mouse_pos)
    
    if is_cat_turn:
        max_eval = -float('inf')
        for move in get_possible_moves(cat_pos, is_cat=True):
            eval = minimax(move, mouse_pos, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(mouse_pos, is_cat=False):
            eval = minimax(cat_pos, move, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

# Función para encontrar la mejor jugada para el gato
def find_best_move_cat(cat_pos, mouse_pos):
    best_move = None
    best_value = -float('inf')
    for move in get_possible_moves(cat_pos, is_cat=True):
        move_value = minimax(move, mouse_pos, 3, False)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    global cont_mov #Establecemos la variable como global
    cont_mov += 1 #Incrementamos el contador de movimiento
    return best_move

# Función para encontrar la mejor jugada para el ratón
def find_best_move_mouse(cat_pos, mouse_pos):
    best_move = None
    best_value = float('inf')
    for move in get_possible_moves(mouse_pos, is_cat=False):
        move_value = minimax(cat_pos, move, 3, True)
        if move_value < best_value:
            best_value = move_value
            best_move = move
    global cont_mov #Establecemos la variable como global
    cont_mov += 1 #Incrementamos el contador de movimiento
    return best_move

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(BLACK)
    draw_board()
    pygame.display.flip()

    # IA mueve el gato
    cat_pos = find_best_move_cat(cat_pos, mouse_pos)
    draw_board()
    pygame.display.flip()
    pygame.time.wait(500)  # Esperar medio segundo para ver el movimiento
    
    # Verificar si el gato ha atrapado al ratón
    if cat_pos == mouse_pos:
        print("El gato ha atrapado al ratón. ¡Gato gana!")
        pygame.quit()
        sys.exit()

    # IA mueve el ratón
    mouse_pos = find_best_move_mouse(cat_pos, mouse_pos)
    draw_board()
    pygame.display.flip()
    pygame.time.wait(500)  # Esperar medio segundo para ver el movimiento

    # Verifica si se llego al limite de movimientos establecido
    if cont_mov >= mov_max:
        print("El juego a terminado en empate!")
        pygame.quit()
        sys.exit()
    
    # Verificar si el ratón ha escapado si hay casilla de escape
    if escape_activo and mouse_pos == escape_pos:
        print("El ratón ha escapado. ¡Ratón gana!")
        pygame.quit()
        sys.exit()
