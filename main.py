import tkinter as tk
from tkinter import filedialog

def select_video():
    file_path = filedialog.askopenfilename(
        title="Select a Video",
        filetypes=[("Video Files", "*.mp4 *.mov *.mkv")]
    )

    if file_path:
        status_label.config(text=f"Selected: {file_path}")

app = tk.Tk()
app.title("CreatorKit AI")
app.geometry("600x300")

title_label = tk.Label(
    app,
    text="CreatorKit AI",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=20)

select_button = tk.Button(
    app,
    text="Select Video",
    command=select_video
)
select_button.pack(pady=10)

status_label = tk.Label(
    app,
    text="No video selected"
)
status_label.pack(pady=10)

app.mainloop()
