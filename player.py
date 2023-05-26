import tkinter as tk
from tkinter import filedialog
import pygame

class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        
        # Create controls
        self.select_button = tk.Button(root, text="Select MP3", command=self.select_mp3)
        self.select_button.pack(pady=10)
        
        self.play_button = tk.Button(root, text="Play", command=self.play)
        self.play_button.pack(pady=5)
        
        self.pause_button = tk.Button(root, text="Pause", command=self.pause)
        self.pause_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(pady=5)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Initialize variables
        self.current_song = None
        
    def select_mp3(self):
        # Open file dialog to select an MP3 file
        file_path = filedialog.askopenfilename(title="Select MP3", filetypes=(("MP3 Files", "*.mp3"),))
        
        if file_path:
            # Load the selected MP3 file
            pygame.mixer.music.load(file_path)
            self.current_song = file_path
            
    def play(self):
        if self.current_song:
            # Play the loaded MP3 file
            pygame.mixer.music.play()
            
    def pause(self):
        if self.current_song:
            # Pause the currently playing MP3 file
            pygame.mixer.music.pause()
            
    def stop(self):
        if self.current_song:
            # Stop the currently playing MP3 file
            pygame.mixer.music.stop()
            self.current_song = None

# Create the Tkinter root window
root = tk.Tk()

# Create an instance of the MP3Player class
mp3_player = MP3Player(root)

# Run the Tkinter event loop
root.mainloop()
