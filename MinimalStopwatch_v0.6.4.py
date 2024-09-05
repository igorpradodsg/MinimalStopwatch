import os
import sys
import tkinter as tk
from tkinter import ttk
import time

def resource_path(relative_path):
    """Obter o caminho absoluto para o recurso, funcionando tanto em dev quanto no executável empacotado"""
    try:
        # PyInstaller usa uma pasta temporária e armazena o caminho do arquivo nela
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Cronometro:
    def __init__(self, root, opacidade=0.9):
        self.root = root
        self.root.geometry("250x50")
        # root.iconbitmap("ms-icon.ico")
        root.iconbitmap(sys.executable) # Load the current executable icon into the window.
        self.root.configure(bg='gray20')
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", opacidade)  # Ajusta a opacidade da janela

        # Define o TÍTULO da aplicação (nome que aparecerá no Gerenciador de Tarefas)
        self.root.title("Minimal Stopwatch")

        # Define o ÍCONE da aplicação
        self.root.iconbitmap("D:\\ms-icon.ico")
        
        # Faixa para arrastar a janela
        self.drag_bar = tk.Frame(self.root, height=10, bg='#F28021', cursor="fleur")
        self.drag_bar.pack(fill=tk.X, side=tk.TOP)
        self.drag_bar.bind("<B1-Motion>", self.move_window)
        self.drag_bar.bind("<Button-1>", self.get_pos)

        self.running = False
        self.reset_time = True
        self.start_time = 0
        self.elapsed_time = 0

        # Variável para o botão de fechar
        self.close_button_held = False
        self.close_start_time = 0
        self.close_hold_duration = 1000  # 1 segundo em milissegundos

        self.display = tk.Label(self.root, text="00:00:00,00", font=("Helvetica", 16), fg="white", bg="gray20")
        self.display.pack(side=tk.LEFT, padx=(10, 5))

        self.play_button = tk.Button(self.root, text="▶", command=self.toggle, font=("Helvetica", 14), fg="white", bg="gray20", bd=0)
        self.play_button.pack(side=tk.LEFT, padx=(5, 0))

        self.reset_button = tk.Button(self.root, text="⟲", command=self.reset, font=("Helvetica", 14), fg="white", bg="gray20", bd=0)
        self.reset_button.pack(side=tk.LEFT, padx=(5, 0))

        self.close_button = tk.Button(self.root, text="✖", font=("Helvetica", 14), fg="white", bg="gray20", bd=0)
        self.close_button.bind("<ButtonPress-1>", self.start_closing)
        self.close_button.bind("<ButtonRelease-1>", self.stop_closing)
        self.close_button.pack(side=tk.LEFT, padx=(5, 10))

        self.update_clock()

    def move_window(self, event):
        x = event.x_root - self.x_start
        y = event.y_root - self.y_start
        self.root.geometry(f"+{x}+{y}")

    def get_pos(self, event):
        self.x_start = event.x
        self.y_start = event.y

    def start_closing(self, event):
        self.close_button_held = True
        self.close_start_time = time.time()
        self.update_closing()

    def stop_closing(self, event):
        self.close_button_held = False

    def update_closing(self):
        if self.close_button_held:
            elapsed = (time.time() - self.close_start_time) * 1000  # Convertendo para milissegundos
            if elapsed >= self.close_hold_duration:
                self.root.destroy()
            else:
                # Adiciona uma barra de progresso circular ao redor do botão ou do mouse
                self.close_button.config(text="⦿" * int((elapsed / self.close_hold_duration) * 10))
                self.root.after(100, self.update_closing)
        else:
            self.close_button.config(text="✖")

    def toggle(self):
        if self.running:
            self.running = False
            self.play_button.config(text="▶")
        else:
            self.running = True
            if self.reset_time:
                self.start_time = time.time()
                self.reset_time = False
            else:
                self.start_time = time.time() - self.elapsed_time
            self.play_button.config(text="⏸")

    def reset(self):
        self.running = False
        self.reset_time = True
        self.elapsed_time = 0
        self.play_button.config(text="▶")
        self.display.config(text="00:00:00,00")

    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            hours, rem = divmod(self.elapsed_time, 3600)
            minutes, rem = divmod(rem, 60)
            seconds, milliseconds = divmod(rem, 1)
            time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds * 100):02}"
            self.display.config(text=time_str)

        self.root.after(10, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    cronometro = Cronometro(root, opacidade=0.65)  # Define a opacidade como 90%
    root.mainloop()
