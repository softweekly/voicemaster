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
        
        # Enable DPI awareness for Windows
        self.setup_dpi_awareness()
        
        # Dynamic sizing based on screen resolution
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate optimal window size (60% of screen, but with limits)
        optimal_width = min(max(int(screen_width * 0.6), 800), 1200)
        optimal_height = min(max(int(screen_height * 0.7), 600), 900)
        
        self.root.geometry(f"{optimal_width}x{optimal_height}")
        self.root.minsize(600, 500)    # Minimum size to prevent UI breaking
        self.root.configure(bg='#1a1a2e')
        
        # Store scaling factor for responsive design
        self.scale_factor = min(optimal_width / 800, optimal_height / 600)
        self.scale_factor = max(0.8, min(self.scale_factor, 1.5))  # Limit scaling
        
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
            'warning': '#ff9f1a',          # Orange
            'info': '#54a0ff'              # Blue
        }
        
        # Configure ttk styles for modern look
        self.setup_styles()
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Variables
        self.voices = []
        self.selected_voice_id = None
        self.selected_voice_name = None
        self.current_audio_file = None
        self.is_recording = False
        self.microphones = []
        
        # Voice parameter variables for advanced control
        self.stability_var = tk.DoubleVar(value=0.5)        # Default: 0.5
        self.similarity_var = tk.DoubleVar(value=0.75)      # Default: 0.75
        self.style_var = tk.DoubleVar(value=0.0)            # Default: 0.0 (style exaggeration)
        self.speed_var = tk.DoubleVar(value=1.0)            # Default: 1.0 (normal speed)
        
        # Store references to UI elements for real-time scaling
        self.scalable_elements = {
            'labels': [],
            'buttons': [],
            'entries': [],
            'text_widgets': []
        }
        self.last_scale_factor = self.scale_factor
        
        # Store references to UI elements for real-time scaling
        self.scalable_elements = {
            'labels': [],
            'buttons': [],
            'entries': [],
            'text_widgets': []
        }
        self.last_scale_factor = self.scale_factor
        
        # Create menu bar
        self.create_menu()
        
        # Create GUI elements
        self.create_widgets()
        
        # Ensure optimal sizing for user's screen
        self.ensure_optimal_visibility()
        
        # Load voices on startup
        self.load_voices()
        
        # Periodic refresh interval (in milliseconds)
        self.refresh_interval = 60000  # Default: 60 seconds
        self.enable_periodic_refresh = True  # Toggle periodic refresh

        # Start periodic refresh
        self.start_periodic_refresh()

        # Bind keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.generate_speech())
        self.root.bind('<F1>', lambda e: self.play_audio())
        self.root.bind('<F2>', lambda e: self.stop_audio())
        self.root.bind('<F3>', lambda e: self.start_speech_to_clone())
        
        # Bind window resize events for responsive design
        self.root.bind('<Configure>', self.on_window_resize)
    
    def setup_dpi_awareness(self):
        """Enable DPI awareness for better scaling on high-DPI displays"""
        try:
            if os.name == 'nt':  # Windows
                import ctypes
                # Try to set DPI awareness
                try:
                    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # PROCESS_SYSTEM_DPI_AWARE
                except:
                    try:
                        ctypes.windll.user32.SetProcessDPIAware()
                    except:
                        pass  # DPI awareness not supported
            else:  # Linux/Unix
                # On Linux, try to detect high-DPI displays
                try:
                    self.root.update_idletasks()
                    dpi = self.root.winfo_fpixels('1i')
                    if dpi > 120:  # High DPI display detected
                        # Adjust scale factor for high DPI
                        dpi_scale = dpi / 96
                        self.scale_factor *= min(dpi_scale, 1.5)  # Cap at 1.5x
                except:
                    pass  # Use default scaling
        except:
            pass  # DPI awareness not supported
    
    def scale_font_size(self, base_size):
        """Scale font size based on screen and user scaling"""
        return max(8, int(base_size * self.scale_factor))
    
    def scale_padding(self, base_padding):
        """Scale padding based on screen size"""
        return max(2, int(base_padding * self.scale_factor))
    
    def register_scalable_element(self, element, element_type, base_font_size=None, base_padding=None):
        """Register an element for real-time scaling"""
        element_info = {
            'widget': element,
            'type': element_type,
            'base_font_size': base_font_size,
            'base_padding': base_padding
        }
        
        if element_type not in self.scalable_elements:
            self.scalable_elements[element_type] = []
        
        self.scalable_elements[element_type].append(element_info)
    
    def apply_real_time_scaling(self):
        """Apply scaling changes to all registered UI elements"""
        try:
            # Update labels
            for element_info in self.scalable_elements.get('labels', []):
                widget = element_info['widget']
                base_size = element_info.get('base_font_size', 11)
                
                if widget.winfo_exists():
                    new_font_size = self.scale_font_size(base_size)
                    current_font = widget.cget('font')
                    
                    # Parse current font
                    if isinstance(current_font, tuple) and len(current_font) >= 2:
                        font_family = current_font[0]
                        font_style = current_font[2] if len(current_font) > 2 else 'normal'
                    else:
                        font_family, font_style = 'Segoe UI', 'normal'
                    
                    widget.configure(font=(font_family, new_font_size, font_style))
            
            # Update buttons
            for element_info in self.scalable_elements.get('buttons', []):
                widget = element_info['widget']
                base_font_size = element_info.get('base_font_size', 11)
                base_padding = element_info.get('base_padding', {})
                base_padx = base_padding.get('padx', 20)
                base_pady = base_padding.get('pady', 12)
                
                if widget.winfo_exists():
                    new_font_size = self.scale_font_size(base_font_size)
                    new_padx = self.scale_padding(base_padx)
                    new_pady = self.scale_padding(base_pady)
                    
                    current_font = widget.cget('font')
                    if isinstance(current_font, tuple) and len(current_font) >= 2:
                        font_family = current_font[0]
                        font_style = current_font[2] if len(current_font) > 2 else 'bold'
                    else:
                        font_family, font_style = 'Segoe UI', 'bold'
                    
                    widget.configure(
                        font=(font_family, new_font_size, font_style),
                        padx=new_padx,
                        pady=new_pady
                    )
            
            # Update text widgets
            for element_info in self.scalable_elements.get('text_widgets', []):
                widget = element_info['widget']
                base_size = element_info.get('base_font_size', 11)
                
                if widget.winfo_exists():
                    new_font_size = self.scale_font_size(base_size)
                    widget.configure(font=('Segoe UI', new_font_size))
            
            # Update entries
            for element_info in self.scalable_elements.get('entries', []):
                widget = element_info['widget']
                base_size = element_info.get('base_font_size', 11)
                
                if widget.winfo_exists():
                    new_font_size = self.scale_font_size(base_size)
                    widget.configure(font=('Segoe UI', new_font_size))
                    
        except Exception as e:
            print(f"Error applying real-time scaling: {e}")
    
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure combobox style
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['bg_card'],
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'],
                       arrowcolor=self.colors['accent_primary'],
                       borderwidth=0,
                       relief='flat')
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       background=self.colors['accent_primary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       relief='flat',
                       padding=(20, 10))
    
    def create_menu(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=file_menu)
        file_menu.add_command(label="Eleven Labs Credentials", command=self.open_credentials_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def create_modern_button(self, parent, text, command, bg_color, hover_color=None, **kwargs):
        """Create a modern styled button with hover effect"""
        print(f"DEBUG: Creating button '{text}' with bg_color: {bg_color}")  # Debug
        if hover_color is None:
            hover_color = bg_color
            
        try:
            # Scale button properties
            font_size = self.scale_font_size(11)
            padx = self.scale_padding(20)
            pady = self.scale_padding(12)
            
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                font=('Segoe UI', font_size, 'bold'),
                bg=bg_color,
                fg=self.colors['text_primary'],
                relief='flat',
                borderwidth=0,
                padx=padx,
                pady=pady,
                cursor='hand2',
                **kwargs
            )
            
            # Register button for real-time scaling
            self.register_scalable_element(btn, 'buttons', 
                                         base_font_size=11, 
                                         base_padding={'padx': 20, 'pady': 12})
            
            # Add hover effects
            def on_enter(e):
                btn.configure(bg=hover_color)
            def on_leave(e):
                btn.configure(bg=bg_color)
                
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            print(f"DEBUG: Button '{text}' created successfully")  # Debug
            return btn
        except Exception as e:
            print(f"DEBUG: Error creating button '{text}': {e}")  # Debug
            raise
    
    def create_card_frame(self, parent, **kwargs):
        """Create a modern card-like frame"""
        frame = tk.Frame(
            parent,
            bg=self.colors['bg_card'],
            relief='flat',
            bd=0,
            **kwargs
        )
        return frame
        
    def create_widgets(self):
        print("DEBUG: Starting create_widgets")  # Debug
        # Main container with smaller padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=15, pady=10)  # Reduced padding
        print("DEBUG: Main container created")  # Debug
        
        # Header section - more compact
        header_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 15))  # Reduced spacing
        
        # Smaller title
        title_label = tk.Label(
            header_frame, 
            text="VoiceMaster Pro", 
            font=('Segoe UI', self.scale_font_size(20), 'bold'),
            fg=self.colors['text_primary'], 
            bg=self.colors['bg_primary']
        )
        title_label.pack()
        # Register for scaling
        self.register_scalable_element(title_label, 'labels', base_font_size=20)
        
        subtitle_label = tk.Label(
            header_frame, 
            text="Live Streaming Text-to-Speech", 
            font=('Segoe UI', self.scale_font_size(10)),
            fg=self.colors['text_secondary'], 
            bg=self.colors['bg_primary']
        )
        subtitle_label.pack(pady=(2, 0))  # Reduced spacing
        # Register for scaling
        self.register_scalable_element(subtitle_label, 'labels', base_font_size=10)
        
        # Status indicator with more compact styling
        status_card = self.create_card_frame(main_container)
        status_card.pack(fill='x', pady=(0, 10))  # Reduced spacing
        
        status_inner = tk.Frame(status_card, bg=self.colors['bg_card'])
        status_inner.pack(fill='x', padx=15, pady=10)  # Reduced padding
        
        self.status_label = tk.Label(
            status_inner,
            text="🟢 Ready for streaming",
            font=('Segoe UI', self.scale_font_size(10), 'bold'),
            fg=self.colors['success'],
            bg=self.colors['bg_card']
        )
        self.status_label.pack()
        # Register for scaling
        self.register_scalable_element(self.status_label, 'labels', base_font_size=10)
        
        # Voice selection card - more compact
        voice_card = self.create_card_frame(main_container)
        voice_card.pack(fill='x', pady=(0, 10))  # Reduced spacing
        
        voice_inner = tk.Frame(voice_card, bg=self.colors['bg_card'])
        voice_inner.pack(fill='both', expand=True, padx=15, pady=12)  # Reduced padding
        
        # Voice selection in horizontal layout to save space
        voice_header = tk.Frame(voice_inner, bg=self.colors['bg_card'])
        voice_header.pack(fill='x', pady=(0, 8))
        
        voice_label = tk.Label(
            voice_header, 
            text="🎭 Voice:", 
            font=('Segoe UI', self.scale_font_size(12), 'bold'),
            fg=self.colors['text_primary'], 
            bg=self.colors['bg_card']
        )
        voice_label.pack(side='left')
        # Register for scaling
        self.register_scalable_element(voice_label, 'labels', base_font_size=12)
        
        # Refresh voices button on same line
        self.refresh_btn = self.create_modern_button(
            voice_header,
            text="🔄",
            command=self.load_voices,
            bg_color=self.colors['info'],
            hover_color='#4a90e2'
        )
        self.refresh_btn.configure(font=('Segoe UI', 9), padx=8, pady=6)  # Smaller button
        self.refresh_btn.pack(side='right')
        
        self.voice_combo = ttk.Combobox(
            voice_inner, 
            state="readonly",
            font=('Segoe UI', 11),  # Smaller font
            style='Modern.TCombobox',
            height=12  # Smaller dropdown
        )
        self.voice_combo.pack(fill='x')
        self.voice_combo.bind('<<ComboboxSelected>>', self.on_voice_selected)
        
        # Voice Parameters card - Advanced Controls (35% SIZE)
        print("DEBUG: Creating Voice Parameters section")  # Debug
        params_card = self.create_card_frame(main_container)
        params_card.pack(fill='x', pady=(0, 10))  # BALANCED: fill x only, no expand
        
        params_inner = tk.Frame(params_card, bg=self.colors['bg_card'])
        params_inner.pack(fill='x', padx=15, pady=15)  # BALANCED: increased padding but no expand
        
        # Parameters header
        params_label = tk.Label(
            params_inner, 
            text="🎛️ Voice Parameters:", 
            font=('Segoe UI', self.scale_font_size(12), 'bold'),
            fg=self.colors['text_primary'], 
            bg=self.colors['bg_card']
        )
        params_label.pack(anchor='w', pady=(0, 8))
        self.register_scalable_element(params_label, 'labels', base_font_size=12)
        print("DEBUG: Voice Parameters header created")  # Debug
        
        # Create a grid for the sliders - 2x2 layout with balanced space
        sliders_frame = tk.Frame(params_inner, bg=self.colors['bg_card'])
        sliders_frame.pack(fill='x', pady=(10, 15))  # BALANCED: fill x only, good vertical padding
        
        # Configure grid weights for responsive layout
        sliders_frame.grid_columnconfigure(0, weight=1)
        sliders_frame.grid_columnconfigure(1, weight=1)
        # REMOVED: row configure to prevent excessive vertical expansion
        
        # Stability slider (top-left) - BALANCED SPACING
        stability_frame = tk.Frame(sliders_frame, bg=self.colors['bg_card'])
        stability_frame.grid(row=0, column=0, padx=(0, 12), pady=(0, 12), sticky='ew')  # BALANCED: moderate padding
        
        stability_label = tk.Label(
            stability_frame,
            text="Stability:",
            font=('Segoe UI', self.scale_font_size(10)),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        stability_label.pack(anchor='w')
        self.register_scalable_element(stability_label, 'labels', base_font_size=10)
        
        self.stability_scale = tk.Scale(
            stability_frame,
            from_=0.0, to=1.0,
            resolution=0.01,
            orient='horizontal',
            variable=self.stability_var,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_primary'],
            highlightthickness=0,
            troughcolor=self.colors['bg_secondary'],
            font=('Segoe UI', self.scale_font_size(8))
        )
        self.stability_scale.pack(fill='x')
        self.register_scalable_element(self.stability_scale, 'labels', base_font_size=8)
        
        # Similarity slider (top-right) - BALANCED SPACING
        similarity_frame = tk.Frame(sliders_frame, bg=self.colors['bg_card'])
        similarity_frame.grid(row=0, column=1, padx=(12, 0), pady=(0, 12), sticky='ew')  # BALANCED: moderate padding
        
        similarity_label = tk.Label(
            similarity_frame,
            text="Similarity:",
            font=('Segoe UI', self.scale_font_size(10)),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        similarity_label.pack(anchor='w')
        self.register_scalable_element(similarity_label, 'labels', base_font_size=10)
        
        self.similarity_scale = tk.Scale(
            similarity_frame,
            from_=0.0, to=1.0,
            resolution=0.01,
            orient='horizontal',
            variable=self.similarity_var,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_primary'],
            highlightthickness=0,
            troughcolor=self.colors['bg_secondary'],
            font=('Segoe UI', self.scale_font_size(8))
        )
        self.similarity_scale.pack(fill='x')
        self.register_scalable_element(self.similarity_scale, 'labels', base_font_size=8)
        
        # Style Exaggeration slider (bottom-left) - BALANCED SPACING
        style_frame = tk.Frame(sliders_frame, bg=self.colors['bg_card'])
        style_frame.grid(row=1, column=0, padx=(0, 12), pady=(12, 0), sticky='ew')  # BALANCED: moderate padding
        
        style_label = tk.Label(
            style_frame,
            text="Style Exaggeration:",
            font=('Segoe UI', self.scale_font_size(10)),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        style_label.pack(anchor='w')
        self.register_scalable_element(style_label, 'labels', base_font_size=10)
        
        self.style_scale = tk.Scale(
            style_frame,
            from_=0.0, to=1.0,
            resolution=0.01,
            orient='horizontal',
            variable=self.style_var,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_primary'],
            highlightthickness=0,
            troughcolor=self.colors['bg_secondary'],
            font=('Segoe UI', self.scale_font_size(8))
        )
        self.style_scale.pack(fill='x')
        self.register_scalable_element(self.style_scale, 'labels', base_font_size=8)
        
        # Speed slider (bottom-right) - BALANCED SPACING
        speed_frame = tk.Frame(sliders_frame, bg=self.colors['bg_card'])
        speed_frame.grid(row=1, column=1, padx=(12, 0), pady=(12, 0), sticky='ew')  # BALANCED: moderate padding
        
        speed_label = tk.Label(
            speed_frame,
            text="Speed:",
            font=('Segoe UI', self.scale_font_size(10)),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        speed_label.pack(anchor='w')
        self.register_scalable_element(speed_label, 'labels', base_font_size=10)
        
        self.speed_scale = tk.Scale(
            speed_frame,
            from_=0.25, to=4.0,
            resolution=0.01,
            orient='horizontal',
            variable=self.speed_var,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['accent_primary'],
            highlightthickness=0,
            troughcolor=self.colors['bg_secondary'],
            font=('Segoe UI', self.scale_font_size(8))
        )
        self.speed_scale.pack(fill='x')
        self.register_scalable_element(self.speed_scale, 'labels', base_font_size=8)
        
        # Reset parameters button
        reset_params_btn = self.create_modern_button(
            params_inner,
            text="🔄 Reset to Defaults",
            command=self.reset_voice_parameters,
            bg_color=self.colors['info'],
            hover_color='#4a90e2'
        )
        reset_params_btn.configure(font=('Segoe UI', 9), padx=10, pady=6)
        reset_params_btn.pack(pady=(10, 0))
        
        # Text input card - BALANCED SIZE (30%)
        text_card = self.create_card_frame(main_container)
        text_card.pack(fill='x', pady=(0, 10))  # BALANCED: fill horizontally
        
        text_inner = tk.Frame(text_card, bg=self.colors['bg_card'])
        text_inner.pack(fill='x', padx=15, pady=12)  # BALANCED: restored standard padding
        
        text_label = tk.Label(
            text_inner, 
            text="📝 Text to Speak:", 
            font=('Segoe UI', 12, 'bold'),  # Smaller font
            fg=self.colors['text_primary'], 
            bg=self.colors['bg_card']
        )
        text_label.pack(anchor='w', pady=(0, 5))  # Reduced spacing
        
        self.text_input = scrolledtext.ScrolledText(
            text_inner,
            height=4,  # BALANCED: increased from 2 to 4 lines for 30% size
            font=('Segoe UI', self.scale_font_size(11)),
            wrap=tk.WORD,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_primary'],
            selectbackground=self.colors['accent_primary'],
            selectforeground=self.colors['text_primary'],
            relief='flat',
            borderwidth=0,
            padx=self.scale_padding(10),  # BALANCED: restored standard padding
            pady=self.scale_padding(8)    # BALANCED: good vertical padding
        )
        self.text_input.pack(fill='x')  # BALANCED: fill horizontally
        # Register for scaling
        self.register_scalable_element(self.text_input, 'text_widgets', base_font_size=11)
        
        # Control buttons card - more compact layout
        controls_card = self.create_card_frame(main_container)
        controls_card.pack(fill='x', pady=(0, 10))  # Reduced spacing
        
        controls_inner = tk.Frame(controls_card, bg=self.colors['bg_card'])
        controls_inner.pack(fill='x', padx=15, pady=12)  # Reduced padding
        
        # All buttons in one row to save vertical space
        buttons_frame = tk.Frame(controls_inner, bg=self.colors['bg_card'])
        buttons_frame.pack(fill='x')
        
        # Generate button (primary action) - smaller
        self.generate_btn = self.create_modern_button(
            buttons_frame,
            text="🎤 Generate",  # Shorter text
            command=self.generate_speech,
            bg_color='#ff0000',  # Bright red to make it visible
            hover_color='#d63447'
        )
        self.generate_btn.configure(font=('Segoe UI', 10, 'bold'), padx=12, pady=8)  # Smaller
        self.generate_btn.pack(side='left', padx=(0, 8))
        print("DEBUG: Generate Speech button created and packed")  # Debug
        
        # Speech-to-Clone button - smaller
        self.mic_btn = self.create_modern_button(
            buttons_frame,
            text="🎙️ Clone",  # Shorter text
            command=self.start_speech_to_clone,
            bg_color='#00ff00',  # Bright green
            hover_color='#e67e22'
        )
        self.mic_btn.configure(font=('Segoe UI', 10, 'bold'), padx=12, pady=8)  # Smaller
        self.mic_btn.pack(side='left', padx=(0, 8))
        
        # Play button - smaller
        self.play_btn = self.create_modern_button(
            buttons_frame,
            text="▶️ Play",
            command=self.play_audio,
            bg_color='#0000ff',  # Bright blue
            hover_color='#00a8a9',
            state='disabled'
        )
        self.play_btn.configure(font=('Segoe UI', 10, 'bold'), padx=10, pady=8)  # Smaller
        self.play_btn.pack(side='left', padx=(0, 8))
        
        # Stop button - smaller
        self.stop_btn = self.create_modern_button(
            buttons_frame,
            text="⏹️ Stop",
            command=self.stop_audio,
            bg_color='#ffff00',  # Bright yellow
            hover_color='#d63447',
            state='disabled'
        )
        self.stop_btn.configure(font=('Segoe UI', 10, 'bold'), padx=10, pady=8)  # Smaller
        self.stop_btn.pack(side='left')
        
        # Quick phrases and favorites card - more compact
        favorites_card = self.create_card_frame(main_container)
        favorites_card.pack(fill='x')
        
        favorites_inner = tk.Frame(favorites_card, bg=self.colors['bg_card'])
        favorites_inner.pack(fill='x', padx=15, pady=10)  # Reduced padding
        
        # Favorites header - horizontal layout
        fav_header_frame = tk.Frame(favorites_inner, bg=self.colors['bg_card'])
        fav_header_frame.pack(fill='x', pady=(0, 8))  # Reduced spacing
        
        fav_label = tk.Label(
            fav_header_frame, 
            text="⭐ Favorites:", 
            font=('Segoe UI', 11, 'bold'),  # Smaller font
            fg=self.colors['text_primary'], 
            bg=self.colors['bg_card']
        )
        fav_label.pack(side='left')
        
        # Favorites control buttons - smaller
        fav_controls = tk.Frame(fav_header_frame, bg=self.colors['bg_card'])
        fav_controls.pack(side='right')
        
        # Add to favorites button - smaller
        self.add_fav_btn = self.create_modern_button(
            fav_controls,
            text="💾 Save",  # Shorter text
            command=self.add_current_to_favorites,
            bg_color=self.colors['accent_secondary'],
            hover_color='#e67e22'
        )
        self.add_fav_btn.configure(font=('Segoe UI', 9), padx=8, pady=6)  # Smaller
        self.add_fav_btn.pack(side='right', padx=(5, 0))
        
        # Refresh favorites button - smaller
        refresh_fav_btn = self.create_modern_button(
            fav_controls,
            text="🔄",
            command=self.refresh_quick_phrases,
            bg_color=self.colors['info'],
            hover_color='#4a90e2'
        )
        refresh_fav_btn.configure(font=('Segoe UI', 9), padx=6, pady=6)  # Smaller
        refresh_fav_btn.pack(side='right')
        
        # Scrollable frame for quick phrases - make it scrollable horizontally if needed
        phrase_container = tk.Frame(favorites_inner, bg=self.colors['bg_card'])
        phrase_container.pack(fill='x')
        
        # Create a canvas for horizontal scrolling if there are many phrases
        self.phrase_canvas = tk.Canvas(phrase_container, bg=self.colors['bg_card'], height=50, highlightthickness=0)
        self.phrase_scrollbar = tk.Scrollbar(phrase_container, orient="horizontal", command=self.phrase_canvas.xview)
        self.phrase_canvas.configure(xscrollcommand=self.phrase_scrollbar.set)
        
        self.quick_buttons_frame = tk.Frame(self.phrase_canvas, bg=self.colors['bg_card'])
        self.phrase_canvas.create_window((0, 0), window=self.quick_buttons_frame, anchor="nw")
        
        self.phrase_canvas.pack(side="top", fill="x", expand=True)
        
        # Bind canvas resize
        def configure_scroll_region(event):
            self.phrase_canvas.configure(scrollregion=self.phrase_canvas.bbox("all"))
        self.quick_buttons_frame.bind("<Configure>", configure_scroll_region)
        
        # Load initial quick phrases
        self.refresh_quick_phrases()
        
        # Hotkeys info footer - smaller
        footer_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        footer_frame.pack(fill='x', pady=(10, 0))  # Reduced spacing
        
        info_text = "⌨️ Hotkeys: Ctrl+Enter = Generate | F1 = Play | F2 = Stop | F3 = Speech-to-Clone"
        info_label = tk.Label(
            footer_frame,
            text=info_text,
            font=('Segoe UI', 8),  # Smaller font
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        info_label.pack()
    
    def load_voices(self):
        """Load custom voices from ElevenLabs"""
        self.update_status("Loading voices...")
        
        def load_voices_thread():
            try:
                voices = get_available_voices()
                if voices:
                    self.voices = voices
                    voice_names = [f"{voice['name']} (ID: {voice['voice_id'][:8]}...)" for voice in voices]
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self.update_voice_combo(voice_names))
                    self.root.after(0, lambda: self.update_status(f"Loaded {len(voices)} custom voices"))
                else:
                    self.root.after(0, lambda: self.update_status("No custom voices found!"))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error loading voices: {str(e)}"))
        
        threading.Thread(target=load_voices_thread, daemon=True).start()
    
    def update_voice_combo(self, voice_names):
        """Update the voice combobox with loaded voices"""
        self.voice_combo['values'] = voice_names
        if voice_names:
            self.voice_combo.set(voice_names[0])
            self.on_voice_selected(None)
    
    def on_voice_selected(self, event):
        """Handle voice selection"""
        print(f"DEBUG: on_voice_selected called, combo value: {self.voice_combo.get()}")  # Debug
        if self.voice_combo.get() and self.voices:
            selected_index = self.voice_combo.current()
            print(f"DEBUG: Selected index: {selected_index}, voices count: {len(self.voices)}")  # Debug
            if 0 <= selected_index < len(self.voices):
                voice = self.voices[selected_index]
                self.selected_voice_id = voice['voice_id']
                self.selected_voice_name = voice['name']
                print(f"DEBUG: Selected voice: {self.selected_voice_name} (ID: {self.selected_voice_id})")  # Debug
                self.update_status(f"Selected voice: {self.selected_voice_name}")
    
    def set_quick_text(self, text):
        """Set quick phrase in text input"""
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, text)
    
    def reset_voice_parameters(self):
        """Reset voice parameters to default values"""
        self.stability_var.set(0.5)      # Default stability
        self.similarity_var.set(0.75)    # Default similarity boost
        self.style_var.set(0.0)          # Default style exaggeration (off)
        self.speed_var.set(1.0)          # Default speed (normal)
        self.update_status("Voice parameters reset to defaults")
    
    def generate_speech(self):
        """Generate speech from text input"""
        print("DEBUG: generate_speech called")  # Debug
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to speak!")
            return
        
        if not self.selected_voice_id:
            messagebox.showwarning("Warning", "Please select a voice!")
            return
        
        print(f"DEBUG: Generating speech with voice {self.selected_voice_id}")  # Debug
        self.generate_btn.config(state='disabled')
        self.update_status("Generating speech...")
        
        def generate_thread():
            try:
                # Get voice parameters from sliders
                stability = self.stability_var.get()
                similarity = self.similarity_var.get()
                style = self.style_var.get()
                speed = self.speed_var.get()
                
                # Generate speech with custom parameters
                timestamp = int(time.time())
                filename = f"stream_tts_{timestamp}.mp3"
                print(f"DEBUG: Calling text_to_speech with parameters - stability: {stability}, similarity: {similarity}, style: {style}, speed: {speed}")
                audio_file = text_to_speech(
                    text, 
                    self.selected_voice_id, 
                    filename,
                    stability=stability,
                    similarity_boost=similarity,
                    style=style,
                    speed=speed
                )
                
                if audio_file:
                    self.current_audio_file = audio_file
                    print(f"DEBUG: Audio file generated: {audio_file}")  # Debug
                    
                    # Update overlay with archive
                    generate_overlay_html(
                        main_text=f"🎤 {self.selected_voice_name}",
                        sub_text="TTS Active",
                        save_archive=True
                    )
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self.on_generation_success(audio_file, filename))
                else:
                    print("DEBUG: text_to_speech returned None")  # Debug
                    self.root.after(0, lambda: self.on_generation_error("Failed to generate audio"))
                    
            except Exception as e:
                print(f"DEBUG: Exception in generate_thread: {e}")  # Debug
                self.root.after(0, lambda: self.on_generation_error(str(e)))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def on_generation_success(self, audio_file, filename=None):
        """Handle successful speech generation"""
        print(f"DEBUG: on_generation_success called with audio_file: {audio_file}")  # Debug
        self.generate_btn.config(state='normal')
        self.play_btn.config(state='normal')
        self.stop_btn.config(state='normal')
        print("DEBUG: Buttons enabled")  # Debug
        self.update_status(f"Speech generated: {os.path.basename(audio_file)}")
        
        # Auto-play the generated audio
        self.play_audio()
    
    def on_generation_error(self, error_msg):
        """Handle speech generation error"""
        self.generate_btn.config(state='normal')
        self.update_status(f"Error: {error_msg}")
        messagebox.showerror("Error", f"Failed to generate speech:\n{error_msg}")
    
    def play_audio(self):
        """Play the generated audio"""
        print(f"DEBUG: play_audio called, current_audio_file: {self.current_audio_file}")  # Debug
        if not self.current_audio_file or not os.path.exists(self.current_audio_file):
            messagebox.showwarning("Warning", "No audio file to play!")
            return
        
        try:
            print(f"DEBUG: Loading audio file: {self.current_audio_file}")  # Debug
            pygame.mixer.music.load(self.current_audio_file)
            pygame.mixer.music.play()
            self.update_status("Playing audio...")
            print("DEBUG: Audio playback started")  # Debug
        except Exception as e:
            print(f"DEBUG: Audio playback error: {e}")  # Debug
            messagebox.showerror("Error", f"Failed to play audio:\n{str(e)}")
    
    def stop_audio(self):
        """Stop audio playback"""
        try:
            pygame.mixer.music.stop()
            self.update_status("Audio stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop audio:\n{str(e)}")
    
    def update_status(self, message, color=None):
        """Update status label with modern styling"""
        if color is None:
            color = self.colors['text_secondary']
        
        # Add emoji indicators for different status types
        if "loading" in message.lower() or "generating" in message.lower():
            icon = "⏳"
            color = self.colors['warning']
        elif "ready" in message.lower() or "success" in message.lower():
            icon = "🟢"
            color = self.colors['success']
        elif "error" in message.lower() or "failed" in message.lower():
            icon = "🔴"
            color = self.colors['accent_primary']
        else:
            icon = "ℹ️"
            
        self.status_label.config(text=f"{icon} {message}", fg=color)
    
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
        
        # Add default phrase buttons with modern styling - smaller
        for i, phrase in enumerate(default_phrases):
            btn_text = phrase[:25] + "..." if len(phrase) > 25 else phrase  # Shorter text
            btn = self.create_modern_button(
                self.quick_buttons_frame,
                text=btn_text,
                command=lambda p=phrase: self.set_quick_text(p),
                bg_color=self.colors['bg_secondary'],
                hover_color=self.colors['info']
            )
            btn.configure(font=('Segoe UI', 8), padx=8, pady=6)  # Smaller buttons
            btn.pack(side='left', padx=2, pady=1)
        
        # Add favorites if any exist
        favorites = get_favorite_phrases()[:4]  # Limit to 4 most recent to save space
        if favorites:
            # Add visual separator
            separator = tk.Label(
                self.quick_buttons_frame,
                text="•",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_card']
            )
            separator.pack(side='left', padx=8)
            
            # Add favorite phrase buttons - smaller
            for fav in favorites:
                display_text = f"⭐ {fav['text'][:20]}..." if len(fav['text']) > 20 else f"⭐ {fav['text']}"
                btn = self.create_modern_button(
                    self.quick_buttons_frame,
                    text=display_text,
                    command=lambda f=fav: self.load_favorite(f),
                    bg_color=self.colors['accent_secondary'],
                    hover_color='#e67e22'
                )
                btn.configure(font=('Segoe UI', 8), padx=8, pady=6)  # Smaller buttons
                btn.pack(side='left', padx=2, pady=1)
                
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
            self.update_status(f"Added '{text[:30]}...' to favorites")
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
        
        self.update_status(f"Loaded favorite: '{favorite['voice_name']}' voice")
    
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
            self.update_status("Favorite deleted")
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
        self.update_status("Recording your voice... speak now!")
        
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
            
            self.update_status(f"Speech cloned: '{text[:30]}{'...' if len(text) > 30 else ''}'")
            
            # Auto-play the cloned speech
            self.play_audio()
            
        else:
            self.update_status("Speech-to-clone failed. Try speaking clearly.")
    
    def on_speech_to_clone_error(self, error_msg):
        """Handle speech-to-clone error"""
        # Reset button state
        self.mic_btn.config(
            text="🎙️ Speech-to-Clone (F3)",
            bg='#e74c3c',
            state='normal'
        )
        self.is_recording = False
        
        self.update_status(f"Recording error: {error_msg}")
        messagebox.showerror("Recording Error", f"Failed to record speech:\n{error_msg}")

    def start_periodic_refresh(self):
        """Start periodic refresh of voices."""
        if self.enable_periodic_refresh:
            self.load_voices()
            self.root.after(self.refresh_interval, self.start_periodic_refresh)
    
    def on_window_resize(self, event):
        """Handle window resize events for responsive design"""
        # Only respond to root window resize events
        if event.widget == self.root:
            # Get current window size
            current_width = self.root.winfo_width()
            current_height = self.root.winfo_height()
            
            # Update scale factor based on current size
            new_scale_factor = min(current_width / 800, current_height / 600)
            new_scale_factor = max(0.8, min(new_scale_factor, 1.5))
            
            # Only update if scale factor changed significantly
            if abs(new_scale_factor - self.scale_factor) > 0.05:
                old_scale_factor = self.scale_factor
                self.scale_factor = new_scale_factor
                self.last_scale_factor = old_scale_factor
                
                # Apply real-time scaling to all UI elements
                self.apply_real_time_scaling()
                
                # Update status to show current scale
                try:
                    scale_percent = int(self.scale_factor * 100)
                    if hasattr(self, 'status_label'):
                        current_text = self.status_label.cget('text')
                        if not current_text.startswith('🔍'):
                            self.status_label.configure(text=f"🔍 UI Scale: {scale_percent}% - {current_text}")
                            # Reset status after 2 seconds
                            self.root.after(2000, lambda: self.reset_status_after_scale())
                except:
                    pass
    
    def reset_status_after_scale(self):
        """Reset status label after showing scale information"""
        try:
            if hasattr(self, 'status_label'):
                current_text = self.status_label.cget('text')
                if current_text.startswith('🔍'):
                    # Extract original status after " - "
                    parts = current_text.split(' - ', 1)
                    if len(parts) > 1:
                        self.status_label.configure(text=parts[1])
                    else:
                        self.status_label.configure(text="🟢 Ready for streaming")
        except:
            pass
    
    def register_scalable_element(self, element, element_type, base_font_size=None, base_padding=None):
        """Register an element for real-time scaling"""
        element_info = {
            'widget': element,
            'type': element_type,
            'base_font_size': base_font_size,
            'base_padding': base_padding
        }
        
        if element_type not in self.scalable_elements:
            self.scalable_elements[element_type] = []
        
        self.scalable_elements[element_type].append(element_info)
    
    def apply_real_time_scaling(self):
        """Apply scaling changes to all registered UI elements"""
        try:
            # Update labels
            for element_info in self.scalable_elements.get('labels', []):
                widget = element_info['widget']
                base_size = element_info.get('base_font_size', 11)
                
                if widget.winfo_exists():
                    new_font_size = self.scale_font_size(base_size)
                    current_font = widget.cget('font')
                    
                    # Parse current font
                    if isinstance(current_font, tuple):
                        font_family, old_size = current_font[0], current_font[1]
                        font_style = current_font[2] if len(current_font) > 2 else 'normal'
                    else:
                        font_family, font_style = 'Segoe UI', 'normal'
                    
                    widget.configure(font=(font_family, new_font_size, font_style))
            
            # Update buttons
            for element_info in self.scalable_elements.get('buttons', []):
                widget = element_info['widget']
                base_font_size = element_info.get('base_font_size', 11)
                base_padx = element_info.get('base_padding', {}).get('padx', 20)
                base_pady = element_info.get('base_padding', {}).get('pady', 12)
                
                if widget.winfo_exists():
                    new_font_size = self.scale_font_size(base_font_size)
                    new_padx = self.scale_padding(base_padx)
                    new_pady = self.scale_padding(base_pady)
                    
                    current_font = widget.cget('font')
                    if isinstance(current_font, tuple):
                        font_family, old_size = current_font[0], current_font[1]
                        font_style = current_font[2] if len(current_font) > 2 else 'bold'
                    else:
                        font_family, font_style = 'Segoe UI', 'bold'
                    
                    widget.configure(
                        font=(font_family, new_font_size, font_style),
                        padx=new_padx,
                        pady=new_pady
                    )
            
            # Update text widgets
            for element_info in self.scalable_elements.get('text_widgets', []):
                widget = element_info['widget']
                base_size = element_info.get('base_font_size', 11)
                
                if widget.winfo_exists():
                    new_font_size = self.scale_font_size(base_size)
                    widget.configure(font=('Segoe UI', new_font_size))
            
            # Update entries
            for element_info in self.scalable_elements.get('entries', []):
                widget = element_info['widget']
                base_size = element_info.get('base_font_size', 11)
                
                if widget.winfo_exists():
                    new_font_size = self.scale_font_size(base_size)
                    widget.configure(font=('Segoe UI', new_font_size))
                    
        except Exception as e:
            print(f"Error applying real-time scaling: {e}")
    
    def ensure_optimal_visibility(self):
        """Ensure everything is visible and properly sized for the user's screen"""
        try:
            # Force window to update and get actual screen dimensions
            self.root.update_idletasks()
            
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Get current window size
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            # Check if window is too large for screen (accounting for taskbar/dock)
            max_usable_width = int(screen_width * 0.95)  # 95% of screen width
            max_usable_height = int(screen_height * 0.90)  # 90% of screen height (taskbar space)
            
            # Adjust if needed
            adjusted_width = min(window_width, max_usable_width)
            adjusted_height = min(window_height, max_usable_height)
            
            # Ensure minimum size for functionality
            min_width = 600
            min_height = 500
            
            final_width = max(adjusted_width, min_width)
            final_height = max(adjusted_height, min_height)
            
            # If we had to adjust, update the window
            if final_width != window_width or final_height != window_height:
                self.root.geometry(f"{final_width}x{final_height}")
                
                # Recalculate scale factor for the new size
                new_scale_factor = min(final_width / 800, final_height / 600)
                new_scale_factor = max(0.8, min(new_scale_factor, 1.5))
                
                if abs(new_scale_factor - self.scale_factor) > 0.05:
                    self.scale_factor = new_scale_factor
                    self.apply_real_time_scaling()
            
            # Center the window on screen
            x = (screen_width - final_width) // 2
            y = (screen_height - final_height) // 2
            self.root.geometry(f"{final_width}x{final_height}+{x}+{y}")
            
            # Update status to show initial scale
            scale_percent = int(self.scale_factor * 100)
            print(f"VoiceMaster Pro initialized: {final_width}x{final_height} at {scale_percent}% scale")
            
        except Exception as e:
            print(f"Error ensuring optimal visibility: {e}")
    
    def open_credentials_dialog(self):
        """Open credentials management dialog"""
        # Import login_gui here to avoid circular imports
        import subprocess
        import sys
        import os
        
        try:
            # Launch the login GUI as a subprocess
            current_dir = os.path.dirname(os.path.abspath(__file__))
            login_script = os.path.join(current_dir, "login_gui.py")
            
            # Find Python executable (cross-platform)
            python_exe = sys.executable
            
            # Try to use venv python if available
            if os.name == 'nt':  # Windows
                venv_python_paths = [
                    os.path.join(current_dir, ".venv", "Scripts", "python.exe"),
                    os.path.join(current_dir, "venv", "Scripts", "python.exe")
                ]
            else:  # Linux/Unix
                venv_python_paths = [
                    os.path.join(current_dir, ".venv", "bin", "python"),
                    os.path.join(current_dir, "venv", "bin", "python")
                ]
            
            for venv_path in venv_python_paths:
                if os.path.exists(venv_path):
                    python_exe = venv_path
                    break
            
            # Launch login GUI with update flag
            subprocess.Popen([python_exe, login_script, "--update-only"])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open credentials dialog: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """VoiceMaster Pro v1.0

A powerful text-to-speech application for live streaming
with Eleven Labs integration.

Features:
• Custom voice cloning
• Real-time speech generation
• OBS overlay integration
• Favorites management
• Speech-to-clone functionality

© 2024 VoiceMaster Pro"""
        
        messagebox.showinfo("About VoiceMaster Pro", about_text)

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