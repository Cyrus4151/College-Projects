import tkinter as tk
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 35
BODY_PARTS = 1
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"
BORDER_COLOR = "white"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[SPACE_SIZE, SPACE_SIZE]] * BODY_PARTS
        self.squares = [canvas.create_rectangle(SPACE_SIZE, SPACE_SIZE, SPACE_SIZE * 2, SPACE_SIZE * 2, fill=SNAKE_COLOR, tags="snake")]

class Food:
    def __init__(self):
        x = random.randint(1, (GAME_WIDTH // SPACE_SIZE) - 2) * SPACE_SIZE
        y = random.randint(1, (GAME_HEIGHT // SPACE_SIZE) - 2) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]
    x += SPACE_SIZE * (direction == "right") - SPACE_SIZE * (direction == "left")
    y += SPACE_SIZE * (direction == "down") - SPACE_SIZE * (direction == "up")

    if (x, y) in [(0, GAME_HEIGHT // 2), (GAME_WIDTH - SPACE_SIZE, GAME_HEIGHT // 2), (GAME_WIDTH // 2, 0), (GAME_WIDTH // 2, GAME_HEIGHT - SPACE_SIZE)]:
        if x == 0:
            x = GAME_WIDTH - 2 * SPACE_SIZE
        elif x == GAME_WIDTH - SPACE_SIZE:
            x = SPACE_SIZE
        elif y == 0:
            y = GAME_HEIGHT - 2 * SPACE_SIZE
        elif y == GAME_HEIGHT - SPACE_SIZE:
            y = SPACE_SIZE
    elif x < SPACE_SIZE or x >= GAME_WIDTH - SPACE_SIZE or y < SPACE_SIZE or y >= GAME_HEIGHT - SPACE_SIZE:
        game_over()
        return
    
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if (x, y) == tuple(food.coordinates):
        global score
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares.pop())

    if check_collisions(snake):
        game_over()
    else:
        if not paused:
            window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    opposites = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
    if new_direction != opposites[direction]:
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if (x, y) in snake.coordinates[1:]:
        return True
    return False

def game_over():
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tags="gameover")

def start_game():
    canvas.delete("all")
    global snake, food, score, direction, paused
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    paused = False
    label.config(text=f"Score: {score}")
    create_borders()
    next_turn(snake, food)

def restart_game():
    canvas.delete("all")
    start_game()

def resume_game():
    global paused
    paused = False
    next_turn(snake, food)

def pause_game():
    global paused
    paused = True

def create_borders():
    # Draw borders with holes
    canvas.create_rectangle(0, 0, GAME_WIDTH, SPACE_SIZE, fill=BORDER_COLOR, outline="")
    canvas.create_rectangle(0, GAME_HEIGHT - SPACE_SIZE, GAME_WIDTH, GAME_HEIGHT, fill=BORDER_COLOR, outline="")
    canvas.create_rectangle(0, 0, SPACE_SIZE, GAME_HEIGHT, fill=BORDER_COLOR, outline="")
    canvas.create_rectangle(GAME_WIDTH - SPACE_SIZE, 0, GAME_WIDTH, GAME_HEIGHT, fill=BORDER_COLOR, outline="")

    # Holes in borders
    canvas.create_rectangle(0, GAME_HEIGHT // 2 - SPACE_SIZE // 2, SPACE_SIZE, GAME_HEIGHT // 2 + SPACE_SIZE // 2, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)
    canvas.create_rectangle(GAME_WIDTH - SPACE_SIZE, GAME_HEIGHT // 2 - SPACE_SIZE // 2, GAME_WIDTH, GAME_HEIGHT // 2 + SPACE_SIZE // 2, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)
    canvas.create_rectangle(GAME_WIDTH // 2 - SPACE_SIZE // 2, 0, GAME_WIDTH // 2 + SPACE_SIZE // 2, SPACE_SIZE, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)
    canvas.create_rectangle(GAME_WIDTH // 2 - SPACE_SIZE // 2, GAME_HEIGHT - SPACE_SIZE, GAME_WIDTH // 2 + SPACE_SIZE // 2, GAME_HEIGHT, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)

window = tk.Tk()
window.title("SNAKE GAME")
window.resizable(False, False)

score = 0
direction = 'down'
paused = False

label = tk.Label(window, text=f"Score: {score}", font=('consolas', 40))
label.pack()

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Buttons
button_frame = tk.Frame(window)
button_frame.pack()

start_button = tk.Button(button_frame, text="Start Game", command=start_game)
start_button.grid(row=0, column=0)

restart_button = tk.Button(button_frame, text="Restart Game", command=restart_game)
restart_button.grid(row=0, column=1)

resume_button = tk.Button(button_frame, text="Resume Game", command=resume_game)
resume_button.grid(row=0, column=2)

pause_button = tk.Button(button_frame, text="Pause Game", command=pause_game)
pause_button.grid(row=0, column=3)

window.update()
window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{int(window.winfo_screenwidth() / 2 - window.winfo_width() / 2)}+{int(window.winfo_screenheight() / 2 - window.winfo_height() / 2)}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.mainloop()
