import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import customtkinter as ctk
import importlib.resources as pkg_resources

ctk.set_appearance_mode("light")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sns.set_style("ticks")
sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 2})
plt.rcParams['font.family'] = 'Aller'
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#335C67', "#FFFFFF", '#fb4b4e', '#3b3355'])

def get_theme_path():
    path = str(pkg_resources.files("plateviz") / "Goldilocks.json")
    return path

ctk.set_default_color_theme(get_theme_path())

class PlateApp(ctk.CTk):
    def __init__(self, channels):
        super().__init__()
        with pkg_resources.path("plateviz.resources", "pv_icon.ico") as icon_path:
            self.iconbitmap(default=str(icon_path))

        self.channels = np.array(channels)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry("790x765")
        self.resizable(False, True)
        
        self.title("Plate Viz")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # MAIN FRAME
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # CHECKBOX FRAME
        self.checkbox_frame = ctk.CTkFrame(self.main_frame, corner_radius=6)
        self.checkbox_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')
        self.checkbox_label = ctk.CTkLabel(self.checkbox_frame, text="Channels",
                                           font=("Aller", 16, "bold"))
        self.checkbox_label.grid(row=0, column=0)
        
        # CHANNEL CHECKBOXES
        self.checkboxes = {}
        self.checkbox_states = {} # stores states of the checkboxes
        for i, channel in enumerate(channels):
            cb_state = ctk.BooleanVar(value=False)
            self.checkbox_states[channel] = cb_state
            self.checkboxes[channel] = ctk.CTkCheckBox(
                self.checkbox_frame, 
                text=channel,
                font=("Aller", 14),
                variable=cb_state
            )
            self.checkboxes[channel].grid(row=i+1, column=0, padx=10, pady=5, sticky='w')
        
        # INTERACTIVE MODE SWITCH
        self.enable_switch = ctk.CTkSwitch(self.checkbox_frame, text="Interactive",
                                           font=("Aller", 16, "bold")
                                           )
        self.enable_switch.grid(row=len(channels)+1, column=0, padx=10, pady=15)    

        # BUTTON FRAME
        self.button_frame = ctk.CTkFrame(self.main_frame, corner_radius=6)
        self.button_frame.grid(row=0, column=0, padx=10, pady=10)
        
        # column labels
        for j in range(12):
            label = ctk.CTkLabel(self.button_frame, text=str(j+1),
                                 font=("Aller", 14, "bold"))
            label.grid(row=0, column=j+1, padx=2, pady=2)
        
        # row labels
        for i in range(8):
            label = ctk.CTkLabel(self.button_frame, text=chr(65+i),
                                 font=("Aller", 14, "bold"))
            label.grid(row=i+1, column=0, padx=2, pady=2)
        
        # WELL BUTTONS
        for i in range(8):
            for j in range(12):
                btn = ctk.CTkButton(
                    self.button_frame,
                    text="",
                    width=30,
                    height=30,
                    corner_radius=15,
                    command=lambda x=j, y=i: self.on_button_click(x, y, self.checkbox_states)
                )
                btn.grid(row=i+1, column=j+1, padx=2, pady=2)
        
        # FIGURE AND CANVAS
        self.fig, self.ax = plt.subplots(figsize=(6, 4), facecolor='#fce5b7')
        self.ax.set_facecolor('#fce5b7')
        self.ax.grid(True, color='#57311a', alpha=0.3)
        self.ax.spines['bottom'].set_color('#57311a')
        self.ax.spines['top'].set_color('#57311a')
        self.ax.spines['right'].set_color('#57311a')
        self.ax.spines['left'].set_color('#57311a')
        self.ax.tick_params(colors='#57311a')
        self.ax.set_xlim(-0.5, 11.5)
        self.ax.set_ylim(-0.5, 7.5)
        self.ax.grid(True)
        
        # embed the figure
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.grid(row=2, column=0, padx=10, pady=10)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
    
    def on_closing(self):
        plt.close(self.fig)
        self.quit()
        self.destroy()

    def on_button_click(self, x, y, states):
        current_states = [var.get() for _, var in states.items()]
        to_plot = self.channels[current_states]
        self.ax.clear()
        self.ax.set_title(f'{chr(65+y)}{x+1}')
        self.ax.grid(True)
        for channel in to_plot:
            self.ax.scatter(*np.random.uniform(0,5,size=2), s=100, label=channel)
            self.ax.legend(loc='best', fontsize='x-small')
        self.canvas.draw()

    def on_channel_click(self, channel):
        # ('A', 1, 'channel_name')
        print(channel)

def plateDisplay(channels):
    app = PlateApp(channels=channels)
    app.mainloop()

VERSION = '1.1.2'
AUTHOR = 'Radium2000'

plateDisplay(['OD', 'Venus', 'Cerulean'])