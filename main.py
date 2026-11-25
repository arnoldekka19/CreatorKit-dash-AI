import tkinter as tk
from tkinter import filedialog, messagebox
from faster_whisper import WhisperModel
import threading
import os

video_path = ""


def select_video():
    global video_path

    video_path = filedialog.askopenfilename(
        title="Select a Video",
        filetypes=[
            ("Video Files", "*.mp4 *.mov *.mkv *.avi")
        ]
    )

    if video_path:
        status_label.config(
            text=f"Selected: {os.path.basename(video_path)}"
        )


def format_timestamp(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)

    return (
        f"{hours:02}:{minutes:02}:"
        f"{seconds:02},{milliseconds:03}"
    )


def update_status(text):
    app.after(0, lambda: status_label.config(text=text))


def generate_subtitles(source, output_path):
    try:
        update_status("Loading AI model...")

        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

        update_status("Transcribing video...")

        segments, info = model.transcribe(
            source,
            beam_size=5
        )

        with open(output_path, "w", encoding="utf-8") as file:
            for index, segment in enumerate(segments, start=1):
                start = format_timestamp(segment.start)
                end = format_timestamp(segment.end)

                file.write(
                    f"{index}\n{start} --> {end}\n"
                    f"{segment.text.strip()}\n\n"
                )

        update_status("Subtitles generated successfully!")

        app.after(
            0,
            lambda: messagebox.showinfo(
                "Success",
                f"Subtitles saved to:\n{output_path}"
            )
        )

    except Exception as error:
        error_message = str(error)
        update_status("An error occurred.")

        app.after(
            0,
            lambda: messagebox.showerror(
                "Error", error_message
            )
        )

    finally:
        app.after(
            0,
            lambda: generate_button.config(state=tk.NORMAL)
        )


def start_transcription():
    if not video_path:
        messagebox.showwarning(
            "Warning",
            "Please select a video first."
        )
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".srt",
        filetypes=[("Subtitle Files", "*.srt")]
    )

    if not output_path:
        return

    generate_button.config(state=tk.DISABLED)

    threading.Thread(
        target=generate_subtitles,
        args=(video_path, output_path),
        daemon=True
    ).start()


app = tk.Tk()
app.title("CreatorKit AI")
app.geometry("650x400")

title_label = tk.Label(
    app,
    text="CreatorKit AI",
    font=("Arial", 28, "bold")
)
title_label.pack(pady=25)

subtitle_label = tk.Label(
    app,
    text="AI Video Transcription & Subtitle Generator",
    font=("Arial", 13)
)
subtitle_label.pack(pady=5)

select_button = tk.Button(
    app,
    text="Select Video",
    command=select_video,
    width=25
)
select_button.pack(pady=15)

generate_button = tk.Button(
    app,
    text="Generate AI Subtitles",
    command=start_transcription,
    width=25
)
generate_button.pack(pady=10)

status_label = tk.Label(
    app,
    text="No video selected",
    wraplength=550
)
status_label.pack(pady=20)

app.mainloop()
