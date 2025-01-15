from PIL import Image, ImageTk
import tkinter as tk
import random
import time

GRID_SIZE = 9
CELL_SIZE = 55
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + 50
WHITE = "#FFFFFF"
BLACK = "#000000"
ERROR_COLOR = "#F44336" #Red
TIMER_COLOR = "#E0B0FF" #Purple
TEXT_COLOR = "#333333" #Black
HIGHLIGHT_COLOR = "#E0B0FF" #Purple
WIN_COLOR = "#11ed3d" #Green
GAME_OVER_COLOR = "#F44336" #Red
BORDER_COLOR = "#2E3B4E" #Deep blue
USER_COLOR = "#6f20b0" #Purple
BLOCK_COLORS = ["#aca6ad", "#FFFFFF", "#aca6ad", # Grey, White, Grey
                "#FFFFFF", "#aca6ad", "#FFFFFF", # White, Grey, White
                "#aca6ad", "#FFFFFF", "#aca6ad"]  # Grey, White, Grey

root = tk.Tk()
root.title("Sudoku")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=WHITE)
canvas.pack()
mistakes = 0
time_limit = 5
remaining_time = time_limit
start_time = time.time()
user_input = {}
grid = None
play_again_button = None
play_again_yes_button = None
play_again_no_button = None
win_image = Image.open("happy_raccoon.png")
lose_image = Image.open("sad_raccoon.jpg")
win_image = win_image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
lose_image = lose_image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
win_image_tk = ImageTk.PhotoImage(win_image)
lose_image_tk = ImageTk.PhotoImage(lose_image)

def generate_grid():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    fill_diagonal(grid)
    fill_remaining(grid, 0, 3)
    remove_numbers(grid)
    return grid

def is_safe(grid, row, col, num):
    for x in range(GRID_SIZE):
        if grid[row][x] == num or grid[x][col] == num:
            return False

    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True

def fill_diagonal(grid):
    for i in range(0, GRID_SIZE, 3):
        fill_box(grid, i, i)

def fill_box(grid, row, col):
    nums = list(range(1, GRID_SIZE + 1))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            grid[row + i][col + j] = nums.pop()

def fill_remaining(grid, i, j):
    if j >= GRID_SIZE and i < GRID_SIZE - 1:
        i += 1
        j = 0
    if i >= GRID_SIZE and j >= GRID_SIZE:
        return True
    if i < 3:
        if j < 3:
            j = 3
    elif i < GRID_SIZE - 3:
        if j == int(i / 3) * 3:
            j += 3
    else:
        if j == GRID_SIZE - 3:
            i += 1
            j = 0
            if i >= GRID_SIZE:
                return True
    for num in range(1, GRID_SIZE + 1):
        if is_safe(grid, i, j, num):
            grid[i][j] = num
            if fill_remaining(grid, i, j + 1):
                return True
            grid[i][j] = 0
    return False

def has_unique_solution(grid):
    def solve(grid):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:
                    for num in range(1, GRID_SIZE + 1):
                        if is_safe(grid, row, col, num):
                            grid[row][col] = num
                            if solve(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True
    grid_copy = [row[:] for row in grid]
    if not solve(grid_copy):
        return False
    solution_found = [False]
    def solve_with_limit(grid):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:
                    for num in range(1, GRID_SIZE + 1):
                        if is_safe(grid, row, col, num):
                            grid[row][col] = num
                            if solve_with_limit(grid):
                                if solution_found[0]:
                                    return False
                                solution_found[0] = True
                            grid[row][col] = 0
                    return True
        return True
    grid_copy = [row[:] for row in grid]
    solve_with_limit(grid_copy)
    return solution_found[0]

def remove_numbers(grid):
    attempts = 40
    while attempts > 0:
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        while grid[row][col] == 0:
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        removed_number = grid[row][col]
        grid[row][col] = 0
        grid_copy = [row[:] for row in grid]
        if not has_unique_solution(grid_copy):
            grid[row][col] = removed_number
        else:
            attempts -= 1

def draw_grid_lines():
    for i in range(1, GRID_SIZE):
        width = 3 if i % 3 == 0 else 1
        canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, HEIGHT, width=width, fill=BORDER_COLOR, tags="grid_lines")
        canvas.create_line(0, i * CELL_SIZE, WIDTH, i * CELL_SIZE, width=width, fill=BORDER_COLOR, tags="grid_lines")

def draw_grid(grid, selected=None):
    canvas.delete("grid")
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x1, y1 = j * CELL_SIZE, i * CELL_SIZE
            x2, y2 = (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE
            block_color = BLOCK_COLORS[(i // 3) * 3 + (j // 3)]
            color = block_color
            if selected == (i, j):
                color = HIGHLIGHT_COLOR
            canvas.create_rectangle(x1, y1, x2, y2, outline=BORDER_COLOR, fill=color, width=2, tags="grid")
            if grid[i][j] != 0:
                if (i, j) in user_input:
                    number_color = USER_COLOR
                else:
                    number_color = TEXT_COLOR
                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(grid[i][j]), font=("Arial", 18, "bold"),fill=number_color, tags="grid")
draw_grid_lines()

def on_key_press(event, grid, selected):
    global mistakes
    if mistakes >= 3:
        return
    if selected:
        i, j = selected
        if event.keysym in ['BackSpace', 'Delete']:
            if (i, j) in user_input:
                del user_input[(i, j)]
                grid[i][j] = 0
                draw_grid(grid)
                undo_stack.append(('delete', (i, j), 0))
        elif grid[i][j] == 0:
            value = event.char
            if value in '123456789':
                value = int(value)
                if is_safe(grid, i, j, value):
                    grid[i][j] = value
                    user_input[(i, j)] = value
                    draw_grid(grid)
                else:
                    mistakes += 1
                    print(f"Mistakes: {mistakes}")
                    if mistakes >= 3:
                        show_game_over()
                    else:
                        draw_grid(grid)

def on_click(event, grid):
    x, y = event.x, event.y
    selected = (y // CELL_SIZE, x // CELL_SIZE)
    draw_grid(grid, selected)
    root.bind("<KeyPress>", lambda e: on_key_press(e, grid, selected))

def disable_game_interaction():
    root.unbind("<KeyPress>")
    canvas.unbind("<Button-1>")
    root.after_cancel(update_timer)

def destroy_play_again_buttons():
    global play_again_yes_button, play_again_no_button
    if play_again_yes_button:
        play_again_yes_button.place_forget()
        play_again_yes_button = None
    if play_again_no_button:
        play_again_no_button.place_forget()
        play_again_no_button = None

def show_win():
    global play_again_yes_button, play_again_no_button
    canvas.delete("all")
    reset_button.place_forget()
    solve_button.place_forget()
    if win_image_tk:
        canvas.create_image(0, 0, anchor="nw", image=win_image_tk)
    else:
        canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=WIN_COLOR, outline=BLACK)
    canvas.create_text(WIDTH // 2, HEIGHT // 3, text="You Win!", font=("Arial", 40, "bold"), fill=WIN_COLOR)
    disable_game_interaction()
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Would you like to play again?", font=("Arial", 16), fill=WIN_COLOR)
    if not play_again_yes_button:
        play_again_yes_button = tk.Button(root, text="Yes", font=("Arial", 14), bg="#6a2c91", fg=WHITE, command=lambda: [reset_game(), destroy_play_again_buttons()])
        play_again_yes_button.place(relx=0.4, rely=0.6, anchor="center")
    if not play_again_no_button:
        play_again_no_button = tk.Button(root, text="No", font=("Arial", 14), bg="#6a2c91", fg=WHITE, command=lambda: [root.quit(), destroy_play_again_buttons()])
        play_again_no_button.place(relx=0.6, rely=0.6, anchor="center")

def show_game_over():
    global play_again_yes_button, play_again_no_button
    canvas.delete("all")
    reset_button.place_forget()
    solve_button.place_forget()
    if lose_image_tk:
        canvas.create_image(0, 0, anchor="nw", image=lose_image_tk)
    else:
        canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=GAME_OVER_COLOR, outline=BLACK)
    canvas.create_text(WIDTH // 2, HEIGHT // 3, text="Game Over!", font=("Arial", 40, "bold"), fill=GAME_OVER_COLOR)
    disable_game_interaction()
    canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Would you like to play again?", font=("Arial", 16), fill=GAME_OVER_COLOR)
    if not play_again_yes_button:
        play_again_yes_button = tk.Button(root, text="Yes", font=("Arial", 14), bg="#6a2c91", fg=WHITE,command=lambda: [reset_game(), destroy_play_again_buttons()])
        play_again_yes_button.place(relx=0.4, rely=0.6, anchor="center")
    if not play_again_no_button:
        play_again_no_button = tk.Button(root, text="No", font=("Arial", 14), bg="#6a2c91", fg=WHITE,command=lambda: [root.quit(), destroy_play_again_buttons()])
        play_again_no_button.place(relx=0.6, rely=0.6, anchor="center")

def check_win(grid):
    for row in grid:
        if 0 in row:
            return False
    return True

grid = generate_grid()

def solve_board(grid):
    def solve(grid):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row][col] == 0:
                    for num in range(1, GRID_SIZE + 1):
                        if is_safe(grid, row, col, num):
                            grid[row][col] = num
                            if solve(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True
    solve(grid)
    draw_grid(grid)

solve_button = None
def create_solve_button():
    global solve_button
    if solve_button is None:
        solve_button = tk.Button(root, text="Solve the Board", font=("Arial", 12), bg="#6a2c91", fg=WHITE, command=lambda: solve_board(grid))
        solve_button.place(x=WIDTH - 480, y=HEIGHT - 42)

def reset_board():
    global grid, user_input, mistakes, start_time
    user_input.clear()
    mistakes = 0
    grid = generate_grid()
    canvas.delete("all")
    draw_grid_lines()
    draw_grid(grid)
    update_timer(grid)

def reset_game():
    global mistakes, start_time, user_input, play_again_button, game_reset, grid
    mistakes = 0
    start_time = time.time()
    user_input.clear()
    game_reset = True
    if 'play_again_button' in globals() and play_again_button:
        play_again_button.destroy()
        play_again_button = None
    grid = generate_grid()
    canvas.delete("all")
    draw_grid_lines()
    draw_grid(grid)
    canvas.unbind("<Button-1>")
    canvas.bind("<Button-1>", lambda event: on_click(event, grid))
    solve_button.place(x=WIDTH - 480, y=HEIGHT - 42)
    update_timer(grid)

def create_reset_button():
    reset_button = tk.Button(root, text="Reset Board", font=("Arial", 12), bg="#6a2c91", fg=WHITE, command=reset_board)
    reset_button.place(x=WIDTH - 120, y=HEIGHT - 40)
    return reset_button

reset_button = create_reset_button()

def update_timer(grid):
    global remaining_time
    remaining_time = time_limit - int(time.time() - start_time)
    minutes, seconds = divmod(remaining_time, 60)
    elapsed_time = int(time.time() - start_time)
    canvas.create_rectangle(0, HEIGHT - 50, WIDTH, HEIGHT, fill=TIMER_COLOR, outline=BLACK, width=2)
    canvas.create_text(WIDTH // 2, HEIGHT - 35, text=f"Time: {minutes:02}:{seconds:02}", font=("Arial", 18, "bold"),fill=TEXT_COLOR)
    canvas.create_text(WIDTH // 2, HEIGHT - 15, text=f"Mistakes: {mistakes}/3", font=("Arial", 18, "bold"),fill=TEXT_COLOR)
    reset_button.place(x=WIDTH - 135, y=HEIGHT - 42)
    if remaining_time <= 0:
        show_game_over()
    elif mistakes < 3 and not check_win(grid):
        root.after(1000, update_timer, grid)
    elif check_win(grid):
        show_win()
    elif mistakes >= 3:
        show_game_over()

game_reset = True

def main():
    global grid
    grid = generate_grid()
    draw_grid(grid)
    canvas.bind("<Button-1>", lambda event: on_click(event, grid))
    update_timer(grid)
    create_solve_button()
    root.mainloop()

if __name__ == "__main__":
    main()