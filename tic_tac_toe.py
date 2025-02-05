# pre-requirements
!pip install gspread oauth2client 

# Note: This code need a credential.json to authenticate and store evaluation metrics in google sheets.

# Code
import tkinter as tk
from tkinter import messagebox
import math
import time
import tracemalloc
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random

# Game class to manage the Tic-Tac-Toe board and alpha-beta pruning AI
class TicTacToe:
    def __init__(self, size, pruning_type):
        self.session_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=11))
        self.size = size
        self.pruning_type = pruning_type  # Sequential or Parallel
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'  # Human player
        self.AI_player = 'O'
        self.human_player = 'X'
        self.win_length = size  # Number of consecutive marks to win
        self.max_depth = self.get_depth_limit(size)  # Dynamic depth limit based on board size
        self.move_metrics = []  # Store metrics for each AI move

    def get_depth_limit(self, size):
        # Dynamically adjust the depth limit based on board size
        if size <= 3:
            return 9  # Explore fully for 3x3
        elif size <= 5:
            return 4
        elif size <= 6:
            return 3
        else:
            return 2  # For larger boards, use a smaller depth to keep computation manageable

    def check_winner(self, player):
        # Check rows, columns, and diagonals for a winning line
        for row in self.board:
            if self.check_consecutive(row, player):
                return True

        for col in range(self.size):
            if self.check_consecutive([self.board[row][col] for row in range(self.size)], player):
                return True

        if self.check_consecutive([self.board[i][i] for i in range(self.size)], player):
            return True
        if self.check_consecutive([self.board[i][self.size - i - 1] for i in range(self.size)], player):
            return True

        return False

    def check_consecutive(self, sequence, player):
        count = 0
        for cell in sequence:
            if cell == player:
                count += 1
                if count == self.win_length:
                    return True
            else:
                count = 0
        return False

    def is_board_full(self):
        return all(self.board[i][j] != '' for i in range(self.size) for j in range(self.size))

    def evaluate_board(self):
        # Evaluate the board state
        if self.check_winner(self.AI_player):
            return 10
        elif self.check_winner(self.human_player):
            return -10
        else:
            return 0

    def minimax(self, depth, is_maximizing, alpha, beta, start_time, max_time=3.0):
        if time.time() - start_time > max_time:
            return 0  # End evaluation if time limit is reached
        
        score = self.evaluate_board()
        if score == 10 or score == -10 or self.is_board_full():
            return score
        if depth >= self.max_depth:  # Depth limit to avoid freezing
            return 0  # Treat as a draw if the maximum depth is reached

        if is_maximizing:
            best_score = -math.inf
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == '':
                        self.board[i][j] = self.AI_player
                        score = self.minimax(depth + 1, False, alpha, beta, start_time, max_time)
                        self.board[i][j] = ''
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = math.inf
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == '':
                        self.board[i][j] = self.human_player
                        score = self.minimax(depth + 1, True, alpha, beta, start_time, max_time)
                        self.board[i][j] = ''
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def get_best_move(self):
        start_time = time.time()
        max_time = 2.0  # Limit the computation to 3 seconds max
        best_score = -math.inf
        best_move = None

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '':
                    start_time = time.time()
                    tracemalloc.start()
                    start_time = time.time()
                    self.board[i][j] = self.AI_player
                    score = self.minimax(0, False, -math.inf, math.inf, start_time, max_time)
                    self.board[i][j] = ''

                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

                    # Store metrics for this AI move if it's an actual AI move
                    if best_move == (i, j):
                        self.move_metrics.append({
                            'session_id': self.session_id,
                            'board_size': self.size,
                            'pruning_type': self.pruning_type,
                            'move': best_move,
                            'time_taken': end_time - start_time,
                            'memory_used': peak / 1024,  # KB,
                            
                            'result': None  # Placeholder, will be updated later
                        })
        return best_move

    def make_move(self, row, col, player):
        if self.board[row][col] == '':
            self.board[row][col] = player
            return True
        return False

# GUI class to manage the game interface
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')  # Fullscreen
        self.main_frame = None
        self.board_frame = None
        self.buttons = []
        self.size = 3  # Default size
        self.pruning_type = 'Sequential'  # Default pruning type
        self.build_main_menu()

    def build_main_menu(self):
        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Title
        tk.Label(self.main_frame, text="Tic-Tac-Toe Game", font=("Arial", 36, "bold")).pack(pady=50)

        # Board size selection
        select_frame = tk.Frame(self.main_frame)
        select_frame.pack(pady=20)

        tk.Label(select_frame, text="Select board size:", font=("Arial", 24)).pack(side=tk.LEFT)
        self.board_size_var = tk.IntVar(value=3)
        size_menu = tk.OptionMenu(select_frame, self.board_size_var, *[i for i in range(3, 11)])
        size_menu.config(font=("Arial", 18), width=5, bg="dodger blue", fg="white")
        size_menu.pack(side=tk.LEFT, padx=10)

        # Pruning type selection
        tk.Label(select_frame, text="Select pruning type:", font=("Arial", 24)).pack(side=tk.LEFT, padx=20)
        self.pruning_type_var = tk.StringVar(value='Sequential')
        pruning_menu = tk.OptionMenu(select_frame, self.pruning_type_var, 'Sequential', 'Parallel')
        pruning_menu.config(font=("Arial", 18), width=10, bg="dodger blue", fg="white")
        pruning_menu.pack(side=tk.LEFT, padx=10)

        # Start and Exit buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=50)

        start_button = tk.Button(button_frame, text="Start Game", font=("Arial", 18), bg="green", fg="white", command=self.start_game)
        start_button.pack(side=tk.LEFT, padx=20)

        exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 18), bg="red", fg="white", width=10, command=self.exit_game)
        exit_button.pack(side=tk.RIGHT, padx=20)

    def exit_game(self):
        self.root.destroy()  # Properly close the application

    def start_game(self):
        self.size = self.board_size_var.get()
        self.pruning_type = self.pruning_type_var.get()
        if self.main_frame:
            self.main_frame.destroy()

        self.build_board()

    def build_board(self):
        if self.board_frame:
            self.board_frame.destroy()

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(expand=True, fill=tk.BOTH)

        self.game = TicTacToe(self.size, self.pruning_type)
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]

        board_frame = tk.Frame(self.board_frame)
        board_frame.pack(expand=True)

        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(board_frame, text="", font='normal 20 bold', width=4, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(self.game, i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        # Create Back and End buttons
        control_frame = tk.Frame(self.board_frame)
        control_frame.pack(pady=20)

        tk.Button(control_frame, text="Back", font=("Arial", 18), command=self.go_back).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="End", font=("Arial", 18), command=self.exit_game).pack(side=tk.RIGHT, padx=10)

    def on_button_click(self, game, i, j):
        if game.make_move(i, j, game.human_player):
            self.buttons[i][j].config(text=game.human_player)
            if game.check_winner(game.human_player):
                messagebox.showinfo("Game Over", "You Win!")
                result = 0  # Human Wins
                for move in game.move_metrics:
                    move['result'] = result
                self.save_metrics(game)
                self.go_back()
            elif game.is_board_full():
                messagebox.showinfo("Game Over", "It's a Draw!")
                result = 2  # Draw
                for move in game.move_metrics:
                    move['result'] = result
                self.save_metrics(game)
                self.go_back()
            else:
                self.ai_move(game)

    def ai_move(self, game):
        move = game.get_best_move()
        if move:
            row, col = move
            game.make_move(row, col, game.AI_player)
            self.buttons[row][col].config(text=game.AI_player)
            if game.check_winner(game.AI_player):
                messagebox.showinfo("Game Over", "AI Wins!")
                result = 1  # AI Wins
                for move in game.move_metrics:
                    move['result'] = result
                self.save_metrics(game)
                self.go_back()
            elif game.is_board_full():
                messagebox.showinfo("Game Over", "It's a Draw!")
                result = 2  # Draw
                for move in game.move_metrics:
                    move['result'] = result
                self.save_metrics(game)
                self.go_back()
            if game.check_winner(game.AI_player):
                messagebox.showinfo("Game Over", "AI Wins!")
                result = 1  # AI Wins
                for move in game.move_metrics:
                    move['result'] = result
                self.save_metrics(game)
                self.go_back()
            elif game.is_board_full():
                messagebox.showinfo("Game Over", "It's a Draw!")
                result = 2  # Draw
                for move in game.move_metrics:
                    move['result'] = result
                self.save_metrics(game)
                self.go_back()

    def save_metrics(self, game):
        # Save the AI metrics to Google Sheets
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)

        # Authenticating Google Sheet 
        sheet = client.open('Tic_Tac_toe_analysis_value').sheet1

        # Prepare data for Google Sheets
        unique_moves = set()
        for move in game.move_metrics:
            if move['move'] not in unique_moves:
                sheet.append_row([
                    move['session_id'],
                    move['board_size'],
                    move['pruning_type'],
                    str(move['move']),
                    move['time_taken'],
                    move['memory_used'],
                    move['result']
                ])
                unique_moves.add(move['move'])

    def go_back(self):
        if self.board_frame:
            self.board_frame.destroy()
        self.build_main_menu()

# Main function to initialize the game and GUI
def main():
    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
