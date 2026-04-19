"""
Tic Tac Toe — single player (AI) and local multiplayer.
Tkinter UI with scoreboard, AI difficulty, and optional sounds (Windows).
"""

from __future__ import annotations

import random
import sys
from tkinter import (
    Tk,
    Frame,
    Label,
    Button,
    StringVar,
    BooleanVar,
    DISABLED,
    NORMAL,
    font as tkfont,
)

try:
    import winsound
except ImportError:
    winsound = None  # type: ignore[misc, assignment]

# --- Theme -----------------------------------------------------------------
BG = "#0f172a"
SURFACE = "#1e293b"
CARD = "#334155"
ACCENT = "#38bdf8"
ACCENT_MUTED = "#64748b"
TEXT = "#f1f5f9"
TEXT_DIM = "#94a3b8"
WIN = "#34d399"
LOSE = "#f87171"
DRAW = "#fbbf24"
CELL_BG = "#1e293b"
CELL_HOVER = "#475569"
CELL_X = "#38bdf8"
CELL_O = "#f472b6"
MUTED_BTN = "#475569"


def main():
    root = Tk()
    root.title("Tic Tac Toe")
    root.geometry("400x680")
    root.minsize(360, 620)
    root.configure(bg=BG)
    root.resizable(True, True)

    title_font = tkfont.Font(family="Segoe UI", size=22, weight="bold")
    body_font = tkfont.Font(family="Segoe UI", size=12)
    small_font = tkfont.Font(family="Segoe UI", size=10)
    btn_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
    cell_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")

    board = {i: " " for i in range(1, 10)}
    turn = "x"
    game_end = False
    mode = StringVar(value="single")
    difficulty = StringVar(value="hard")
    sound_on = BooleanVar(value=True)

    status_var = StringVar(value="Your turn — you are X")

    score_x = 0
    score_o = 0
    score_draw = 0

    def check_for_win(player: str) -> bool:
        lines = [
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            (1, 4, 7),
            (2, 5, 8),
            (3, 6, 9),
            (1, 5, 9),
            (3, 5, 7),
        ]
        for a, b, c in lines:
            if board[a] == board[b] == board[c] == player:
                return True
        return False

    def check_for_draw() -> bool:
        return all(board[i] != " " for i in range(1, 10))

    def minimax(is_maximizing: bool) -> int:
        if check_for_win("o"):
            return 1
        if check_for_win("x"):
            return -1
        if check_for_draw():
            return 0

        if is_maximizing:
            best = -100
            for k in range(1, 10):
                if board[k] == " ":
                    board[k] = "o"
                    best = max(best, minimax(False))
                    board[k] = " "
            return best

        best = 100
        for k in range(1, 10):
            if board[k] == " ":
                board[k] = "x"
                best = min(best, minimax(True))
                board[k] = " "
        return best

    def empty_cells() -> list[int]:
        return [k for k in range(1, 10) if board[k] == " "]

    def ai_move_hard():
        best_score = -100
        best_move = 0
        for k in range(1, 10):
            if board[k] == " ":
                board[k] = "o"
                score = minimax(False)
                board[k] = " "
                if score > best_score:
                    best_score = score
                    best_move = k
        if best_move:
            board[best_move] = "o"

    def ai_move():
        empties = empty_cells()
        if not empties:
            return
        tier = difficulty.get()
        if tier == "easy":
            board[random.choice(empties)] = "o"
            return
        if tier == "medium":
            if random.random() < 0.55:
                board[random.choice(empties)] = "o"
            else:
                ai_move_hard()
            return
        ai_move_hard()

    def play_tone(freq: int, ms: int) -> None:
        if not sound_on.get() or winsound is None or sys.platform != "win32":
            return
        try:
            winsound.Beep(freq, ms)
        except RuntimeError:
            pass

    def sound_move(player: str) -> None:
        if player == "x":
            play_tone(880, 28)
        else:
            play_tone(620, 28)

    def sound_outcome(outcome: str) -> None:
        if outcome == "draw":
            play_tone(520, 90)
            return
        if outcome == "x":
            play_tone(784, 50)
            play_tone(988, 70)
        else:
            play_tone(392, 80)
            play_tone(330, 100)

    cell_buttons: list[Button] = []

    def sync_cell(idx: int):
        b = cell_buttons[idx]
        val = board[idx + 1]
        b["text"] = val.upper() if val != " " else ""
        if val == "x":
            b["fg"] = CELL_X
        elif val == "o":
            b["fg"] = CELL_O
        else:
            b["fg"] = TEXT

    def refresh_board():
        for i in range(9):
            sync_cell(i)

    def set_status(text: str, accent: str = TEXT_DIM):
        status_var.set(text)
        status_label["fg"] = accent

    def update_scoreboard():
        if mode.get() == "single":
            score_main_var.set(f"You (X)  {score_x}    ·    Computer (O)  {score_o}    ·    Draws  {score_draw}")
        else:
            score_main_var.set(f"Player X  {score_x}    ·    Player O  {score_o}    ·    Draws  {score_draw}")

    def record_result(outcome: str) -> None:
        nonlocal score_x, score_o, score_draw
        if outcome == "x":
            score_x += 1
        elif outcome == "o":
            score_o += 1
        else:
            score_draw += 1
        update_scoreboard()
        sound_outcome(outcome)

    def end_game(message: str, color: str, outcome: str):
        nonlocal game_end
        game_end = True
        set_status(message, color)
        record_result(outcome)
        for b in cell_buttons:
            b["state"] = "disabled"

    def reset_cells_enabled():
        for b in cell_buttons:
            b["state"] = "normal"

    def restart():
        nonlocal turn, game_end
        for i in range(1, 10):
            board[i] = " "
        turn = "x"
        game_end = False
        refresh_board()
        reset_cells_enabled()
        if mode.get() == "single":
            set_status("Your turn — you are X", TEXT_DIM)
        else:
            set_status("Player X — click a cell", TEXT_DIM)

    def reset_scores():
        nonlocal score_x, score_o, score_draw
        score_x = score_o = score_draw = 0
        update_scoreboard()

    def run_ai_turn():
        nonlocal turn, game_end
        if game_end or mode.get() != "single":
            return
        ai_move()
        refresh_board()
        sound_move("o")
        if check_for_win("o"):
            end_game("Computer wins — try again!", LOSE, "o")
            return
        if check_for_draw():
            end_game("It's a draw.", DRAW, "draw")
            return
        turn = "x"
        set_status("Your turn — you are X", TEXT_DIM)

    def on_cell_click(cell_index: int):
        nonlocal turn, game_end
        if game_end:
            return
        key = cell_index + 1
        if board[key] != " ":
            return

        if mode.get() == "single":
            if turn != "x":
                return
            board[key] = "x"
            refresh_board()
            sound_move("x")
            if check_for_win("x"):
                end_game("You win — great game!", WIN, "x")
                return
            if check_for_draw():
                end_game("It's a draw.", DRAW, "draw")
                return
            turn = "o"
            set_status("Computer is thinking…", ACCENT)
            root.after(400, run_ai_turn)
            return

        board[key] = turn
        refresh_board()
        sound_move(turn)
        if check_for_win(turn):
            label = "Player X" if turn == "x" else "Player O"
            end_game(f"{label} wins!", WIN, turn)
            return
        if check_for_draw():
            end_game("It's a draw.", DRAW, "draw")
            return
        turn = "o" if turn == "x" else "x"
        next_p = "X" if turn == "x" else "O"
        set_status(f"Player {next_p} — your turn", TEXT_DIM)

    def on_mode_change():
        restart()
        update_scoreboard()
        paint_difficulty_row()

    def paint_difficulty_row():
        single = mode.get() == "single"
        state = NORMAL if single else DISABLED
        tier = difficulty.get()
        for b in diff_buttons:
            b["state"] = state
            t = getattr(b, "_tier", "hard")
            if not single:
                b["bg"] = MUTED_BTN
                b["fg"] = TEXT_DIM
            else:
                b["bg"] = ACCENT if t == tier else SURFACE
                b["fg"] = BG if t == tier else TEXT

    def pick_diff(tier: str):
        difficulty.set(tier)
        if mode.get() != "single":
            return
        for b in diff_buttons:
            t = getattr(b, "_tier", "hard")
            b["bg"] = ACCENT if t == tier else SURFACE
            b["fg"] = BG if t == tier else TEXT

    def hover(cell_index: int, entering: bool):
        if game_end:
            return
        key = cell_index + 1
        b = cell_buttons[cell_index]
        if board[key] != " ":
            return
        b["bg"] = CELL_HOVER if entering else CELL_BG

    def toggle_sound():
        sound_on.set(not sound_on.get())
        sound_btn["text"] = "Sound: On" if sound_on.get() else "Sound: Off"
        sound_btn["fg"] = TEXT if sound_on.get() else TEXT_DIM

    # --- Layout ------------------------------------------------------------
    outer = Frame(root, bg=BG)
    outer.pack(fill="both", expand=True, padx=20, pady=20)

    header = Frame(outer, bg=BG)
    header.pack(fill="x", pady=(0, 4))

    top_row = Frame(header, bg=BG)
    top_row.pack(fill="x")

    Label(
        top_row,
        text="Tic Tac Toe",
        font=title_font,
        fg=TEXT,
        bg=BG,
    ).pack(side="left", anchor="w")

    sound_btn = Button(
        top_row,
        text="Sound: On",
        font=small_font,
        bg=SURFACE,
        fg=TEXT,
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=4,
        command=toggle_sound,
    )
    sound_btn.pack(side="right", anchor="e")

    status_label = Label(
        header,
        textvariable=status_var,
        font=body_font,
        fg=TEXT_DIM,
        bg=BG,
        wraplength=340,
        justify="left",
    )
    status_label.pack(anchor="w", pady=(6, 0))

    score_card = Frame(outer, bg=SURFACE, highlightbackground=ACCENT_MUTED, highlightthickness=1)
    score_card.pack(fill="x", pady=(14, 8))

    score_inner = Frame(score_card, bg=SURFACE)
    score_inner.pack(fill="x", padx=12, pady=10)

    score_main_var = StringVar(value="")
    Label(
        score_inner,
        textvariable=score_main_var,
        font=small_font,
        fg=TEXT,
        bg=SURFACE,
        wraplength=350,
        justify="center",
    ).pack()

    reset_scores_btn = Button(
        score_inner,
        text="Reset session scores",
        font=small_font,
        bg=CARD,
        fg=TEXT_DIM,
        activebackground=CELL_HOVER,
        activeforeground=TEXT,
        relief="flat",
        cursor="hand2",
        padx=8,
        pady=4,
        command=reset_scores,
    )
    reset_scores_btn.pack(pady=(8, 0))

    mode_card = Frame(outer, bg=CARD, highlightbackground=ACCENT_MUTED, highlightthickness=1)
    mode_card.pack(fill="x", pady=(8, 10))

    inner_mode = Frame(mode_card, bg=CARD)
    inner_mode.pack(padx=12, pady=10)

    Label(
        inner_mode,
        text="Game mode",
        font=btn_font,
        fg=TEXT,
        bg=CARD,
    ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

    def paint_mode_buttons():
        sp_on = mode.get() == "single"
        single_btn["bg"] = ACCENT if sp_on else SURFACE
        single_btn["fg"] = BG if sp_on else TEXT
        multi_btn["bg"] = ACCENT if not sp_on else SURFACE
        multi_btn["fg"] = BG if not sp_on else TEXT

    def pick_single():
        mode.set("single")
        paint_mode_buttons()
        on_mode_change()

    def pick_multi():
        mode.set("multi")
        paint_mode_buttons()
        on_mode_change()

    single_btn = Button(
        inner_mode,
        text="vs Computer",
        font=btn_font,
        width=12,
        relief="flat",
        cursor="hand2",
        command=pick_single,
    )
    single_btn.grid(row=1, column=0, padx=(0, 4), pady=2)

    multi_btn = Button(
        inner_mode,
        text="2 Players",
        font=btn_font,
        width=12,
        relief="flat",
        cursor="hand2",
        command=pick_multi,
    )
    multi_btn.grid(row=1, column=1, padx=(4, 0), pady=2)
    paint_mode_buttons()

    Label(
        inner_mode,
        text="AI strength",
        font=btn_font,
        fg=TEXT,
        bg=CARD,
    ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(14, 6))

    diff_buttons: list[Button] = []

    def add_diff(text: str, tier: str, col: int):
        b = Button(
            inner_mode,
            text=text,
            font=small_font,
            width=10,
            relief="flat",
            cursor="hand2",
            command=lambda t=tier: pick_diff(t),
        )
        b.grid(row=3, column=col, padx=3, pady=2)
        b._tier = tier  # type: ignore[attr-defined]
        diff_buttons.append(b)

    add_diff("Easy", "easy", 0)
    add_diff("Medium", "medium", 1)
    add_diff("Hard", "hard", 2)

    board_card = Frame(outer, bg=CARD, highlightbackground=ACCENT_MUTED, highlightthickness=1)
    board_card.pack(fill="both", expand=True, pady=(4, 12))

    grid = Frame(board_card, bg=CARD)
    grid.pack(padx=16, pady=16)

    for r in range(3):
        for c in range(3):
            idx = r * 3 + c
            b = Button(
                grid,
                text="",
                font=cell_font,
                width=3,
                height=1,
                bg=CELL_BG,
                fg=TEXT,
                activebackground=CELL_HOVER,
                activeforeground=TEXT,
                relief="flat",
                cursor="hand2",
                command=lambda i=idx: on_cell_click(i),
            )
            b.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
            b.bind("<Enter>", lambda e, i=idx: hover(i, True))
            b.bind("<Leave>", lambda e, i=idx: hover(i, False))
            cell_buttons.append(b)

    for i in range(3):
        grid.grid_columnconfigure(i, weight=1)
        grid.grid_rowconfigure(i, weight=1)

    restart_btn = Button(
        outer,
        text="New game",
        font=btn_font,
        bg=SURFACE,
        fg=TEXT,
        activebackground=CELL_HOVER,
        activeforeground=TEXT,
        relief="flat",
        cursor="hand2",
        padx=24,
        pady=10,
        command=restart,
    )
    restart_btn.pack(fill="x", pady=(4, 0))

    pick_diff("hard")
    update_scoreboard()
    paint_difficulty_row()
    restart()
    root.mainloop()


if __name__ == "__main__":
    main()
