import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text="", font=('Helvetica', 30), width=5, height=2,
                                                command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_button_click(self, row, col):
        if self.board[row][col] == '':
            self.buttons[row][col].config(text=self.current_player)
            self.board[row][col] = self.current_player
            if self.check_winner(row, col):
                messagebox.showinfo("Congratulations!", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.check_board_full():
                messagebox.showinfo("Tied!", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, row, col):
        player = self.current_player
        # Check row
        if all(self.board[row][c] == player for c in range(3)):
            return True
        # Check column
        if all(self.board[r][col] == player for r in range(3)):
            return True
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def check_board_full(self):
        return all(self.board[row][col] != '' for row in range(3) for col in range(3))

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
                self.board[i][j] = ''
        self.current_player = "X"

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
