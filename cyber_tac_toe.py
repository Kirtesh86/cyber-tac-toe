#!/usr/bin/env python3
import tkinter as tk
from tkinter import font
import time
import math
import random
import threading

# Platform checks for audio
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

class SoundSynth:
    """Asynchronous synthesized retro-futuristic sound manager."""
    enabled = True

    @classmethod
    def play_beep(cls, freq, duration):
        if not cls.enabled or not HAS_WINSOUND:
            return
        def _run():
            try:
                winsound.Beep(freq, duration)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()

    @classmethod
    def hover(cls):
        # Ultra short high beep for hover tick
        cls.play_beep(1500, 20)

    @classmethod
    def click(cls):
        # Futuristic click
        def _run():
            try:
                if not cls.enabled or not HAS_WINSOUND: return
                winsound.Beep(900, 40)
                time.sleep(0.01)
                winsound.Beep(1600, 30)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()

    @classmethod
    def place_x(cls):
        # Slide down frequency
        def _run():
            try:
                if not cls.enabled or not HAS_WINSOUND: return
                winsound.Beep(700, 60)
                winsound.Beep(500, 60)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()

    @classmethod
    def place_o(cls):
        # Slide up frequency
        def _run():
            try:
                if not cls.enabled or not HAS_WINSOUND: return
                winsound.Beep(800, 60)
                winsound.Beep(1100, 60)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()

    @classmethod
    def victory(cls):
        # Winning chord sequence
        def _run():
            try:
                if not cls.enabled or not HAS_WINSOUND: return
                notes = [600, 800, 1000, 1400]
                for note in notes:
                    winsound.Beep(note, 90)
                    time.sleep(0.02)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()

    @classmethod
    def defeat(cls):
        # Glitchy descending sequence
        def _run():
            try:
                if not cls.enabled or not HAS_WINSOUND: return
                notes = [500, 380, 260]
                for note in notes:
                    winsound.Beep(note, 150)
                    time.sleep(0.04)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()

    @classmethod
    def tie(cls):
        # Alert tone
        def _run():
            try:
                if not cls.enabled or not HAS_WINSOUND: return
                winsound.Beep(700, 80)
                time.sleep(0.05)
                winsound.Beep(700, 80)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()

    @classmethod
    def glitch(cls):
        # Sound overlay representing a static screen click
        def _run():
            try:
                if not cls.enabled or not HAS_WINSOUND: return
                f1 = random.randint(1800, 2200)
                f2 = random.randint(1200, 1600)
                winsound.Beep(f1, 30)
                time.sleep(0.01)
                winsound.Beep(f2, 20)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()


class TicTacToeEngine:
    """Tic Tac Toe board logic and AI computations."""
    WIN_COMBOS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8), # Columns
        (0, 4, 8), (2, 4, 6)             # Diagonals
    ]

    def __init__(self):
        self.board = [""] * 9
        self.current_turn = "X" # X starts
        self.scores = {"X": 0, "O": 0, "ties": 0}
        self.mode = "PVE" # PVP, PVE, EVE
        self.difficulty = "HARD" # EASY, MEDIUM, HARD

    def reset_board(self):
        self.board = [""] * 9
        self.current_turn = "X"

    def make_move(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_turn
            self.current_turn = "O" if self.current_turn == "X" else "X"
            return True
        return False

    def check_winner(self, board_state=None):
        b = board_state if board_state is not None else self.board
        for combo in self.WIN_COMBOS:
            if b[combo[0]] != "" and b[combo[0]] == b[combo[1]] == b[combo[2]]:
                return b[combo[0]], combo
        if "" not in b:
            return "tie", None
        return None, None

    def is_full(self):
        return "" not in self.board

    # --- Minimax AI ---
    def get_empty_cells(self, board):
        return [i for i, val in enumerate(board) if val == ""]

    def minimax(self, board, depth, is_maximizing, ai_token, opponent_token):
        winner, _ = self.check_winner(board)
        if winner == ai_token:
            return 10 - depth
        elif winner == opponent_token:
            return depth - 10
        elif "" not in board:
            return 0

        if is_maximizing:
            best_val = -1000
            for i in self.get_empty_cells(board):
                board[i] = ai_token
                val = self.minimax(board, depth + 1, False, ai_token, opponent_token)
                board[i] = ""
                best_val = max(best_val, val)
            return best_val
        else:
            best_val = 1000
            for i in self.get_empty_cells(board):
                board[i] = opponent_token
                val = self.minimax(board, depth + 1, True, ai_token, opponent_token)
                board[i] = ""
                best_val = min(best_val, val)
            return best_val

    def get_ai_move(self):
        empty = self.get_empty_cells(self.board)
        if not empty:
            return None

        ai_token = self.current_turn
        opp_token = "O" if ai_token == "X" else "X"

        # 1. Easy Mode: Complete randomness
        if self.difficulty == "EASY":
            return random.choice(empty)

        # 2. Medium Mode: 60% smart (win/block), else random
        if self.difficulty == "MEDIUM":
            # Can we win in next move?
            for i in empty:
                self.board[i] = ai_token
                win, _ = self.check_winner()
                self.board[i] = ""
                if win == ai_token:
                    return i
            # Can opponent win in next move? Block them.
            for i in empty:
                self.board[i] = opp_token
                lose, _ = self.check_winner()
                self.board[i] = ""
                if lose == opp_token:
                    return i
            # 50% minimax, 50% random
            if random.random() > 0.5:
                return random.choice(empty)

        # 3. Psycho Mode / Medium standard path: Full minimax
        best_val = -1000
        best_move = empty[0]

        # Optimize: if board is empty, pick corner or center to skip minimax delay
        if len(empty) == 9:
            return random.choice([0, 2, 4, 6, 8])

        for i in empty:
            self.board[i] = ai_token
            val = self.minimax(self.board, 0, False, ai_token, opp_token)
            self.board[i] = ""
            if val > best_val:
                best_val = val
                best_move = i
        return best_move

    def scan_cell_probability(self, index):
        """Calculates win probability for the scanning HUD overlay."""
        if self.board[index] != "":
            return None

        active = self.current_turn
        opponent = "O" if active == "X" else "X"

        # Check immediate win
        self.board[index] = active
        win, _ = self.check_winner()
        if win == active:
            self.board[index] = ""
            return 100 # Guaranteed Win

        # Check immediate block
        self.board[index] = opponent
        block, _ = self.check_winner()
        if block == opponent:
            self.board[index] = ""
            # Scanning evaluates blocking as highly favorable, but not a guaranteed winning branch
            # We run normal minimax score check on placement
            self.board[index] = active
            val = self.minimax(self.board, 0, False, active, opponent)
            self.board[index] = ""
            if val > 0: return 100
            if val == 0: return 0
            return -100

        self.board[index] = active
        val = self.minimax(self.board, 0, False, active, opponent)
        self.board[index] = ""

        if val > 0:
            return 100  # Win path
        elif val == 0:
            return 0    # Tie path
        else:
            return -100 # Defeat path


class CyberCanvasButton:
    """Fully custom-drawn interactive neon button for tkinter canvas."""
    def __init__(self, canvas, x1, y1, x2, y2, text, callback, 
                 active_color="#00f0ff", hover_color="#fcee0a", bg_color="#090a0f",
                 is_toggle=False, is_selected=False):
        self.canvas = canvas
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.text = text
        self.callback = callback
        self.active_color = active_color
        self.hover_color = hover_color
        self.bg_color = bg_color
        self.is_toggle = is_toggle
        self.is_selected = is_selected
        self.is_hovered = False
        
        self.poly_id = None
        self.text_id = None
        self.accent_id = None
        self.glow_id = None
        self.draw()

    def _get_corners(self):
        # 45-degree chamfered tech corners (top-left & bottom-right cut)
        d = 8
        return [
            self.x1 + d, self.y1,
            self.x2, self.y1,
            self.x2, self.y2 - d,
            self.x2 - d, self.y2,
            self.x1, self.y2,
            self.x1, self.y1 + d
        ]

    def draw(self):
        # Clean existing canvas objects
        if self.poly_id: self.canvas.delete(self.poly_id)
        if self.text_id: self.canvas.delete(self.text_id)
        if self.accent_id: self.canvas.delete(self.accent_id)
        if self.glow_id: self.canvas.delete(self.glow_id)

        # Decide theme color based on hover and selection state
        outline_c = self.hover_color if self.is_hovered else self.active_color
        text_c = self.hover_color if self.is_hovered else self.active_color
        bg_c = self.bg_color

        if self.is_toggle and self.is_selected:
            # Highlight selected toggle button
            bg_c = "#141b29"
            outline_c = self.hover_color
            text_c = self.hover_color

        # Render neon glow underlay if hovered or selected
        corners = self._get_corners()
        if self.is_hovered or (self.is_toggle and self.is_selected):
            self.glow_id = self.canvas.create_polygon(
                corners,
                fill="",
                outline=outline_c,
                width=5,
                stipple="gray25" # transparency simulation in Tkinter
            )

        # Main polygon shape
        self.poly_id = self.canvas.create_polygon(
            corners,
            fill=bg_c,
            outline=outline_c,
            width=1.5
        )

        # Draw decorative neon strip if selected
        if self.is_toggle and self.is_selected:
            self.accent_id = self.canvas.create_line(
                self.x1 + 1, self.y1 + 8, self.x1 + 1, self.y2 - 1,
                fill="#ff0055", width=3
            )

        # Draw button label
        mx = (self.x1 + self.x2) / 2
        my = (self.y1 + self.y2) / 2
        self.text_id = self.canvas.create_text(
            mx, my,
            text=self.text.upper(),
            fill=text_c,
            font=("Consolas", 10, "bold")
        )

    def check_hover(self, mx, my):
        inside = (self.x1 <= mx <= self.x2) and (self.y1 <= my <= self.y2)
        if inside != self.is_hovered:
            self.is_hovered = inside
            self.draw()
            if self.is_hovered:
                SoundSynth.hover()
            return True
        return False

    def check_click(self, mx, my):
        if (self.x1 <= mx <= self.x2) and (self.y1 <= my <= self.y2):
            SoundSynth.click()
            self.callback()
            return True
        return False


class CyberpunkApp:
    """The central application wrapper, handling visuals, physics, and canvas loops."""
    def __init__(self, root):
        self.root = root
        self.root.title("TIC-TAC-TOE // NEON GRID v.77")
        self.root.geometry("950x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#07070a")

        # Initialize engines
        self.engine = TicTacToeEngine()
        
        # State Management: 'MENU' or 'GAME'
        self.app_state = "MENU"
        self.simulation_running = False
        self.sim_last_move_time = 0
        
        # Dashboard parameters
        self.opt_sound = True
        self.opt_hacking = False
        self.opt_crt = True
        
        # Visual variables
        self.particles = []
        self.glitch_active = False
        self.glitch_end_frame = 0
        self.frame_count = 0
        
        # Grid hover highlight
        self.hovered_cell = None
        
        # Console output buffer
        self.logs = []
        
        # Set up canvas
        self.canvas = tk.Canvas(root, width=950, height=700, bg="#07070a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Set up events
        self.canvas.bind("<Motion>", self.on_mouse_motion)
        self.canvas.bind("<Button-1>", self.on_mouse_click)

        # Init logs
        self.log_message("SYS_BOOT: SYSTEM KERNEL OK.")
        self.log_message("SYS_LINK: CHIP TUNED TO PORT 77.")
        
        # Spawn ambient dust particles
        for _ in range(25):
            self.spawn_particle(
                random.randint(20, 930), random.randint(20, 680), 
                random.uniform(-0.3, 0.3), random.uniform(-0.5, -0.1),
                random.randint(1, 3), random.choice(["#00f0ff", "#ff0055", "#fcee0a"]),
                random.uniform(0.5, 1.0), 0.005
            )

        # Init UI elements
        self.buttons = []
        self.init_menu_widgets()

        # Start Visual Rendering Loop (FPS Target: ~30-40 FPS)
        self.update_loop()

    # --- CLI Logging Console ---
    def log_message(self, text):
        timestamp = time.strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {text.upper()}")
        if len(self.logs) > 5:
            self.logs.pop(0)

    # --- Particle Physics Engine ---
    def spawn_particle(self, x, y, vx, vy, size, color, life=1.0, decay=0.04):
        self.particles.append({
            "x": x, "y": y,
            "vx": vx, "vy": vy,
            "size": size, "color": color,
            "life": life, "decay": decay
        })

    def spawn_explosion(self, cx, cy, count=15, color_palette=None):
        if color_palette is None:
            color_palette = ["#00f0ff", "#ff0055", "#fcee0a"]
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.spawn_particle(
                cx, cy, vx, vy,
                random.randint(2, 4),
                random.choice(color_palette),
                life=1.0,
                decay=random.uniform(0.03, 0.06)
            )

    # --- Drawing Routines ---
    def draw_tech_frame(self, x1, y1, x2, y2, title="", active_color="#00f0ff"):
        """Draws standard Cyberpunk bevel-corner telemetry window panels."""
        d = 12
        corners = [
            x1 + d, y1,
            x2, y1,
            x2, y2 - d,
            x2 - d, y2,
            x1, y2,
            x1, y1 + d
        ]
        # Main structure
        self.canvas.create_polygon(corners, fill="#090a10", outline=active_color, width=1.5)
        # Small corner detail ticks
        self.canvas.create_line(x1 + d + 10, y1, x1 + d, y1, fill="#fcee0a", width=3)
        self.canvas.create_line(x2 - d - 10, y2, x2 - d, y2, fill="#fcee0a", width=3)
        
        # Frame Title
        if title:
            # Header bracket
            self.canvas.create_text(
                x1 + 15, y1 + 1,
                anchor="w",
                text=f"// {title.upper()}",
                fill="#07070a",
                font=("Consolas", 8, "bold")
            )
            # Background behind title text
            t_width = len(title) * 6 + 25
            self.canvas.create_polygon(
                [x1+d, y1-1, x1+t_width, y1-1, x1+t_width-5, y1+15, x1+d-5, y1+15],
                fill=active_color, outline=""
            )
            self.canvas.create_text(
                x1 + d + 5, y1 + 7,
                anchor="w",
                text=f"SYS.{title.upper()}",
                fill="#07070a",
                font=("Consolas", 8, "bold")
            )

    # --- UI Initializers ---
    def init_menu_widgets(self):
        self.buttons.clear()
        # Large central main boot button
        self.buttons.append(
            CyberCanvasButton(self.canvas, 375, 450, 575, 495, "BOOT SYSTEM", self.boot_system)
        )

    def init_game_widgets(self):
        self.buttons.clear()
        
        # --- Column 1: Game Modes ---
        # 510, 180 to 890, 210 (Widths: 120, margins: 10)
        self.buttons.append(
            CyberCanvasButton(self.canvas, 510, 180, 625, 210, "VS AI", 
                              lambda: self.change_mode("PVE"), is_toggle=True, is_selected=(self.engine.mode == "PVE"))
        )
        self.buttons.append(
            CyberCanvasButton(self.canvas, 635, 180, 750, 210, "VS HUMAN", 
                              lambda: self.change_mode("PVP"), is_toggle=True, is_selected=(self.engine.mode == "PVP"))
        )
        self.buttons.append(
            CyberCanvasButton(self.canvas, 760, 180, 875, 210, "SIMULATE", 
                              lambda: self.change_mode("EVE"), is_toggle=True, is_selected=(self.engine.mode == "EVE"))
        )

        # --- Column 2: AI Intellect (Only drawn in PVE) ---
        if self.engine.mode == "PVE":
            self.buttons.append(
                CyberCanvasButton(self.canvas, 510, 255, 625, 285, "CHIP IN", 
                                  lambda: self.change_difficulty("EASY"), is_toggle=True, is_selected=(self.engine.difficulty == "EASY"))
            )
            self.buttons.append(
                CyberCanvasButton(self.canvas, 635, 255, 750, 285, "NETRUNNER", 
                                  lambda: self.change_difficulty("MEDIUM"), is_toggle=True, is_selected=(self.engine.difficulty == "MEDIUM"))
            )
            self.buttons.append(
                CyberCanvasButton(self.canvas, 760, 255, 875, 285, "PSYCHO", 
                                  lambda: self.change_difficulty("HARD"), is_toggle=True, is_selected=(self.engine.difficulty == "HARD"))
            )

        # --- Column 3: Telemetry options ---
        self.buttons.append(
            CyberCanvasButton(self.canvas, 510, 330, 625, 360, "AUDIO", 
                              self.toggle_audio, is_toggle=True, is_selected=self.opt_sound)
        )
        self.buttons.append(
            CyberCanvasButton(self.canvas, 635, 330, 750, 360, "NETRUNNER", 
                              self.toggle_hacking, is_toggle=True, is_selected=self.opt_hacking)
        )
        self.buttons.append(
            CyberCanvasButton(self.canvas, 760, 330, 875, 360, "SCANLINES", 
                              self.toggle_crt, is_toggle=True, is_selected=self.opt_crt)
        )

        # --- Control panel base triggers ---
        # "REBOOT NEURAL GRID" or "START RUN" if in simulation
        reboot_text = "START SIMULATION" if (self.engine.mode == "EVE" and not self.simulation_running) else ("HALT SIMULATION" if self.simulation_running else "REBOOT GRID")
        self.buttons.append(
            CyberCanvasButton(self.canvas, 510, 610, 690, 645, reboot_text, self.trigger_reboot, active_color="#fcee0a")
        )
        self.buttons.append(
            CyberCanvasButton(self.canvas, 710, 610, 875, 645, "DISCONNECT", self.disconnect_system, active_color="#ff0055")
        )

    # --- Mode / Option Switchers ---
    def boot_system(self):
        SoundSynth.click()
        self.trigger_glitch(10)
        self.app_state = "GAME"
        self.engine.reset_board()
        self.log_message("SYS_LINK: GAME ENGINE ONLINE.")
        self.init_game_widgets()

    def disconnect_system(self):
        SoundSynth.click()
        self.trigger_glitch(10)
        self.app_state = "MENU"
        self.simulation_running = False
        self.log_message("SYS_LINK: NEURAL FEED DISCONNECTED.")
        self.init_menu_widgets()

    def change_mode(self, mode):
        self.engine.mode = mode
        self.simulation_running = False
        self.engine.reset_board()
        self.log_message(f"MODE: SWITCHED TO {mode}")
        self.init_game_widgets()
        self.trigger_glitch(4)

    def change_difficulty(self, diff):
        self.engine.difficulty = diff
        self.log_message(f"AI_CORE: COMPILING {diff} PROFILE")
        self.init_game_widgets()
        self.trigger_glitch(4)

    def toggle_audio(self):
        self.opt_sound = not self.opt_sound
        SoundSynth.enabled = self.opt_sound
        self.log_message(f"SYS_AUDIO: {'ENABLED' if self.opt_sound else 'MUTED'}")
        self.init_game_widgets()

    def toggle_hacking(self):
        self.opt_hacking = not self.opt_hacking
        self.log_message(f"NET_DECK: ANALYZER {'LOADED' if self.opt_hacking else 'PURGED'}")
        self.init_game_widgets()
        self.trigger_glitch(4)

    def toggle_crt(self):
        self.opt_crt = not self.opt_crt
        self.log_message(f"CRT_EMU: FILTER {'ON' if self.opt_crt else 'OFF'}")
        self.init_game_widgets()

    def trigger_reboot(self):
        if self.engine.mode == "EVE":
            self.simulation_running = not self.simulation_running
            if self.simulation_running:
                self.log_message("SIM_RUN: SIMULATION ROUTINE INITIATED.")
                self.sim_last_move_time = time.time()
            else:
                self.log_message("SIM_RUN: SIMULATION SUSPENDED.")
        else:
            self.engine.reset_board()
            self.log_message("GRID: REBOOT COMPLETE.")
        
        self.trigger_glitch(6)
        self.init_game_widgets()

    def trigger_glitch(self, duration=5):
        self.glitch_active = True
        self.glitch_end_frame = self.frame_count + duration
        SoundSynth.glitch()

    # --- Mouse and Logic Triggers ---
    def on_mouse_motion(self, event):
        mx, my = event.x, event.y
        
        # Check buttons hover
        button_state_changed = False
        for btn in self.buttons:
            if btn.check_hover(mx, my):
                button_state_changed = True

        if self.app_state == "GAME" and not self.simulation_running:
            # Check grid cells hover coordinates (50, 150) to (470, 570)
            if 50 <= mx <= 470 and 150 <= my <= 570:
                col = int((mx - 50) / 140)
                row = int((my - 150) / 140)
                cell_idx = row * 3 + col
                if 0 <= cell_idx < 9:
                    if self.engine.board[cell_idx] == "":
                        if self.hovered_cell != cell_idx:
                            self.hovered_cell = cell_idx
                            # Light spawn drifting ambient particles around hover cell
                            self.spawn_particle(
                                mx, my, 
                                random.uniform(-1, 1), random.uniform(-1, 1), 
                                random.randint(1, 2), "#00f0ff", 0.8, 0.05
                            )
                    else:
                        self.hovered_cell = None
                else:
                    self.hovered_cell = None
            else:
                self.hovered_cell = None

    def on_mouse_click(self, event):
        mx, my = event.x, event.y

        # Handle UI Button Clicks
        for btn in self.buttons:
            if btn.check_click(mx, my):
                return

        # Handle Tic Tac Toe Grid Clicks (if state is GAME and simulation is not automatically running)
        if self.app_state == "GAME" and not self.simulation_running:
            # Check grid coordinates
            if 50 <= mx <= 470 and 150 <= my <= 570:
                # Check if game is already over
                winner, _ = self.engine.check_winner()
                if winner is not None:
                    # Let click reboot board
                    self.engine.reset_board()
                    self.log_message("GRID: REBOOTING GAME...")
                    SoundSynth.click()
                    self.trigger_glitch(6)
                    return

                col = int((mx - 50) / 140)
                row = int((my - 150) / 140)
                cell_idx = row * 3 + col

                if 0 <= cell_idx < 9:
                    self.handle_player_move(cell_idx)

    def handle_player_move(self, index):
        active_p = self.engine.current_turn
        
        # Prevent moves during AI simulated turns in Single Player (if turn belongs to AI)
        if self.engine.mode == "PVE" and active_p == "O":
            return

        if self.engine.make_move(index):
            # Play beep corresponding to token
            if active_p == "X":
                SoundSynth.place_x()
            else:
                SoundSynth.place_o()

            # Particle explosion at cell center
            cx = 50 + (index % 3) * 140 + 70
            cy = 150 + int(index / 3) * 140 + 70
            self.spawn_explosion(cx, cy, 15, ["#ff0055"] if active_p == "X" else ["#00f0ff"])
            self.log_message(f"GRID: {active_p} CONNECTED AT SLOT {index}")
            self.hovered_cell = None

            # Check outcome
            winner, combo = self.engine.check_winner()
            if winner:
                self.handle_game_over(winner, combo)
            else:
                # Trigger PVE AI delayed response
                if self.engine.mode == "PVE" and self.engine.current_turn == "O":
                    self.log_message("AI_CORE: EXECUTING NEURAL PATHWAYS...")
                    # Set a delay trigger using tk.after to run the AI move asynchronously
                    self.root.after(500, self.execute_ai_turn)

    def execute_ai_turn(self):
        # Safety checks
        if self.app_state != "GAME" or self.engine.mode != "PVE" or self.engine.current_turn != "O":
            return
        winner, _ = self.engine.check_winner()
        if winner:
            return

        ai_move = self.engine.get_ai_move()
        if ai_move is not None:
            self.engine.make_move(ai_move)
            SoundSynth.place_o()

            cx = 50 + (ai_move % 3) * 140 + 70
            cy = 150 + int(ai_move / 3) * 140 + 70
            self.spawn_explosion(cx, cy, 15, ["#00f0ff"])
            self.log_message(f"AI: PLACED O AT SLOT {ai_move}")

            winner, combo = self.engine.check_winner()
            if winner:
                self.handle_game_over(winner, combo)

    def handle_game_over(self, winner, combo):
        if winner == "tie":
            self.engine.scores["ties"] += 1
            self.log_message("GRID: LINK DISSOLVED. A TIE.")
            SoundSynth.tie()
            self.trigger_glitch(8)
            # Explosion in center
            self.spawn_explosion(260, 360, 20, ["#fcee0a"])
        else:
            self.engine.scores[winner] += 1
            self.log_message(f"GRID: MATCH DECIDED. {winner} DOMINATES.")
            self.trigger_glitch(12)
            
            # Sound feedback based on outcome
            if self.engine.mode == "PVE":
                if winner == "X":
                    SoundSynth.victory()
                else:
                    SoundSynth.defeat()
            else:
                SoundSynth.victory()

            # Massive explosion along winning combo lines
            if combo:
                for idx in combo:
                    cx = 50 + (idx % 3) * 140 + 70
                    cy = 150 + int(idx / 3) * 140 + 70
                    self.spawn_explosion(cx, cy, 15, ["#ff0055"] if winner == "X" else ["#00f0ff"])

    # --- Render Engine and Frame Loop ---
    def update_loop(self):
        self.frame_count += 1
        
        # Handle glitch timeout
        if self.glitch_active and self.frame_count > self.glitch_end_frame:
            self.glitch_active = False

        # Clear canvas
        self.canvas.delete("all")

        # Handle simulation timer for EVE Mode
        if self.app_state == "GAME" and self.simulation_running:
            curr_time = time.time()
            if curr_time - self.sim_last_move_time > 0.8:
                # Run one step of simulation
                winner, _ = self.engine.check_winner()
                if winner:
                    # Restart simulation loop automatically
                    self.engine.reset_board()
                    self.log_message("SIM_RUN: REBOOTING GRID SIM.")
                    self.trigger_glitch(6)
                else:
                    active_ai = self.engine.current_turn
                    # Let the current active agent compute its move
                    # We toggle difficulty values for variation in EVE mode
                    if active_ai == "X":
                        # Simulate as a medium difficulty agent
                        self.engine.difficulty = "MEDIUM"
                    else:
                        self.engine.difficulty = "HARD"
                    
                    move = self.engine.get_ai_move()
                    if move is not None:
                        self.engine.make_move(move)
                        if active_ai == "X":
                            SoundSynth.place_x()
                        else:
                            SoundSynth.place_o()
                        cx = 50 + (move % 3) * 140 + 70
                        cy = 150 + int(move / 3) * 140 + 70
                        self.spawn_explosion(cx, cy, 12, ["#ff0055"] if active_ai == "X" else ["#00f0ff"])
                        self.log_message(f"SIM_{active_ai}: SLOT CONNECTOR {move} OK.")
                        
                        winner, combo = self.engine.check_winner()
                        if winner:
                            self.handle_game_over(winner, combo)
                
                self.sim_last_move_time = curr_time

        # --- Draw Background Grid / Stars ---
        self.draw_ambient_elements()

        # --- Draw Active Screens ---
        if self.app_state == "MENU":
            self.draw_menu_screen()
        elif self.app_state == "GAME":
            self.draw_game_screen()

        # --- Update and Draw Particles ---
        self.update_and_draw_particles()

        # --- Draw Static Screen Scanlines CRT Effect ---
        if self.opt_crt:
            self.draw_crt_overlay()

        # --- Draw Glitch Filters ---
        if self.glitch_active:
            self.draw_glitch_overlay()

        # Register next frame callback
        self.root.after(30, self.update_loop)

    def draw_ambient_elements(self):
        # Faint technological grid mesh
        grid_space = 40
        grid_offset = (self.frame_count * 0.5) % grid_space
        for x in range(int(grid_offset), 950, grid_space):
            self.canvas.create_line(x, 0, x, 700, fill="#0c0e18", width=1)
        for y in range(int(grid_offset), 700, grid_space):
            self.canvas.create_line(0, y, 950, y, fill="#0c0e18", width=1)
            
        # Draw background technology crosshairs and HUD elements
        self.canvas.create_line(15, 15, 40, 15, fill="#1c1e2d", width=1)
        self.canvas.create_line(15, 15, 15, 40, fill="#1c1e2d", width=1)
        self.canvas.create_line(935, 15, 910, 15, fill="#1c1e2d", width=1)
        self.canvas.create_line(935, 15, 935, 40, fill="#1c1e2d", width=1)
        self.canvas.create_line(15, 685, 40, 685, fill="#1c1e2d", width=1)
        self.canvas.create_line(15, 685, 15, 660, fill="#1c1e2d", width=1)
        self.canvas.create_line(935, 685, 910, 685, fill="#1c1e2d", width=1)
        self.canvas.create_line(935, 685, 935, 660, fill="#1c1e2d", width=1)

    def draw_menu_screen(self):
        # Draw tech title
        self.canvas.create_text(
            475, 230,
            text="TIC - TAC - TOE",
            fill="#fcee0a",
            font=("Impact", 48, "italic"),
            tags="menu_header"
        )
        self.canvas.create_text(
            475, 290,
            text="// NEURAL NETWORK GRID ACCESS_v.77",
            fill="#00f0ff",
            font=("Consolas", 12, "bold"),
            tags="menu_header"
        )
        
        # Subtle glowing panel box around title
        self.canvas.create_rectangle(
            220, 170, 730, 330,
            outline="#00f0ff", width=1.5
        )
        # Accent yellow dots
        self.canvas.create_rectangle(218, 168, 224, 174, fill="#fcee0a", outline="")
        self.canvas.create_rectangle(726, 326, 732, 332, fill="#fcee0a", outline="")

        # Connecting simulation string
        sys_dots = "." * (int(self.frame_count / 8) % 4)
        self.canvas.create_text(
            475, 380,
            text=f"INITIALIZING NEURO-LINK{sys_dots}",
            fill="#ff0055",
            font=("Consolas", 10, "bold")
        )
        
        # Redraw Boot button
        for btn in self.buttons:
            btn.draw()

    def draw_game_screen(self):
        # 1. Main Header bar
        self.canvas.create_rectangle(50, 45, 900, 95, fill="#090a10", outline="#00f0ff", width=1.5)
        # Diagonal cuts on top panel
        self.canvas.create_polygon(
            [48, 43, 85, 43, 90, 48, 48, 48], fill="#ff0055"
        )
        self.canvas.create_text(
            65, 70,
            anchor="w",
            text="NETRUNNER_TAC_TOE // NODE_77",
            fill="#fcee0a",
            font=("Consolas", 16, "bold"),
            tags="header"
        )
        
        # Floating system clock representation
        time_str = time.strftime("%H:%M:%S")
        self.canvas.create_text(
            885, 70,
            anchor="e",
            text=f"SYS_TIME: {time_str}",
            fill="#00f0ff",
            font=("Consolas", 11, "bold"),
            tags="header"
        )

        # 2. Main Tic Tac Toe Board (Left Area: 50, 150 to 470, 570)
        self.draw_ttt_board()

        # 3. Control Panel Telemetry Boxes (Right Area)
        # Telemetry panel wrapper
        self.draw_tech_frame(500, 130, 900, 660, "GRID CONTROL DECK", "#00f0ff")

        # Game Mode Label
        self.canvas.create_text(510, 165, anchor="w", text="SELECT LINK PROTOCOL", fill="#00f0ff", font=("Consolas", 8, "bold"), tags="status_hud")
        
        # AI Intellect Label (PVE only)
        if self.engine.mode == "PVE":
            self.canvas.create_text(510, 240, anchor="w", text="AI NEURAL CAPABILITY", fill="#00f0ff", font=("Consolas", 8, "bold"), tags="status_hud")

        # Toggles Label
        self.canvas.create_text(510, 315, anchor="w", text="HUD VISUAL TELEMETRY", fill="#00f0ff", font=("Consolas", 8, "bold"), tags="status_hud")

        # Redraw control buttons
        for btn in self.buttons:
            btn.draw()

        # 4. Score board panel (510, 390 to 890, 470)
        self.draw_tech_frame(510, 385, 890, 475, "NEURAL INTERGRITY METRICS", "#fcee0a")
        
        # Labels and scores
        # We compute visual spacing
        self.canvas.create_text(
            530, 420, anchor="w",
            text=f"PLAYER [X]: {self.engine.scores['X']}",
            fill="#ff0055", font=("Consolas", 12, "bold"), tags="score_hud"
        )
        self.canvas.create_text(
            660, 420, anchor="w",
            text=f"AI/OPP [O]: {self.engine.scores['O']}",
            fill="#00f0ff", font=("Consolas", 12, "bold"), tags="score_hud"
        )
        self.canvas.create_text(
            800, 420, anchor="w",
            text=f"TIES: {self.engine.scores['ties']}",
            fill="#fcee0a", font=("Consolas", 12, "bold"), tags="score_hud"
        )
        
        # Small diagnostic bars under scores
        self.canvas.create_rectangle(530, 440, 620, 445, outline="#ff0055", fill="#230a13")
        self.canvas.create_rectangle(660, 440, 750, 445, outline="#00f0ff", fill="#0a2128")
        self.canvas.create_rectangle(800, 440, 870, 445, outline="#fcee0a", fill="#212007")

        # Fill diagnostic bars based on ratio (just simple visual juice)
        total = self.engine.scores['X'] + self.engine.scores['O'] + self.engine.scores['ties']
        if total > 0:
            px = 90 * (self.engine.scores['X'] / total)
            po = 90 * (self.engine.scores['O'] / total)
            pt = 70 * (self.engine.scores['ties'] / total)
            if px > 0: self.canvas.create_rectangle(530, 440, 530 + px, 445, fill="#ff0055", outline="")
            if po > 0: self.canvas.create_rectangle(660, 440, 660 + po, 445, fill="#00f0ff", outline="")
            if pt > 0: self.canvas.create_rectangle(800, 440, 800 + pt, 445, fill="#fcee0a", outline="")

        # 5. Terminal CLI log box (510, 490 to 890, 590)
        self.draw_tech_frame(510, 490, 890, 595, "DECK BUFFER LOGS", "#ff0055")
        
        # Roll the console messages
        for idx, log in enumerate(self.logs):
            # Monospace text inside logs terminal
            self.canvas.create_text(
                525, 515 + idx * 14,
                anchor="w",
                text=log,
                fill="#5bf26a" if idx == len(self.logs)-1 else "#36a341", # glowing green latest log
                font=("Consolas", 8),
                tags="terminal"
            )
        # Blinking console cursor at the end of last log
        if int(self.frame_count / 10) % 2 == 0 and self.logs:
            last_y = 515 + (len(self.logs)-1) * 14
            last_text = self.logs[-1]
            cursor_offset = len(last_text) * 5.6 + 525 # rough monospace character spacing estimation
            self.canvas.create_line(cursor_offset, last_y - 5, cursor_offset, last_y + 6, fill="#5bf26a", width=2, tags="terminal")

        # 6. Technical footer subtext
        sys_status = "AI COMPILING..." if (self.engine.mode == "PVE" and self.engine.current_turn == "O") else ("SIMULATING RUN..." if self.simulation_running else "GRID LINK STABLE")
        self.canvas.create_text(
            50, 640, anchor="w",
            text=f"SYS_LOAD: 34% // SECTOR: NIGHT_CITY_NET // STABLE_RATIO: 99.8% // {sys_status}",
            fill="#3e4359", font=("Consolas", 8), tags="status_hud"
        )

    def draw_ttt_board(self):
        # Draw outer boundary bevelled telemetry box
        self.draw_tech_frame(45, 145, 475, 575, "NEURAL MATRIX", "#00f0ff")

        # 3x3 Grid Lines with Neon Glow Tube simulation (Cyan)
        # Vertical grid separators at cols x = 190, 330
        for x in [190, 330]:
            # Neon Outer Glow (faint wider line)
            self.canvas.create_line(x, 155, x, 565, fill="#042a38", width=9)
            self.canvas.create_line(x, 155, x, 565, fill="#08546a", width=5)
            # Neon Core Line
            self.canvas.create_line(x, 155, x, 565, fill="#00f0ff", width=2)
            
        # Horizontal grid separators at rows y = 290, 430
        for y in [290, 430]:
            # Neon Outer Glow
            self.canvas.create_line(55, y, 465, y, fill="#042a38", width=9)
            self.canvas.create_line(55, y, 465, y, fill="#08546a", width=5)
            # Neon Core Line
            self.canvas.create_line(55, y, 465, y, fill="#00f0ff", width=2)

        # Draw cells (Markers X, O and Scan probabilities)
        winner, win_combo = self.engine.check_winner()

        for idx, cell in enumerate(self.engine.board):
            col = idx % 3
            row = int(idx / 3)
            # Center of the cell
            cx = 50 + col * 140 + 70
            cy = 150 + row * 140 + 70

            # --- Cell Hover ghost marker or hacking scan results ---
            if cell == "":
                # 1. Netrunner Grid Hacking analyzer (Minimax visualizer)
                if self.opt_hacking and winner is None:
                    prob = self.engine.scan_cell_probability(idx)
                    if prob is not None:
                        # Decide color and string
                        if prob > 0:
                            p_color = "#00ff66" # Green: guaranteed win for active player
                            p_str = "[WIN]"
                        elif prob == 0:
                            p_color = "#fcee0a" # Yellow: guaranteed draw
                            p_str = "[TIE]"
                        else:
                            p_color = "#ff0055" # Red: guaranteed loss
                            p_str = "[LOSS]"

                        self.canvas.create_text(
                            cx + 45, cy + 50,
                            anchor="se",
                            text=p_str,
                            fill=p_color,
                            font=("Consolas", 8, "bold"),
                            tags="scanner"
                        )
                
                # 2. Draw hover ghost preview marker
                if idx == self.hovered_cell and winner is None:
                    active_p = self.engine.current_turn
                    self.draw_cell_marker(cx, cy, active_p, ghost=True)
            
            else:
                # Draw permanent solid placed marker
                is_win_cell = (win_combo and idx in win_combo)
                self.draw_cell_marker(cx, cy, cell, ghost=False, winning=is_win_cell)

        # --- Draw Glowing Winning Strike Line ---
        if winner and winner != "tie" and win_combo:
            c1, c2, c3 = win_combo
            col1, row1 = c1 % 3, int(c1 / 3)
            col3, row3 = c3 % 3, int(c3 / 3)
            
            # Start/End coords
            x1 = 50 + col1 * 140 + 70
            y1 = 150 + row1 * 140 + 70
            x2 = 50 + col3 * 140 + 70
            y2 = 150 + row3 * 140 + 70

            # Pulsing color width calculation
            glow_width = 11 + math.sin(self.frame_count * 0.3) * 3
            
            # Neon beam strike (Yellow/Orange Cyber style)
            self.canvas.create_line(x1, y1, x2, y2, fill="#521d05", width=glow_width + 4)
            self.canvas.create_line(x1, y1, x2, y2, fill="#b54308", width=glow_width)
            self.canvas.create_line(x1, y1, x2, y2, fill="#fcee0a", width=3)
            self.canvas.create_line(x1, y1, x2, y2, fill="#ffffff", width=1.5)

            # Draw "SYS_OVERLOAD MATCH_COMPLETED" text tag
            self.canvas.create_rectangle(
                160, 335, 360, 385,
                fill="#07070a", outline="#ff0055", width=2
            )
            self.canvas.create_text(
                260, 360,
                text=f"{winner} VICTORY".upper(),
                fill="#fcee0a",
                font=("Impact", 20, "italic")
            )
            
        elif winner == "tie":
            # Draw tie dialog overlay
            self.canvas.create_rectangle(
                160, 335, 360, 385,
                fill="#07070a", outline="#fcee0a", width=2
            )
            self.canvas.create_text(
                260, 360,
                text="SYSTEM TIE",
                fill="#ff0055",
                font=("Impact", 20, "italic")
            )

    def draw_cell_marker(self, cx, cy, token, ghost=False, winning=False):
        size = 35 # bounding half-width
        
        if token == "X":
            # Magenta / Hot Pink Neon glow theme
            line_c = "#ff0055"
            glow_c_outer = "#350512"
            glow_c_inner = "#75092a"
            
            if ghost:
                line_c = "#571325"
                glow_c_outer = ""
                glow_c_inner = ""
            elif winning:
                # Turn winning marks neon yellow/white
                line_c = "#ffffff"
                glow_c_outer = "#b54308"
                glow_c_inner = "#fcee0a"

            # Draw Line 1 (Top-Left to Bottom-Right)
            if glow_c_outer:
                self.canvas.create_line(cx - size, cy - size, cx + size, cy + size, fill=glow_c_outer, width=10)
                self.canvas.create_line(cx - size, cy - size, cx + size, cy + size, fill=glow_c_inner, width=5)
            self.canvas.create_line(cx - size, cy - size, cx + size, cy + size, fill=line_c, width=3.5)
            
            # Draw Line 2 (Bottom-Left to Top-Right)
            if glow_c_outer:
                self.canvas.create_line(cx - size, cy + size, cx + size, cy - size, fill=glow_c_outer, width=10)
                self.canvas.create_line(cx - size, cy + size, cx + size, cy - size, fill=glow_c_inner, width=5)
            self.canvas.create_line(cx - size, cy + size, cx + size, cy - size, fill=line_c, width=3.5)

        elif token == "O":
            # Cyan / Neon Blue glow theme
            line_c = "#00f0ff"
            glow_c_outer = "#052d35"
            glow_c_inner = "#096075"

            if ghost:
                line_c = "#144e54"
                glow_c_outer = ""
                glow_c_inner = ""
            elif winning:
                # Turn winning marks neon yellow/white
                line_c = "#ffffff"
                glow_c_outer = "#b54308"
                glow_c_inner = "#fcee0a"

            # Draw Oval
            if glow_c_outer:
                self.canvas.create_oval(cx - size, cy - size, cx + size, cy + size, outline=glow_c_outer, width=10)
                self.canvas.create_oval(cx - size, cy - size, cx + size, cy + size, outline=glow_c_inner, width=5)
            self.canvas.create_oval(cx - size, cy - size, cx + size, cy + size, outline=line_c, width=3.5)

    # --- CRT Scanline Visual Filters ---
    def draw_crt_overlay(self):
        # 1. Ambient CRT Phosphor flicker
        flicker_alpha = random.uniform(0.01, 0.04)
        self.canvas.create_rectangle(
            0, 0, 950, 700,
            fill="#00f0ff" if random.random() < 0.003 else "#ff0055",
            outline="",
            stipple="gray12" # Built-in Tkinter dither pattern
        )

        # 2. Moving scanline beam (V-Blank scroll)
        beam_y = (self.frame_count * 3) % 700
        self.canvas.create_rectangle(
            0, beam_y, 950, beam_y + 120,
            fill="#ffffff", outline="",
            stipple="gray12"
        )
        
        # 3. Faint static CRT scanline rows
        # Drawing too many lines creates lag, so we draw thick bars spaced 12px
        for sy in range(0, 700, 16):
            self.canvas.create_line(0, sy, 950, sy, fill="#040406", width=1.5)

    # --- Glitch Visual Overlays ---
    def draw_glitch_overlay(self):
        # 1. Colored glitch blocks
        for _ in range(random.randint(2, 5)):
            gx = random.randint(0, 900)
            gy = random.randint(0, 680)
            gw = random.randint(30, 300)
            gh = random.randint(2, 20)
            color = random.choice(["#ff0055", "#00f0ff", "#fcee0a", "#ffffff"])
            self.canvas.create_rectangle(
                gx, gy, gx + gw, gy + gh,
                fill=color, outline=""
            )

        # 2. Chromatic aberration simulations on text tags (Glitch duplication)
        clones = []
        for tag in ["header", "score_hud", "terminal"]:
            items = self.canvas.find_withtag(tag)
            for item in items:
                if self.canvas.type(item) == "text":
                    txt = self.canvas.itemcget(item, "text")
                    coords = self.canvas.coords(item)
                    font_val = self.canvas.itemcget(item, "font")
                    anchor_val = self.canvas.itemcget(item, "anchor")
                    clones.append((coords, txt, font_val, anchor_val))

        for coord, txt, f_val, a_val in clones:
            dx = random.randint(-4, 4)
            # Red clone left
            self.canvas.create_text(
                coord[0] + dx, coord[1],
                text=txt, font=f_val, anchor=a_val,
                fill="#ff0055"
            )
            # Cyan clone right
            self.canvas.create_text(
                coord[0] - dx, coord[1],
                text=txt, font=f_val, anchor=a_val,
                fill="#00f0ff"
            )

    # --- Ambient Dust Particles Update Loop ---
    def update_and_draw_particles(self):
        # Filter dead particles
        self.particles = [p for p in self.particles if p["life"] > 0]
        
        for p in self.particles:
            # physics step
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            
            # decelerate friction slightly
            p["vx"] *= 0.96
            p["vy"] *= 0.96
            
            # float up slightly if ambient dust
            p["vy"] -= 0.01
            
            # apply life decay
            p["life"] -= p["decay"]
            
            if p["life"] > 0:
                # Render particle on canvas
                sz = p["size"] * p["life"]
                if sz < 0.5: sz = 0.5
                self.canvas.create_oval(
                    p["x"] - sz, p["y"] - sz,
                    p["x"] + sz, p["y"] + sz,
                    fill=p["color"], outline=""
                )

        # Repopulate ambient background dust
        if len(self.particles) < 30:
            self.spawn_particle(
                random.randint(10, 940), 690,
                random.uniform(-0.4, 0.4), random.uniform(-1.0, -0.2),
                random.randint(1, 3), random.choice(["#00f0ff", "#ff0055", "#fcee0a"]),
                life=1.0, decay=0.004
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = CyberpunkApp(root)
    root.mainloop()
