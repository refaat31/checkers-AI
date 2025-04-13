import tkinter as tk
from tkinter import messagebox
from player_stats import PlayerStats

def update_display():
    stats = PlayerStats()
    stats_text.delete(1.0, tk.END)
    stats_text.insert(tk.END, stats.get_stats_summary())
    
    name_label.config(text=f"Player: {stats.stats['player_name']}")

#create the main window
root = tk.Tk()
root.title("Checkers Statistics Viewer")
root.geometry("500x450")
root.resizable(False, False)

#create a frame for the title
title_frame = tk.Frame(root)
title_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="Checkers Statistics", font=("Arial", 16, "bold"))
title_label.pack()

#create a frame for the player name
name_frame = tk.Frame(root)
name_frame.pack(pady=10)

name_label = tk.Label(name_frame, text="Player: Unknown", font=("Arial", 12))
name_label.pack()

#create a frame for the statistics display
stats_frame = tk.Frame(root)
stats_frame.pack(pady=10, fill=tk.BOTH, expand=True)

stats_text = tk.Text(stats_frame, width=50, height=15, font=("Courier", 10))
stats_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

#create a frame for the exit button
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

exit_button = tk.Button(button_frame, text="Exit", command=root.destroy)
exit_button.pack(side=tk.LEFT, padx=10)

#add info text about resetting stats
info_label = tk.Label(root, text="Press 'R' in the main menu to reset statistics", font=("Arial", 10))
info_label.pack(pady=5)

#load and display initial stats
update_display()

#start the main loop
if __name__ == "__main__":
    root.mainloop()