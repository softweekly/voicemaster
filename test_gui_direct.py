#!/usr/bin/env python3
"""
Direct test of VoiceMaster GUI to check slider visibility
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
from voicemaster_gui import VoiceMasterGUI

def test_gui_visibility():
    """Test if sliders are visible in the GUI"""
    print("Starting VoiceMaster GUI test...")
    
    root = tk.Tk()
    
    try:
        # Create the GUI
        app = VoiceMasterGUI(root)
        
        # Check if slider variables exist
        print(f"Stability variable exists: {hasattr(app, 'stability_var')}")
        print(f"Similarity variable exists: {hasattr(app, 'similarity_var')}")
        print(f"Style variable exists: {hasattr(app, 'style_var')}")
        print(f"Speed variable exists: {hasattr(app, 'speed_var')}")
        
        if hasattr(app, 'stability_var'):
            print(f"Stability value: {app.stability_var.get()}")
            print(f"Similarity value: {app.similarity_var.get()}")
            print(f"Style value: {app.style_var.get()}")
            print(f"Speed value: {app.speed_var.get()}")
        
        # Check if slider widgets exist
        print(f"Stability slider exists: {hasattr(app, 'stability_scale')}")
        print(f"Similarity slider exists: {hasattr(app, 'similarity_scale')}")
        print(f"Style slider exists: {hasattr(app, 'style_scale')}")
        print(f"Speed slider exists: {hasattr(app, 'speed_scale')}")
        
        print("GUI created successfully! Check the window for sliders.")
        print("Close the window to end the test.")
        
        # Start the GUI
        root.mainloop()
        
    except Exception as e:
        print(f"Error creating GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui_visibility()