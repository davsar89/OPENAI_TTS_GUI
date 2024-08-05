import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from openai import OpenAI
import datetime
import pygame
import threading

client = OpenAI()

voice_options = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

def split_text(text):
    max_chunk_size = 4000
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_sound(txtt, ii, directory, timestamp, voice, speed):
    speech_file_path = directory / f"{timestamp}_{voice}_{ii}.mp3"
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        speed=speed,
        input=txtt
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path

def log_input_text(text, text_log_directory, timestamp):
    log_file_path = text_log_directory / f"{timestamp}_input_log.txt"
    with log_file_path.open("a") as log_file:
        log_file.write(f"{timestamp} - Input Text:\n{text}\n\n")
    return log_file_path

def generate_audio_thread():
    global last_generated_file
    theText = text_box.get("1.0", tk.END).strip()
    if not theText:
        messagebox.showerror("Input Error", "Please enter some text.")
        status_label.config(text="")
        return

    current_directory = Path(__file__).parent
    audio_directory = current_directory / "generated_sounds"
    text_log_directory = current_directory / "text_logs"
    audio_directory.mkdir(parents=True, exist_ok=True)
    text_log_directory.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    selected_voice = voice_var.get()
    selected_speed = speed_var.get()
    
    # Log the input text
    log_input_text(theText, text_log_directory, timestamp)
    
    input_chunks = split_text(theText)
    generated_files = []
    for ii, chunk in enumerate(input_chunks):
        last_generated_file = generate_sound(chunk, ii, audio_directory, timestamp, selected_voice, selected_speed)
        generated_files.append(last_generated_file)

    files_list = "\n".join([str(file) for file in generated_files])
    status_label.config(text=f"Audio files have been generated successfully.\n{files_list}", fg="green")

def generate_audio():
    status_label.config(text="Processing text, please wait...", fg="red")
    threading.Thread(target=generate_audio_thread).start()

def play_last_sound():
    if last_generated_file and last_generated_file.exists():
        pygame.mixer.init()
        pygame.mixer.music.load(str(last_generated_file))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        messagebox.showwarning("Play Error", "No audio file generated yet or file not found.")

# Setting up the GUI
root = tk.Tk()
root.title("Text to Speech Generator")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

text_label = tk.Label(frame, text="Enter Text:")
text_label.grid(row=0, column=0, sticky="w")

text_box = tk.Text(frame, wrap="word", width=60, height=15)
text_box.grid(row=1, column=0, columnspan=2, pady=(5, 10))

voice_label = tk.Label(frame, text="Select Voice:")
voice_label.grid(row=2, column=0, sticky="w")

voice_var = tk.StringVar(value="onyx")
voice_menu = tk.OptionMenu(frame, voice_var, *voice_options)
voice_menu.grid(row=2, column=1, sticky="w")

speed_label = tk.Label(frame, text="Select Speed:")
speed_label.grid(row=3, column=0, sticky="w")

speed_var = tk.DoubleVar(value=1.05)
speed_scale = tk.Scale(frame, variable=speed_var, from_=0.5, to=2.0, resolution=0.01, orient=tk.HORIZONTAL)
speed_scale.grid(row=3, column=1, sticky="w")

generate_button = tk.Button(frame, text="Generate Audio", command=generate_audio)
generate_button.grid(row=4, column=0, columnspan=2, pady=(5, 0))

play_button = tk.Button(frame, text="Play Last Generated Audio", command=play_last_sound)
play_button.grid(row=5, column=0, columnspan=2, pady=(5, 0))

status_label = tk.Label(frame, text="", fg="red", justify=tk.LEFT)
status_label.grid(row=6, column=0, columnspan=2)

last_generated_file = None

root.mainloop()
