import tkinter as tk
import random

# Constants
GAME_SIZE = 20  # Number of cells in the grid
CELL_SIZE = 35
GAME_WIDTH = GAME_SIZE * CELL_SIZE
GAME_HEIGHT = GAME_SIZE * CELL_SIZE
SPEED = 100
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"
BORDER_COLOR = "white"

class SnakeGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Snake Game")
        self.window.resizable(False, False)
        
        self.score = 0
        self.direction = 'down'
        self.paused = False

        self.label = tk.Label(window, text=f"Score: {self.score}", font=('consolas', 40))
        self.label.pack()

        self.canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        button_frame = tk.Frame(window)
        button_frame.pack()

        self.start_button = tk.Button(button_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=0, column=0)

        self.restart_button = tk.Button(button_frame, text="Restart Game", command=self.restart_game)
        self.restart_button.grid(row=0, column=1)

        self.resume_button = tk.Button(button_frame, text="Resume Game", command=self.resume_game)
        self.resume_button.grid(row=0, column=2)

        self.pause_button = tk.Button(button_frame, text="Pause Game", command=self.pause_game)
        self.pause_button.grid(row=0, column=3)

        window.bind('<Left>', lambda event: self.change_direction('left'))
        window.bind('<Right>', lambda event: self.change_direction('right'))
        window.bind('<Up>', lambda event: self.change_direction('up'))
        window.bind('<Down>', lambda event: self.change_direction('down'))

        self.create_borders()

    def create_borders(self):
        # Draw borders with holes
        self.canvas.create_rectangle(0, 0, GAME_WIDTH, CELL_SIZE, fill=BORDER_COLOR, outline="")
        self.canvas.create_rectangle(0, GAME_HEIGHT - CELL_SIZE, GAME_WIDTH, GAME_HEIGHT, fill=BORDER_COLOR, outline="")
        self.canvas.create_rectangle(0, 0, CELL_SIZE, GAME_HEIGHT, fill=BORDER_COLOR, outline="")
        self.canvas.create_rectangle(GAME_WIDTH - CELL_SIZE, 0, GAME_WIDTH, GAME_HEIGHT, fill=BORDER_COLOR, outline="")

        # Holes in borders
        self.canvas.create_rectangle(0, GAME_HEIGHT // 2 - CELL_SIZE // 2, CELL_SIZE, GAME_HEIGHT // 2 + CELL_SIZE // 2, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)
        self.canvas.create_rectangle(GAME_WIDTH - CELL_SIZE, GAME_HEIGHT // 2 - CELL_SIZE // 2, GAME_WIDTH, GAME_HEIGHT // 2 + CELL_SIZE // 2, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)
        self.canvas.create_rectangle(GAME_WIDTH // 2 - CELL_SIZE // 2, 0, GAME_WIDTH // 2 + CELL_SIZE // 2, CELL_SIZE, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)
        self.canvas.create_rectangle(GAME_WIDTH // 2 - CELL_SIZE // 2, GAME_HEIGHT - CELL_SIZE, GAME_WIDTH // 2 + CELL_SIZE // 2, GAME_HEIGHT, fill=BACKGROUND_COLOR, outline=BACKGROUND_COLOR)

    def start_game(self):
        self.canvas.delete("all")
        self.create_borders()
        self.snake = [[CELL_SIZE, CELL_SIZE]]
        self.snake_squares = [self.canvas.create_rectangle(CELL_SIZE, CELL_SIZE, CELL_SIZE * 2, CELL_SIZE * 2, fill=SNAKE_COLOR)]
        self.food = self.create_food()
        self.score = 0
        self.direction = 'down'
        self.paused = False
        self.label.config(text=f"Score: {self.score}")
        self.next_turn()

    def restart_game(self):
        self.start_game()

    def resume_game(self):
        self.paused = False
        self.next_turn()

    def pause_game(self):
        self.paused = True

    def create_food(self):
        x = random.randint(1, GAME_SIZE - 2) * CELL_SIZE
        y = random.randint(1, GAME_SIZE - 2) * CELL_SIZE
        return self.canvas.create_oval(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=FOOD_COLOR, tag="food")

    def next_turn(self):
        if self.paused:
            return
        x, y = self.snake[0]
        if self.direction == "up":
            y -= CELL_SIZE
        elif self.direction == "down":
            y += CELL_SIZE
        elif self.direction == "left":
            x -= CELL_SIZE
        elif self.direction == "right":
            x += CELL_SIZE

        # Handle wrapping around the borders
        if (x, y) in [(0, GAME_HEIGHT // 2), (GAME_WIDTH - CELL_SIZE, GAME_HEIGHT // 2), (GAME_WIDTH // 2, 0), (GAME_WIDTH // 2, GAME_HEIGHT - CELL_SIZE)]:
            if x == 0:
                x = GAME_WIDTH - 2 * CELL_SIZE
            elif x == GAME_WIDTH - CELL_SIZE:
                x = CELL_SIZE
            elif y == 0:
                y = GAME_HEIGHT - 2 * CELL_SIZE
            elif y == GAME_HEIGHT - CELL_SIZE:
                y = CELL_SIZE

        self.snake.insert(0, (x, y))
        square = self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=SNAKE_COLOR)
        self.snake_squares.insert(0, square)

        if self.canvas.coords(self.snake_squares[0]) == self.canvas.coords(self.food):
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.food = self.create_food()
        else:
            del self.snake[-1]
            self.canvas.delete(self.snake_squares.pop())

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(SPEED, self.next_turn)

    def change_direction(self, new_direction):
        opposites = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        if new_direction != opposites[self.direction]:
            self.direction = new_direction

    def check_collisions(self):
        x, y = self.snake[0]
        if (x, y) in self.snake[1:]:
            return True
        return False

    def game_over(self):
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, font=('consolas', 70), text="GAME OVER", fill="red", tags="gameover")

if __name__ == "__main__":
    window = tk.Tk()
    game = SnakeGame(window)
    window.mainloop()
