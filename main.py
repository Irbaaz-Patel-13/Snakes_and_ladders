import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from PIL import Image, ImageTk


class SnakesAndLaddersGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snakes and Ladders")

        self.board_size = 10
        self.square_size = 70
        self.players = [1, 1]
        self.current_player = 0

        # Load images

        try:
            background_image = Image.open("board_background.jpg").resize(
                (self.board_size * self.square_size, self.board_size * self.square_size), Image.LANCZOS)
            self.background_image = ImageTk.PhotoImage(background_image)

            player_images = [
                Image.open("player_red.png").resize((40, 40), Image.LANCZOS),
                Image.open("player_blue.png").resize((40, 40), Image.LANCZOS)
            ]
            self.player_images = [ImageTk.PhotoImage(img) for img in player_images]

            self.snake_image = Image.open("snake.png.jpeg").resize((60, 60), Image.LANCZOS)
            self.snake_image = ImageTk.PhotoImage(self.snake_image)

            self.ladder_image = Image.open("ladder.png").resize((60, 60), Image.LANCZOS)
            self.ladder_image = ImageTk.PhotoImage(self.ladder_image)

        except Exception as e:
            messagebox.showerror("Image Loading Error", f"An error occurred while loading images: {str(e)}")
            self.master.destroy()
            return

        # Create canvas
        self.canvas = tk.Canvas(self.master, width=self.board_size * self.square_size,
                                height=self.board_size * self.square_size)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        self.draw_board()
        self.draw_players()
        self.draw_snakes_and_ladders()

        self.roll_button = tk.Button(self.master, text="Roll the Die", command=self.roll_die, font=("Arial", 12),
                                     bg="lightblue", padx=10, pady=5)
        self.roll_button.pack(pady=10)

    def draw_board(self):
        # Draw the start block
        start_x, start_y = 0, 0
        self.canvas.create_rectangle(start_x, start_y, start_x + self.square_size, start_y + self.square_size,
                                     outline="black", fill="lightgreen")
        self.canvas.create_text(start_x + self.square_size / 2, start_y + self.square_size / 2, text="Start",
                                fill="black", font=("Arial", 10, "bold"))

        # Draw the win block
        win_x, win_y = (self.board_size - 1) * self.square_size, (self.board_size - 1) * self.square_size
        self.canvas.create_rectangle(win_x, win_y, win_x + self.square_size, win_y + self.square_size, outline="black",
                                     fill="lightgreen")
        self.canvas.create_text(win_x + self.square_size / 2, win_y + self.square_size / 2, text="Win", fill="black",
                                font=("Arial", 10, "bold"))

    def draw_players(self):
        for i, player_pos in enumerate(self.players):
            if player_pos > 1:  # Clear previous position
                prev_row, prev_col = divmod(player_pos - 1, self.board_size)
                prev_x, prev_y = prev_col * self.square_size + self.square_size // 2, prev_row * self.square_size + self.square_size // 2
                self.canvas.create_rectangle(prev_x - 20, prev_y - 20, prev_x + 20, prev_y + 20, outline="lightblue",
                                             fill="lightblue")

            row, col = divmod(player_pos - 1, self.board_size)
            x, y = col * self.square_size + self.square_size // 2, row * self.square_size + self.square_size // 2
            self.canvas.create_image(x, y, anchor=tk.CENTER, image=self.player_images[i])

    def draw_snakes_and_ladders(self):
        snakes_and_ladders_dict = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}

        for start, end in snakes_and_ladders_dict.items():
            start_row, start_col = divmod(start - 1, self.board_size)
            start_x, start_y = start_col * self.square_size + self.square_size // 2, start_row * self.square_size + self.square_size // 2

            end_row, end_col = divmod(end - 1, self.board_size)
            end_x, end_y = end_col * self.square_size + self.square_size // 2, end_row * self.square_size + self.square_size // 2

            if start > end:
                self.canvas.create_image(start_x, start_y, anchor=tk.CENTER, image=self.snake_image)
            else:
                self.canvas.create_image(start_x, start_y, anchor=tk.CENTER, image=self.ladder_image)

    def roll_die(self):
        dice_roll = random.randint(1, 6)
        messagebox.showinfo("Dice Roll", f"The current player rolled a {dice_roll}")

        self.players[self.current_player] += dice_roll
        self.players[self.current_player] = self.snakes_and_ladders(self.players[self.current_player])

        self.draw_players()

        if self.players[self.current_player] >= self.board_size ** 2:
            winner = "Player 1" if self.current_player == 0 else "Player 2"
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.master.destroy()
        else:
            self.current_player = 1 - self.current_player  # Switch player turns

    def snakes_and_ladders(self, position):
        snakes_and_ladders_dict = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        return snakes_and_ladders_dict.get(position, position)


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakesAndLaddersGame(root)
    root.mainloop()
