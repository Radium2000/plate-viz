import matplotlib.pyplot as plt
import seaborn as sns
import customtkinter as ctk

ctk.set_appearance_mode("light")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sns.set_style("ticks")
sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 2})
plt.rcParams['font.family'] = 'Aller'

import importlib.resources as pkg_resources

def get_theme_path():
    return str(pkg_resources.files("plateviz") / "Goldilocks.json")

ctk.set_default_color_theme(get_theme_path())

class PlateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry("630x775")
        self.resizable(False, True)    
        
        self.title("Grid Plot App")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Create button frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Add column labels (1-12)
        for j in range(12):
            label = ctk.CTkLabel(self.button_frame, text=str(j+1),
                                 font=("Aller", 14, "bold"))
            label.grid(row=0, column=j+1, padx=2, pady=2)
        
        # Add row labels (A-H)
        for i in range(8):
            label = ctk.CTkLabel(self.button_frame, text=chr(65+i),
                                 font=("Aller", 14, "bold"))  # 65 is ASCII for 'A'
            label.grid(row=i+1, column=0, padx=2, pady=2)
        
        # Create buttons (shifted by 1 row and column to make room for labels)
        for i in range(8):
            for j in range(12):
                btn = ctk.CTkButton(
                    self.button_frame,
                    text="",
                    width=30,
                    height=30,
                    corner_radius=15,
                    command=lambda x=j, y=i: self.button_click(x, y)
                )
                btn.grid(row=i+1, column=j+1, padx=2, pady=2)
        
        # Create figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(6, 4), facecolor='#fce5b7')
        self.ax.set_facecolor('#fce5b7')
        self.ax.grid(True, color='#57311a', alpha=0.3)  # Added color and transparency
        self.ax.spines['bottom'].set_color('#57311a')
        self.ax.spines['top'].set_color('#57311a')
        self.ax.spines['right'].set_color('#57311a')
        self.ax.spines['left'].set_color('#57311a')
        self.ax.tick_params(colors='#57311a')
        self.ax.set_xlim(-0.5, 11.5)
        self.ax.set_ylim(-0.5, 7.5)
        self.ax.grid(True)
        
        # Create canvas frame and embed figure
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.grid(row=1, column=0, padx=10, pady=10)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
    
    def on_closing(self):
        plt.close(self.fig)  # Close the matplotlib figure
        self.quit()  # Stop the mainloop
        self.destroy()  # Destroy the window

    def button_click(self, x, y):
        self.ax.clear()
        self.ax.set_title(f'{chr(65+y)}{x+1}')
        self.ax.set_xlim(-0.5, 11.5)
        self.ax.set_ylim(-0.5, 7.5)
        self.ax.grid(True)
        self.ax.scatter(x, 7-y, color='#57311a', s=100)
        self.canvas.draw()

def plateDisplay():
    app = PlateApp()
    app.mainloop()

VERSION = '0.1.0'
AUTHOR = 'Rudra Kalra'