import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import customtkinter as ctk
import importlib.resources as pkg_resources

from cycler import cycler
cmap = plt.get_cmap("gnuplot")
multicolor = [cmap(i) for i in np.linspace(0.1, 0.9, 12)]

ctk.set_appearance_mode("light")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sns.set_style("ticks")
sns.set_context("talk", font_scale=0.8)
plt.rcParams['font.family'] = 'Aller'

def get_theme_path():
    path = str(pkg_resources.files("plateviz") / "Goldilocks.json")
    return path

ctk.set_default_color_theme(get_theme_path())

VERSION = '1.1.3'
AUTHOR = '@Radium2000'
BRAND = 'plateviz by Radium2000'

class PlateApp(ctk.CTk):
    def __init__(self, channels):
        
        super().__init__()

        self.channels = np.array(channels)
        self.color_cycle = plt.cycler(color=["#3C73C5", '#fb4b4e', "#37b632", "#7D42E2"])
        plt.rcParams['axes.prop_cycle'] = cycler(color=multicolor)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.geometry("800x765")
        self.resizable(False, True)
        
        self.title("Plate Viz")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # MAIN FRAME
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # CHECKBOX FRAME
        self.extras_frame = ctk.CTkFrame(self.main_frame, corner_radius=6)
        self.extras_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')
        self.checkbox_label = ctk.CTkLabel(self.extras_frame, text="Channels",
                                           font=("Aller", 16, "bold"))
        self.checkbox_label.grid(row=0, column=0)
        
        # CHANNEL CHECKBOXES
        self.checkboxes = {}
        self.checkbox_states = {} # stores states of the checkboxes
        for i, channel in enumerate(channels):
            cb_state = ctk.BooleanVar(value=False)
            self.checkbox_states[channel] = cb_state
            self.checkboxes[channel] = ctk.CTkCheckBox(
                self.extras_frame, 
                text=channel,
                font=("Aller", 14),
                variable=cb_state
            )
            self.checkboxes[channel].grid(row=i+1, column=0, padx=10, pady=5, sticky='w')
        
        # INTERACTIVE MODE SWITCH
        self.int_state = ctk.BooleanVar(value=False)
        self.interact_switch = ctk.CTkSwitch(self.extras_frame, text="Interactive",
                                           font=("Aller", 16, "bold"),
                                           variable=self.int_state
                                           )
        self.interact_switch.grid(row=len(channels)+1, column=0, padx=10, pady=15, sticky='w')   

        # MULTIWELL SWITCH
        self.mw_state = ctk.BooleanVar(value=False)
        self.multiwell_switch = ctk.CTkSwitch(self.extras_frame, text="Multi Well",
                                           font=("Aller", 16, "bold"), 
                                           variable=self.mw_state
                                           )
        self.multiwell_switch.grid(row=len(channels)+2, column=0, padx=10, pady=15, sticky='w')

        # CLEAR PLOT BUTTON
        clr_btn = ctk.CTkButton(
            self.extras_frame,
            text="Clear Plot",
            font=("Aller", 16, "bold"),
            command=self.clear_frame
        )
        clr_btn.grid(row=len(channels)+3, column=0, padx=10, pady=15)

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
                    command=lambda x=j, y=i: self.on_button_click(x, y,
                                                                  self.checkbox_states,
                                                                  self.mw_state,
                                                                  self.int_state)
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
        self.ax.grid(True)
        
        # embed the figure
        self.canvas_frame = ctk.CTkFrame(self.main_frame)
        self.canvas_frame.grid(row=2, column=0, padx=10, pady=10)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
    
    def clear_frame(self):
        self.ax.clear()
        self.ax.grid(True)
        self.canvas.draw()
    
    def on_closing(self):
        plt.close(self.fig)
        self.quit()
        self.destroy()

    def on_button_click(self, x, y, cb_states,  mw_state, int_state):

        current_states = [var.get() for _, var in cb_states.items()]
        
        # checking whether all channels are deselected
        if np.array(current_states).any() == False:
            self.ax.clear()
            self.ax.set_prop_cycle(self.color_cycle)
            self.ax.grid(True)
            self.ax.set_title(BRAND, fontsize=14, color='#57311a')
            self.ax.text(0.5, 0.5, "Select a channel to start plotting", 
                         transform=self.ax.transAxes,
                         horizontalalignment='center', verticalalignment='center',
                         fontsize=16, color='#57311a')
            self.canvas.draw()

        else:
            to_plot = self.channels[current_states]
            # Checking state of multiwell_switch
            if mw_state.get() == False:
                # If Interactive Mode is on
                if int_state.get():
                    plt.close(self.fig)
                    new_fig, new_ax = plt.subplots()
                    new_ax.clear()
                    new_ax.set_prop_cycle(self.color_cycle)
                    new_ax.set_title(f'{chr(65+y)}{x+1}', color='#57311a')
                    new_ax.grid(True)
                    for channel in to_plot:
                        new_ax.scatter(*np.random.uniform(0,1,size=2), s=100, label=channel)
                        new_ax.legend(loc='best', fontsize='x-small')
                    plt.show(block=False)
                else:
                    self.ax.clear()
                    self.ax.set_prop_cycle(self.color_cycle)
                    self.ax.set_title(f'{chr(65+y)}{x+1}', color='#57311a')
                    self.ax.grid(True)
                    for channel in to_plot:
                        self.ax.scatter(*np.random.uniform(0,1,size=2), s=100, label=channel)
                        self.ax.legend(loc='best', fontsize='x-small')
                    self.canvas.draw()
            else:
                # checking whether current plot is part of multiwell
                _, labels = self.ax.get_legend_handles_labels()
                check_multi = True
                for item in self.channels:
                    if item in labels:
                        check_multi = False
                if check_multi==False or self.ax.get_title()==BRAND:
                    self.ax.clear()

                # checking if that well has already been plotted
                plotted_wells = [label.split(":")[1] for label in labels]
                if chr(65+y)+str(x+1) not in plotted_wells:
                    self.ax.set_title("Multi-Well Plotting", color='#57311a')
                    self.ax.grid(True)
                    for channel in to_plot:
                        if len(labels)<=13:
                            self.ax.scatter(*np.random.uniform(0,1,size=2), s=100,
                                            label=f'{channel}:{chr(65+y)}{x+1}')
                        else:
                            self.ax.scatter(*np.random.uniform(0,1,size=2), s=100)
                        self.ax.legend(loc='best', fontsize='xx-small')
                    self.canvas.draw()

def plateDisplay(channels):
    app = PlateApp(channels=channels)
    app.mainloop()

# plateDisplay(['OD', 'Venus', 'Cerulean'])