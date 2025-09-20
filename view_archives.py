import os
import time
from app_logic import get_overlay_archive_list

def main():
    print("=== VoiceMaster Pro - Overlay Archive Viewer ===\n")
    
    archives = get_overlay_archive_list()
    
    if not archives:
        print("No archived overlays found.")
        return
    
    print(f"Found {len(archives)} archived overlays:\n")
    
    for i, archive in enumerate(archives, 1):
        print(f"{i:2d}. {archive['filename']}")
        print(f"    Created: {archive['created']}")
        print(f"    Path: {archive['path']}")
        print()
    
    print("Overlay files are saved with timestamp numbers for easy identification.")
    print("Higher numbers = newer overlays")
    print("\nTo use an archived overlay in OBS:")
    print("1. Copy the desired overlay file")
    print("2. Rename it to 'overlay.html'")
    print("3. OBS will automatically use the updated overlay")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")