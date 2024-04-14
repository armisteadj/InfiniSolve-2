
import tkinter as tk
from tkinter import messagebox, Frame, Entry, simpledialog
import random

def print_grid(grid):
    for row in grid:
        print(" ".join(map(str, row)))

def is_valid_move(grid, row, col, num):
    if num in grid[row]:
        return False
    for i in range(9):
        if grid[i][col] == num or grid[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
            return False
    return True

def solve_sudoku(grid):
    empty = find_empty_location(grid)
    if not empty:
        return True  # No empty location means puzzle is solved
    row, col = empty
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0  # Undo the move
    return False

def find_empty_location(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)
    return None

def generate_sudoku():
    grid = [[0] * 9 for _ in range(9)]
    solve_sudoku(grid)  # First solve it completely
    remove_count = random.randint(20, 40)  # Amount of numbers to remove
    attempts = 0
    while remove_count > 0 and attempts < 100:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0:
            backup = grid[row][col]
            grid[row][col] = 0
            copy_grid = [r[:] for r in grid]
            if not solve_sudoku(copy_grid):
                grid[row][col] = backup  # Restore the number if removal makes it unsolvable
            else:
                remove_count -= 1
        attempts += 1
    return grid

def auto_solve():
    global sudoku_grid, solution_grid
    copy_grid = [row[:] for row in sudoku_grid]  # Make a copy of the current puzzle
    if solve_sudoku(copy_grid):
        for i in range(9):
            for j in range(9):
                entry_grid[i][j].delete(0, tk.END)
                entry_grid[i][j].insert(0, copy_grid[i][j])
                entry_grid[i][j].config(state='disabled', disabledforeground='black')
    else:
        messagebox.showerror("Unable to solve", "This Sudoku puzzle cannot be solved.")

def draw_grid(play_frame):
    global sudoku_grid, entry_grid
    entry_grid = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            e = Entry(play_frame, width=3, font=('Arial', 18), justify='center')
            e.grid(row=i, column=j, sticky='news', padx=1, pady=1)
            e.insert(0, sudoku_grid[i][j] if sudoku_grid[i][j] != 0 else '')
            if sudoku_grid[i][j] != 0:
                e.config(state='disabled', disabledforeground='black')
            else:
                e.bind('<FocusOut>', lambda event, row=i, col=j: update_cell(row, col, entry_grid[row][col]))
            entry_grid[i][j] = e

def update_cell(row, col, entry):
    global sudoku_grid, solution_grid
    try:
        val = int(entry.get())
        if val != solution_grid[row][col]:
            messagebox.showerror("Incorrect", "This number is incorrect.")
            entry.delete(0, 'end')
        elif val == solution_grid[row][col]:
            entry.config(state='disabled', disabledforeground='black')
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number (1-9).")
        entry.delete(0, 'end')

def generate_and_solve():
    global sudoku_grid, solution_grid
    solution_grid = generate_sudoku()  # Store the solution
    sudoku_grid = [row[:] for row in solution_grid]  # Copy for mutable version
    draw_grid(play_frame)

def input_custom_sudoku():
    input_data = simpledialog.askstring("Input", "Enter your Sudoku as an 81-character string (use space for empty):")
    if input_data and len(input_data) == 81:
        try:
            global sudoku_grid, solution_grid
            sudoku_grid = [[int(ch) if ch != ' ' else 0 for ch in input_data[i*9:(i+1)*9]] for i in range(9)]
            solution_grid = [row[:] for row in sudoku_grid]  # Copy grid
            if solve_sudoku(solution_grid):
                draw_grid(play_frame)
            else:
                messagebox.showerror("Error", "Sudoku cannot be solved.")
        except ValueError:
            messagebox.showerror("Error", "Invalid characters. Please enter numbers 1-9 and spaces.")
    elif input_data:
        messagebox.showerror("Error", "Invalid input length. Please enter exactly 81 characters.")

def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.title("Self-Solving Sudoku")

main_menu = Frame(root)
hints_menu = Frame(root)
play_screen = Frame(root)
scores_screen = Frame(root)
play_frame = Frame(play_screen)

for frame in (main_menu, hints_menu, play_screen, scores_screen, play_frame):
    frame.grid(row=0, column=0, sticky='news')

play_frame.grid(row=1, column=0, sticky='news')

tk.Button(main_menu, text="Hints", command=lambda: show_frame(hints_menu)).grid(row=0, column=0)
tk.Button(main_menu, text="Play", command=lambda: show_frame(play_screen)).grid(row=1, column=0)
tk.Button(main_menu, text="Scores", command=lambda: show_frame(scores_screen)).grid(row=2, column=0)

tk.Label(hints_menu, text="Hints are coming soon").grid(row=0, column=0)
tk.Button(hints_menu, text="Back", command=lambda: show_frame(main_menu)).grid(row=1, column=0)

tk.Button(play_screen, text="Generate Sudoku", command=generate_and_solve).grid(row=0, column=0, sticky='ew', padx=10, pady=10)
tk.Button(play_screen, text="Automatically Solve", command=auto_solve).grid(row=0, column=1, sticky='ew', padx=10, pady=10)
tk.Button(play_screen, text="Input Custom Sudoku", command=input_custom_sudoku).grid(row=0, column=2, sticky='ew', padx=10, pady=10)

tk.Label(scores_screen, text="Scores coming soon...").grid(row=0, column=0)
tk.Button(scores_screen, text="Back", command=lambda: show_frame(main_menu)).grid(row=1, column=0)

show_frame(main_menu)

root.mainloop()
