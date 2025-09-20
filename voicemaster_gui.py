import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
import pygame
from app_logic import get_available_voices, text_to_speech, generate_overlay_html
import time

class VoiceMasterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceMaster Pro - Live Streaming TTS")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Variables
        self.voices = []
        self.selected_voice_id = None
        self.selected_voice_name = None
        self.current_audio_file = None
        
        # Create GUI elements
        self.create_widgets()
        
        # Load voices on startup
        self.load_voices()
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.generate_speech())
        self.root.bind('<F1>', lambda e: self.play_audio())
        self.root.bind('<F2>', lambda e: self.stop_audio())
        
    def create_widgets(self):
        # Main title
        title_label = tk.Label(
            self.root, 
            text="VoiceMaster Pro", 
            font=('Arial', 20, 'bold'),
            fg='#ecf0f1', 
            bg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg='#2c3e50')
        status_frame.pack(pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready for streaming",
            font=('Arial', 10),
            fg='#27ae60',
            bg='#2c3e50'
        )
        self.status_label.pack()
        
        # Voice selection frame
        voice_frame = tk.Frame(self.root, bg='#2c3e50')
        voice_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            voice_frame, 
            text="Select Voice:", 
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1', 
            bg='#2c3e50'
        ).pack(anchor='w')
        
        self.voice_combo = ttk.Combobox(
            voice_frame, 
            state="readonly",
            font=('Arial', 11),
            width=50
        )
        self.voice_combo.pack(pady=5, fill='x')
        self.voice_combo.bind('<<ComboboxSelected>>', self.on_voice_selected)
        
        # Text input frame
        text_frame = tk.Frame(self.root, bg='#2c3e50')
        text_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(
            text_frame, 
            text="Enter Text to Speak:", 
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1', 
            bg='#2c3e50'
        ).pack(anchor='w')
        
        self.text_input = scrolledtext.ScrolledText(
            text_frame,
            height=8,
            font=('Arial', 11),
            wrap=tk.WORD,
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.text_input.pack(pady=5, fill='both', expand=True)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10, padx=20, fill='x')
        
        # Generate button
        self.generate_btn = tk.Button(
            button_frame,
            text="🎤 Generate Speech (Ctrl+Enter)",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.generate_speech
        )
        self.generate_btn.pack(side='left', padx=5)
        
        # Play button
        self.play_btn = tk.Button(
            button_frame,
            text="▶️ Play (F1)",
            font=('Arial', 11),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.play_audio,
            state='disabled'
        )
        self.play_btn.pack(side='left', padx=5)
        
        # Stop button
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ Stop (F2)",
            font=('Arial', 11),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.stop_audio,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=5)
        
        # Refresh voices button
        self.refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh Voices",
            font=('Arial', 10),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=10,
            pady=8,
            command=self.load_voices
        )
        self.refresh_btn.pack(side='right', padx=5)
        
        # Quick text buttons frame
        quick_frame = tk.Frame(self.root, bg='#2c3e50')
        quick_frame.pack(pady=5, padx=20, fill='x')
        
        tk.Label(
            quick_frame, 
            text="Quick Phrases:", 
            font=('Arial', 10, 'bold'),
            fg='#ecf0f1', 
            bg='#2c3e50'
        ).pack(anchor='w')
        
        quick_buttons_frame = tk.Frame(quick_frame, bg='#2c3e50')
        quick_buttons_frame.pack(fill='x', pady=5)
        
        quick_phrases = [
            "Hello everyone, welcome to the stream!",
            "Thanks for following!",
            "Let's get started with today's content.",
            "Don't forget to like and subscribe!"
        ]
        
        for i, phrase in enumerate(quick_phrases):
            btn = tk.Button(
                quick_buttons_frame,
                text=phrase[:30] + "..." if len(phrase) > 30 else phrase,
                font=('Arial', 9),
                bg='#7f8c8d',
                fg='white',
                relief='flat',
                padx=5,
                pady=3,
                command=lambda p=phrase: self.set_quick_text(p)
            )
            btn.pack(side='left', padx=2, fill='x', expand=True)
        
        # Hotkeys info
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(pady=5, padx=20, fill='x')
        
        info_text = "Hotkeys: Ctrl+Enter = Generate | F1 = Play | F2 = Stop"
        tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 9),
            fg='#95a5a6',
            bg='#2c3e50'
        ).pack()
    
    def load_voices(self):
        """Load custom voices from ElevenLabs"""
        self.update_status("Loading voices...", '#f39c12')
        
        def load_voices_thread():
            try:
                voices = get_available_voices()
                if voices:
                    self.voices = voices
                    voice_names = [f"{voice['name']} (ID: {voice['voice_id'][:8]}...)" for voice in voices]
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self.update_voice_combo(voice_names))
                    self.root.after(0, lambda: self.update_status(f"Loaded {len(voices)} custom voices", '#27ae60'))
                else:
                    self.root.after(0, lambda: self.update_status("No custom voices found!", '#e74c3c'))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error loading voices: {str(e)}", '#e74c3c'))
        
        threading.Thread(target=load_voices_thread, daemon=True).start()
    
    def update_voice_combo(self, voice_names):
        """Update the voice combobox with loaded voices"""
        self.voice_combo['values'] = voice_names
        if voice_names:
            self.voice_combo.set(voice_names[0])
            self.on_voice_selected(None)
    
    def on_voice_selected(self, event):
        """Handle voice selection"""
        if self.voice_combo.get() and self.voices:
            selected_index = self.voice_combo.current()
            if 0 <= selected_index < len(self.voices):
                voice = self.voices[selected_index]
                self.selected_voice_id = voice['voice_id']
                self.selected_voice_name = voice['name']
                self.update_status(f"Selected voice: {self.selected_voice_name}", '#3498db')
    
    def set_quick_text(self, text):
        """Set quick phrase in text input"""
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, text)
    
    def generate_speech(self):
        """Generate speech from text input"""
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to speak!")
            return
        
        if not self.selected_voice_id:
            messagebox.showwarning("Warning", "Please select a voice!")
            return
        
        self.generate_btn.config(state='disabled')
        self.update_status("Generating speech...", '#f39c12')
        
        def generate_thread():
            try:
                # Generate speech
                timestamp = int(time.time())
                filename = f"stream_tts_{timestamp}.mp3"
                audio_file = text_to_speech(text, self.selected_voice_id, filename)
                
                if audio_file:
                    self.current_audio_file = audio_file
                    
                    # Update overlay
                    generate_overlay_html(
                        main_text=f"🎤 {self.selected_voice_name}",
                        sub_text="TTS Active"
                    )
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self.on_generation_success(audio_file))
                else:
                    self.root.after(0, lambda: self.on_generation_error("Failed to generate audio"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_generation_error(str(e)))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def on_generation_success(self, audio_file):
        """Handle successful speech generation"""
        self.generate_btn.config(state='normal')
        self.play_btn.config(state='normal')
        self.stop_btn.config(state='normal')
        self.update_status(f"✅ Speech generated: {os.path.basename(audio_file)}", '#27ae60')
        
        # Auto-play the generated audio
        self.play_audio()
    
    def on_generation_error(self, error_msg):
        """Handle speech generation error"""
        self.generate_btn.config(state='normal')
        self.update_status(f"❌ Error: {error_msg}", '#e74c3c')
        messagebox.showerror("Error", f"Failed to generate speech:\n{error_msg}")
    
    def play_audio(self):
        """Play the generated audio"""
        if not self.current_audio_file or not os.path.exists(self.current_audio_file):
            messagebox.showwarning("Warning", "No audio file to play!")
            return
        
        try:
            pygame.mixer.music.load(self.current_audio_file)
            pygame.mixer.music.play()
            self.update_status("🔊 Playing audio...", '#3498db')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio:\n{str(e)}")
    
    def stop_audio(self):
        """Stop audio playback"""
        try:
            pygame.mixer.music.stop()
            self.update_status("⏹️ Audio stopped", '#95a5a6')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop audio:\n{str(e)}")
    
    def update_status(self, message, color='#95a5a6'):
        """Update status label"""
        self.status_label.config(text=message, fg=color)

def main():
    # Create and run the GUI
    root = tk.Tk()
    app = VoiceMasterGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()