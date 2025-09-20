import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
import pygame
from app_logic import (get_available_voices, text_to_speech, generate_overlay_html, 
                      add_favorite, get_favorite_phrases, delete_favorite, 
                      get_overlay_archive_list, speech_to_cloned_voice,
                      get_microphone_list, record_until_silence, speech_to_text)
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
        self.is_recording = False
        self.microphones = []
        
        # Create GUI elements
        self.create_widgets()
        
        # Load voices on startup
        self.load_voices()
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.generate_speech())
        self.root.bind('<F1>', lambda e: self.play_audio())
        self.root.bind('<F2>', lambda e: self.stop_audio())
        self.root.bind('<F3>', lambda e: self.start_speech_to_clone())
        
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
        
        # Microphone button (Speech-to-Clone)
        self.mic_btn = tk.Button(
            button_frame,
            text="🎙️ Speech-to-Clone (F3)",
            font=('Arial', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=15,
            pady=10,
            command=self.start_speech_to_clone
        )
        self.mic_btn.pack(side='left', padx=5)
        
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
        
        # Quick phrases header with refresh button
        header_frame = tk.Frame(quick_frame, bg='#2c3e50')
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame, 
            text="Quick Phrases & Favorites:", 
            font=('Arial', 10, 'bold'),
            fg='#ecf0f1', 
            bg='#2c3e50'
        ).pack(side='left')
        
        # Add to favorites button
        self.add_fav_btn = tk.Button(
            header_frame,
            text="💾 Save as Favorite",
            font=('Arial', 8),
            bg='#f39c12',
            fg='white',
            relief='flat',
            padx=8,
            pady=2,
            command=self.add_current_to_favorites
        )
        self.add_fav_btn.pack(side='right', padx=5)
        
        # Refresh favorites button
        refresh_fav_btn = tk.Button(
            header_frame,
            text="🔄",
            font=('Arial', 8),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=5,
            pady=2,
            command=self.refresh_quick_phrases
        )
        refresh_fav_btn.pack(side='right', padx=2)
        
        # Scrollable frame for quick phrases
        self.quick_buttons_frame = tk.Frame(quick_frame, bg='#2c3e50')
        self.quick_buttons_frame.pack(fill='x', pady=5)
        
        # Load initial quick phrases
        self.refresh_quick_phrases()
        
        # Hotkeys info
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(pady=5, padx=20, fill='x')
        
        info_text = "Hotkeys: Ctrl+Enter = Generate | F1 = Play | F2 = Stop | F3 = Speech-to-Clone"
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
                    
                    # Update overlay with archive
                    generate_overlay_html(
                        main_text=f"🎤 {self.selected_voice_name}",
                        sub_text="TTS Active",
                        save_archive=True
                    )
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self.on_generation_success(audio_file, filename))
                else:
                    self.root.after(0, lambda: self.on_generation_error("Failed to generate audio"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_generation_error(str(e)))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def on_generation_success(self, audio_file, filename=None):
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
    
    def refresh_quick_phrases(self):
        """Refresh the quick phrases section with default and favorite phrases"""
        # Clear existing buttons
        for widget in self.quick_buttons_frame.winfo_children():
            widget.destroy()
        
        # Default quick phrases
        default_phrases = [
            "Hello everyone, welcome to the stream!",
            "Thanks for following!",
            "Let's get started with today's content.",
            "Don't forget to like and subscribe!"
        ]
        
        # Add default phrase buttons
        for i, phrase in enumerate(default_phrases):
            btn = tk.Button(
                self.quick_buttons_frame,
                text=phrase[:25] + "..." if len(phrase) > 25 else phrase,
                font=('Arial', 8),
                bg='#7f8c8d',
                fg='white',
                relief='flat',
                padx=3,
                pady=2,
                command=lambda p=phrase: self.set_quick_text(p)
            )
            btn.pack(side='left', padx=1, fill='x', expand=True)
        
        # Add separator
        separator = tk.Label(
            self.quick_buttons_frame,
            text="|",
            font=('Arial', 10),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        separator.pack(side='left', padx=5)
        
        # Load and add favorite phrases (limit to 6 most recent)
        favorites = get_favorite_phrases()[:6]
        for fav in favorites:
            display_text = f"🎤 {fav['text'][:20]}..." if len(fav['text']) > 20 else f"🎤 {fav['text']}"
            btn = tk.Button(
                self.quick_buttons_frame,
                text=display_text,
                font=('Arial', 8),
                bg='#e67e22',
                fg='white',
                relief='flat',
                padx=3,
                pady=2,
                command=lambda f=fav: self.load_favorite(f)
            )
            btn.pack(side='left', padx=1)
            
            # Add right-click context menu for deletion
            btn.bind("<Button-3>", lambda e, f_id=fav['id']: self.show_favorite_context_menu(e, f_id))
    
    def set_quick_text(self, text):
        """Set quick phrase in text input"""
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, text)
    
    def add_current_to_favorites(self):
        """Add current text and voice to favorites"""
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text first!")
            return
        
        if not self.selected_voice_id:
            messagebox.showwarning("Warning", "Please select a voice first!")
            return
        
        try:
            add_favorite(text, self.selected_voice_id, self.selected_voice_name)
            self.refresh_quick_phrases()
            self.update_status(f"Added '{text[:30]}...' to favorites", '#27ae60')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add favorite:\n{str(e)}")
    
    def load_favorite(self, favorite):
        """Load a favorite phrase and set voice"""
        # Set the text
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, favorite['text'])
        
        # Try to set the voice if it exists
        for i, voice in enumerate(self.voices):
            if voice['voice_id'] == favorite['voice_id']:
                self.voice_combo.current(i)
                self.on_voice_selected(None)
                break
        
        self.update_status(f"Loaded favorite: '{favorite['voice_name']}' voice", '#3498db')
    
    def show_favorite_context_menu(self, event, favorite_id):
        """Show context menu for favorite deletion"""
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Delete Favorite", command=lambda: self.delete_favorite_by_id(favorite_id))
        context_menu.tk_popup(event.x_root, event.y_root)
    
    def delete_favorite_by_id(self, favorite_id):
        """Delete a favorite by ID"""
        try:
            delete_favorite(favorite_id)
            self.refresh_quick_phrases()
            self.update_status("Favorite deleted", '#e74c3c')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete favorite:\n{str(e)}")
    
    def start_speech_to_clone(self):
        """Start the speech-to-clone process"""
        if not self.selected_voice_id:
            messagebox.showwarning("Warning", "Please select a voice first!")
            return
        
        if self.is_recording:
            messagebox.showinfo("Info", "Already recording! Please wait...")
            return
        
        # Change button state
        self.mic_btn.config(
            text="🎙️ Recording... (speak now)",
            bg='#c0392b',
            state='disabled'
        )
        self.is_recording = True
        self.update_status("🎙️ Recording your voice... speak now!", '#e74c3c')
        
        # Start recording in separate thread
        def record_thread():
            try:
                # Record speech and convert to cloned voice
                text, audio_file = speech_to_cloned_voice(
                    duration=10,  # Max 10 seconds
                    voice_id=self.selected_voice_id,
                    mic_index=None  # Use default microphone
                )
                
                # Update UI in main thread
                self.root.after(0, lambda: self.on_speech_to_clone_complete(text, audio_file))
                
            except Exception as e:
                self.root.after(0, lambda: self.on_speech_to_clone_error(str(e)))
        
        threading.Thread(target=record_thread, daemon=True).start()
    
    def on_speech_to_clone_complete(self, text, audio_file):
        """Handle completed speech-to-clone process"""
        # Reset button state
        self.mic_btn.config(
            text="🎙️ Speech-to-Clone (F3)",
            bg='#e74c3c',
            state='normal'
        )
        self.is_recording = False
        
        if text and audio_file:
            # Set the recognized text in the input field
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(1.0, text)
            
            # Set the current audio file for playback
            self.current_audio_file = audio_file
            self.play_btn.config(state='normal')
            self.stop_btn.config(state='normal')
            
            # Update overlay
            generate_overlay_html(
                main_text=f"🎭 {self.selected_voice_name} (Cloned)",
                sub_text=f"'{text[:50]}{'...' if len(text) > 50 else ''}'"
            )
            
            self.update_status(f"✅ Speech cloned: '{text[:30]}{'...' if len(text) > 30 else ''}'", '#27ae60')
            
            # Auto-play the cloned speech
            self.play_audio()
            
        else:
            self.update_status("❌ Speech-to-clone failed. Try speaking clearly.", '#e74c3c')
    
    def on_speech_to_clone_error(self, error_msg):
        """Handle speech-to-clone error"""
        # Reset button state
        self.mic_btn.config(
            text="🎙️ Speech-to-Clone (F3)",
            bg='#e74c3c',
            state='normal'
        )
        self.is_recording = False
        
        self.update_status(f"❌ Recording error: {error_msg}", '#e74c3c')
        messagebox.showerror("Recording Error", f"Failed to record speech:\n{error_msg}")

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