import tkinter as tk
from tkinter import ttk, messagebox
import os
import requests
import json
from pathlib import Path
import subprocess
import sys

class ElevenLabsLoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceMaster Pro - Eleven Labs Setup")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # Center the window
        self.center_window()
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#1a1a2e',      # Dark navy
            'bg_secondary': '#16213e',     # Darker navy
            'bg_card': '#0f3460',          # Card background
            'accent_primary': '#e94560',   # Modern red
            'accent_secondary': '#f39c12', # Orange
            'text_primary': '#ffffff',     # White text
            'text_secondary': '#a0a0a0',   # Gray text
            'success': '#00d2d3',          # Cyan
            'input_bg': '#2c3e50',         # Input background
            'input_border': '#34495e'      # Input border
        }
        
        # Check if credentials already exist
        self.credentials_file = Path(".env")
        self.config_file = Path("elevenlabs_config.json")
        
        self.create_widgets()
        self.load_existing_credentials()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create the login interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="VoiceMaster Pro Setup",
            font=('Segoe UI', 20, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_primary']
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Connect your Eleven Labs account to get started",
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg=self.colors['bg_card'], relief='flat', bd=0)
        form_frame.pack(fill='x', pady=20)
        
        # Inner padding frame
        inner_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
        inner_frame.pack(fill='x', padx=25, pady=25)
        
        # API Key section
        api_key_label = tk.Label(
            inner_frame,
            text="Eleven Labs API Key:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card'],
            anchor='w'
        )
        api_key_label.pack(fill='x', pady=(0, 8))
        
        self.api_key_entry = tk.Entry(
            inner_frame,
            font=('Segoe UI', 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            relief='flat',
            bd=0,
            show='*'  # Hide API key
        )
        self.api_key_entry.pack(fill='x', ipady=8, pady=(0, 5))
        
        # Show/Hide API key button
        self.show_key_var = tk.BooleanVar()
        show_key_check = tk.Checkbutton(
            inner_frame,
            text="Show API Key",
            variable=self.show_key_var,
            command=self.toggle_api_key_visibility,
            font=('Segoe UI', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_card'],
            selectcolor=self.colors['bg_secondary'],
            activebackground=self.colors['bg_card'],
            activeforeground=self.colors['text_primary']
        )
        show_key_check.pack(anchor='w', pady=(0, 15))
        
        # Help text with clickable link style
        help_label = tk.Label(
            inner_frame,
            text="Don't have an API key? Get one from elevenlabs.io → Profile + API Key",
            font=('Segoe UI', 9),
            fg=self.colors['accent_secondary'],
            bg=self.colors['bg_card'],
            wraplength=400,
            justify='left',
            cursor='hand2'
        )
        help_label.pack(fill='x', pady=(0, 20))
        
        # Bind click to open browser (optional enhancement)
        help_label.bind("<Button-1>", lambda e: self.open_elevenlabs_help())
        
        # Button frame
        button_frame = tk.Frame(inner_frame, bg=self.colors['bg_card'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Test connection button
        self.test_btn = self.create_modern_button(
            button_frame,
            "Test Connection",
            self.test_connection,
            self.colors['accent_secondary'],
            width=15
        )
        self.test_btn.pack(side='left', padx=(0, 10))
        
        # Save and continue button
        self.save_btn = self.create_modern_button(
            button_frame,
            "Save & Launch VoiceMaster",
            self.save_and_launch,
            self.colors['success'],
            width=20
        )
        self.save_btn.pack(side='right')
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Enter your Eleven Labs API key to continue",
            font=('Segoe UI', 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        self.status_label.pack(pady=20)
        
        # Skip button for existing users
        skip_btn = tk.Button(
            main_frame,
            text="Skip (Use existing .env file)",
            command=self.skip_login,
            font=('Segoe UI', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary'],
            bd=0,
            relief='flat',
            cursor='hand2'
        )
        skip_btn.pack(pady=10)
        
    def create_modern_button(self, parent, text, command, bg_color, width=None):
        """Create a modern styled button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Segoe UI', 11, 'bold'),
            bg=bg_color,
            fg='white',
            activebackground=bg_color,
            activeforeground='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            width=width
        )
        
        # Add hover effect
        def on_enter(e):
            btn.configure(bg=self.lighten_color(bg_color, 20))
        
        def on_leave(e):
            btn.configure(bg=bg_color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def lighten_color(self, hex_color, percent):
        """Lighten a hex color by a percentage"""
        # Simple color lightening - just return the original for now
        return hex_color
    
    def toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        if self.show_key_var.get():
            self.api_key_entry.config(show='')
        else:
            self.api_key_entry.config(show='*')
    
    def load_existing_credentials(self):
        """Load existing credentials if they exist"""
        if self.credentials_file.exists():
            try:
                with open(self.credentials_file, 'r') as f:
                    for line in f:
                        if line.startswith('ELEVENLABS_API_KEY='):
                            api_key = line.split('=', 1)[1].strip().strip('"')
                            if api_key:
                                self.api_key_entry.insert(0, api_key)
                                self.status_label.config(
                                    text="Existing credentials found - you can test or update them",
                                    fg=self.colors['success']
                                )
                                break
            except Exception as e:
                print(f"Error loading credentials: {e}")
    
    def test_connection(self):
        """Test the API key by making a request to Eleven Labs"""
        api_key = self.api_key_entry.get().strip()
        
        if not api_key:
            self.status_label.config(
                text="Please enter your API key",
                fg=self.colors['accent_primary']
            )
            return
        
        self.status_label.config(
            text="Testing connection...",
            fg=self.colors['text_secondary']
        )
        
        # Disable buttons during test
        self.test_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        
        # Test in a separate thread to avoid blocking UI
        import threading
        
        def test_api():
            try:
                headers = {
                    "xi-api-key": api_key,
                    "Accept": "application/json"
                }
                
                response = requests.get(
                    "https://api.elevenlabs.io/v1/voices",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    voices = data.get("voices", [])
                    
                    # Filter for custom voices
                    custom_voices = [v for v in voices if v.get("category", "").lower() in ["cloned", "generated"]]
                    
                    self.root.after(0, lambda: self.on_test_success(len(custom_voices), len(voices)))
                elif response.status_code == 401:
                    self.root.after(0, lambda: self.on_test_error("Invalid API key"))
                else:
                    self.root.after(0, lambda: self.on_test_error(f"API error: {response.status_code}"))
                    
            except requests.exceptions.Timeout:
                self.root.after(0, lambda: self.on_test_error("Connection timeout"))
            except requests.exceptions.ConnectionError:
                self.root.after(0, lambda: self.on_test_error("Connection failed"))
            except Exception as e:
                self.root.after(0, lambda: self.on_test_error(f"Error: {str(e)}"))
        
        threading.Thread(target=test_api, daemon=True).start()
    
    def on_test_success(self, custom_voices, total_voices):
        """Handle successful API test"""
        self.status_label.config(
            text=f"✓ Connection successful! Found {custom_voices} custom voices ({total_voices} total)",
            fg=self.colors['success']
        )
        self.test_btn.config(state='normal')
        self.save_btn.config(state='normal')
    
    def on_test_error(self, error_msg):
        """Handle API test error"""
        self.status_label.config(
            text=f"✗ {error_msg}",
            fg=self.colors['accent_primary']
        )
        self.test_btn.config(state='normal')
        self.save_btn.config(state='normal')
    
    def save_credentials(self, api_key):
        """Save credentials to .env file"""
        try:
            # Create .env file content
            env_content = f'ELEVENLABS_API_KEY="{api_key}"\n'
            
            # Write to .env file
            with open(self.credentials_file, 'w') as f:
                f.write(env_content)
            
            # Also save to config file for easier access
            config_data = {
                "api_key": api_key,
                "setup_date": str(Path().resolve()),
                "version": "1.0"
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save credentials: {str(e)}")
            return False
    
    def save_and_launch(self):
        """Save credentials and launch the main application"""
        api_key = self.api_key_entry.get().strip()
        
        if not api_key:
            messagebox.showwarning("Warning", "Please enter your API key")
            return
        
        # Save credentials
        if self.save_credentials(api_key):
            # Check if this is being run from the main app (credentials update)
            # or as initial setup (should launch main app)
            import sys
            
            if len(sys.argv) > 1 and sys.argv[1] == "--update-only":
                messagebox.showinfo(
                    "Success", 
                    "Credentials updated successfully!\nRestart VoiceMaster to apply changes."
                )
                self.root.destroy()
            else:
                messagebox.showinfo(
                    "Success", 
                    "Credentials saved successfully!\nLaunching VoiceMaster..."
                )
                self.launch_main_app()
        
    def skip_login(self):
        """Skip login and launch main app (for users with existing .env)"""
        if self.credentials_file.exists():
            self.launch_main_app()
        else:
            messagebox.showwarning(
                "No Credentials", 
                "No .env file found. Please enter your API key or create a .env file manually."
            )
    
    def launch_main_app(self):
        """Launch the main VoiceMaster application"""
        try:
            # Get the current directory and find the virtual environment
            current_dir = Path.cwd()
            venv_python = None
            
            # Look for virtual environment Python executable
            possible_venv_paths = [
                current_dir / ".venv" / "Scripts" / "python.exe",
                current_dir / "venv" / "Scripts" / "python.exe",
                current_dir / ".env" / "Scripts" / "python.exe"
            ]
            
            for path in possible_venv_paths:
                if path.exists():
                    venv_python = str(path)
                    break
            
            if not venv_python:
                # Fallback to system python
                venv_python = "python"
            
            # Launch the main GUI
            subprocess.Popen([venv_python, "voicemaster_gui.py"])
            
            # Close login window
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch VoiceMaster: {str(e)}")
    
    def open_elevenlabs_help(self):
        """Open Eleven Labs API key page in browser"""
        import webbrowser
        try:
            webbrowser.open("https://elevenlabs.io/speech-synthesis")
        except:
            # If browser opening fails, show the URL in a message
            messagebox.showinfo(
                "Get API Key", 
                "Visit: https://elevenlabs.io\nGo to Profile + API Key to get your API key"
            )

def main():
    root = tk.Tk()
    app = ElevenLabsLoginGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()