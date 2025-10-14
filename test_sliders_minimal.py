#!/usr/bin/env python3
"""
Debug script to test if the voice parameter sliders are visible
"""

import tkinter as tk
from tkinter import ttk

def test_sliders():
    """Test the slider visibility in a minimal window"""
    
    root = tk.Tk()
    root.title("Slider Test")
    root.geometry("600x400")
    root.configure(bg='#1a1a2e')
    
    # Colors
    colors = {
        'bg_primary': '#1a1a2e',
        'bg_card': '#0f3460',
        'text_primary': '#ffffff',
        'accent_primary': '#e94560',
        'bg_secondary': '#16213e'
    }
    
    # Main frame
    main_frame = tk.Frame(root, bg=colors['bg_primary'])
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Title
    title = tk.Label(
        main_frame,
        text="🎛️ Voice Parameters Test",
        font=('Segoe UI', 16, 'bold'),
        fg=colors['text_primary'],
        bg=colors['bg_primary']
    )
    title.pack(pady=(0, 20))
    
    # Card frame
    card_frame = tk.Frame(main_frame, bg=colors['bg_card'], relief='raised', bd=2)
    card_frame.pack(fill='x', pady=10)
    
    inner_frame = tk.Frame(card_frame, bg=colors['bg_card'])
    inner_frame.pack(fill='x', padx=15, pady=15)
    
    # Variables
    stability_var = tk.DoubleVar(value=0.5)
    similarity_var = tk.DoubleVar(value=0.75)
    style_var = tk.DoubleVar(value=0.0)
    speed_var = tk.DoubleVar(value=1.0)
    
    # Grid frame
    grid_frame = tk.Frame(inner_frame, bg=colors['bg_card'])
    grid_frame.pack(fill='x')
    
    grid_frame.grid_columnconfigure(0, weight=1)
    grid_frame.grid_columnconfigure(1, weight=1)
    
    # Stability
    stab_frame = tk.Frame(grid_frame, bg=colors['bg_card'])
    stab_frame.grid(row=0, column=0, padx=(0, 10), pady=5, sticky='ew')
    
    tk.Label(stab_frame, text="Stability:", fg=colors['text_primary'], bg=colors['bg_card']).pack(anchor='w')
    stab_scale = tk.Scale(
        stab_frame, from_=0.0, to=1.0, resolution=0.01, orient='horizontal',
        variable=stability_var, bg=colors['bg_card'], fg=colors['text_primary']
    )
    stab_scale.pack(fill='x')
    
    # Similarity
    sim_frame = tk.Frame(grid_frame, bg=colors['bg_card'])
    sim_frame.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='ew')
    
    tk.Label(sim_frame, text="Similarity:", fg=colors['text_primary'], bg=colors['bg_card']).pack(anchor='w')
    sim_scale = tk.Scale(
        sim_frame, from_=0.0, to=1.0, resolution=0.01, orient='horizontal',
        variable=similarity_var, bg=colors['bg_card'], fg=colors['text_primary']
    )
    sim_scale.pack(fill='x')
    
    # Style
    style_frame = tk.Frame(grid_frame, bg=colors['bg_card'])
    style_frame.grid(row=1, column=0, padx=(0, 10), pady=5, sticky='ew')
    
    tk.Label(style_frame, text="Style:", fg=colors['text_primary'], bg=colors['bg_card']).pack(anchor='w')
    style_scale = tk.Scale(
        style_frame, from_=0.0, to=1.0, resolution=0.01, orient='horizontal',
        variable=style_var, bg=colors['bg_card'], fg=colors['text_primary']
    )
    style_scale.pack(fill='x')
    
    # Speed
    speed_frame = tk.Frame(grid_frame, bg=colors['bg_card'])
    speed_frame.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='ew')
    
    tk.Label(speed_frame, text="Speed:", fg=colors['text_primary'], bg=colors['bg_card']).pack(anchor='w')
    speed_scale = tk.Scale(
        speed_frame, from_=0.25, to=4.0, resolution=0.01, orient='horizontal',
        variable=speed_var, bg=colors['bg_card'], fg=colors['text_primary']
    )
    speed_scale.pack(fill='x')
    
    # Test button
    def show_values():
        values = f"Stability: {stability_var.get():.2f}, Similarity: {similarity_var.get():.2f}, Style: {style_var.get():.2f}, Speed: {speed_var.get():.2f}"
        print(values)
        result_label.config(text=values)
    
    test_btn = tk.Button(
        inner_frame, text="Test Values", command=show_values,
        bg=colors['accent_primary'], fg='white', font=('Segoe UI', 10, 'bold')
    )
    test_btn.pack(pady=(10, 0))
    
    result_label = tk.Label(
        inner_frame, text="Click 'Test Values' to see slider values",
        fg=colors['text_primary'], bg=colors['bg_card'], wraplength=500
    )
    result_label.pack(pady=(10, 0))
    
    root.mainloop()

if __name__ == "__main__":
    test_sliders()