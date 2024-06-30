import pyaudio
import wave
import threading
import tkinter as tk
from tkinter import messagebox, filedialog

class AudioRecorder:
    def __init__(self):
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2  # Stereo
        self.rate = 44100  # Record at 44100 samples per second
        self.frames = []  # Initialize array to store frames
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.recording = False
        self.thread = None

    def start_recording(self):
        self.frames = []
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)
        self.recording = True
        self.thread = threading.Thread(target=self.record)
        self.thread.start()
        print("Recording started")

    def record(self):
        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.thread.join()
            self.stream.stop_stream()
            self.stream.close()
            print("Recording stopped")

    def save_recording(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"Recording saved as {filename}")

    def close(self):
        self.p.terminate()

class AudioRecorderApp:
    def __init__(self, root):
        self.recorder = AudioRecorder()
        self.root = root
        self.root.title("Audio Recorder")

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack(pady=10)
        self.stop_button.config(state=tk.DISABLED)

        self.save_button = tk.Button(root, text="Save Recording", command=self.save_recording)
        self.save_button.pack(pady=10)

    def start_recording(self):
        self.recorder.start_recording()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        messagebox.showinfo("Info", "Recording started")

    def stop_recording(self):
        self.recorder.stop_recording()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        messagebox.showinfo("Info", "Recording stopped")

    def save_recording(self):
        filename = filedialog.asksaveasfilename(defaultextension=".wav",
                                                filetypes=[("WAV files", "*.wav")])
        if filename:
            self.recorder.save_recording(filename)
            messagebox.showinfo("Info", f"Recording saved as {filename}")

    def on_closing(self):
        self.recorder.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorderApp(root)
   # root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()