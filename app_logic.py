import requests
import os
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") # Get API key from .env
VOICE_ID = "21m00Tcm4TlvDq8ikWAM" # Rachel voice from ElevenLabs
OUTPUT_AUDIO_DIR = "generated_audio"
SAVED_OVERLAYS_DIR = "saved_overlays"
FAVORITES_DIR = "tts_favorites"
OVERLAY_HTML_PATH = "overlay.html" # This is the file OBS will read
FAVORITES_JSON_PATH = "tts_favorites.json" # Store favorites data

# Create directories if they don't exist
os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)
os.makedirs(SAVED_OVERLAYS_DIR, exist_ok=True)
os.makedirs(FAVORITES_DIR, exist_ok=True)

# --- Eleven Labs API Functions ---

def get_available_voices():
    """Fetches a list of custom voices only from Eleven Labs (excludes premade voices)."""
    if not ELEVENLABS_API_KEY:
        print("Error: ELEVENLABS_API_KEY not set.")
        return None

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Accept": "application/json"
    }
    url = "https://api.elevenlabs.io/v1/voices"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        voices_data = response.json()
        all_voices = voices_data.get("voices", [])
        
        # Filter for custom voices only (exclude premade ElevenLabs voices)
        custom_voices = []
        for voice in all_voices:
            # Custom voices typically have category "cloned" or are marked as custom
            category = voice.get("category", "").lower()
            sharing = voice.get("sharing", {})
            
            is_custom = (
                category == "cloned" or 
                category == "custom" or
                (sharing and sharing.get("status") == "private") or
                (sharing and not sharing.get("public_owner_id"))  # No public owner means it's custom
            )
            if is_custom:
                custom_voices.append(voice)
        
        return custom_voices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching voices: {e}")
        return None

def text_to_speech(text, voice_id=VOICE_ID, filename="output.mp3"):
    """
    Converts text to speech using Eleven Labs API and saves it to a file.
    Returns the path to the saved audio file.
    """
    if not ELEVENLABS_API_KEY:
        print("Error: ELEVENLABS_API_KEY not set.")
        return None

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1", # Or another model if you prefer
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    output_path = os.path.join(OUTPUT_AUDIO_DIR, filename)

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Audio saved to {output_path}")
        return output_path
    except requests.exceptions.RequestException as e:
        print(f"Error during text-to-speech: {e}")
        return None

def generate_overlay_html(main_text, sub_text="", save_archive=True):
    """
    Generates or updates the HTML file for the OBS overlay.
    Optionally saves numbered archive copies.
    """
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoiceMaster Overlay</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden; /* Hide scrollbars if content overflows */
            background-color: rgba(0, 0, 0, 0); /* Transparent background */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #ffffff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); /* Subtle shadow for readability */
        }}
        .overlay-container {{
            position: absolute;
            bottom: 20px; /* Adjust as needed */
            left: 20px; /* Adjust as needed */
            background-color: rgba(44, 62, 80, 0.7); /* Semi-transparent dark blue */
            padding: 10px 20px;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            gap: 5px;
            align-items: flex-start;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }}
        .main-text {{
            font-size: 2em; /* Larger for main title */
            font-weight: bold;
            line-height: 1.2;
        }}
        .sub-text {{
            font-size: 1.2em; /* Smaller for additional info */
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="overlay-container">
        <div class="main-text">{main_text}</div>
        {'<div class="sub-text">' + sub_text + '</div>' if sub_text else ''}
    </div>
</body>
</html>
    """
    try:
        # Write the current overlay file
        with open(OVERLAY_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Overlay HTML updated: {OVERLAY_HTML_PATH}")
        
        # Save numbered archive copy if requested
        if save_archive:
            timestamp = int(time.time())
            archive_filename = f"overlay_{timestamp:010d}.html"
            archive_path = os.path.join(SAVED_OVERLAYS_DIR, archive_filename)
            
            with open(archive_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Overlay archived: {archive_path}")
            
    except IOError as e:
        print(f"Error writing overlay HTML: {e}")


def load_favorites():
    """Load TTS favorites from JSON file."""
    try:
        if os.path.exists(FAVORITES_JSON_PATH):
            with open(FAVORITES_JSON_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading favorites: {e}")
    return []


def save_favorites(favorites):
    """Save TTS favorites to JSON file."""
    try:
        with open(FAVORITES_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(favorites, f, indent=2, ensure_ascii=False)
        print(f"Favorites saved to {FAVORITES_JSON_PATH}")
    except Exception as e:
        print(f"Error saving favorites: {e}")


def add_favorite(text, voice_id, voice_name, audio_filename=None):
    """Add a TTS comment to favorites."""
    favorites = load_favorites()
    
    # Generate unique ID for this favorite
    favorite_id = int(time.time())
    
    favorite = {
        "id": favorite_id,
        "text": text,
        "voice_id": voice_id,
        "voice_name": voice_name,
        "audio_filename": audio_filename,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": favorite_id
    }
    
    favorites.append(favorite)
    save_favorites(favorites)
    
    print(f"Added favorite: '{text[:50]}...' with voice '{voice_name}'")
    return favorite_id


def get_favorite_phrases():
    """Get all favorite phrases for quick access."""
    favorites = load_favorites()
    # Sort by timestamp (newest first)
    favorites.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
    return favorites


def delete_favorite(favorite_id):
    """Delete a favorite by ID."""
    favorites = load_favorites()
    favorites = [f for f in favorites if f.get('id') != favorite_id]
    save_favorites(favorites)
    print(f"Deleted favorite with ID: {favorite_id}")


def get_overlay_archive_list():
    """Get list of archived overlay files, sorted by number (newest first)."""
    try:
        files = []
        for filename in os.listdir(SAVED_OVERLAYS_DIR):
            if filename.startswith('overlay_') and filename.endswith('.html'):
                timestamp = filename.replace('overlay_', '').replace('.html', '')
                try:
                    timestamp_int = int(timestamp)
                    files.append({
                        'filename': filename,
                        'timestamp': timestamp_int,
                        'path': os.path.join(SAVED_OVERLAYS_DIR, filename),
                        'created': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp_int))
                    })
                except ValueError:
                    continue
        
        # Sort by timestamp (newest first)
        files.sort(key=lambda x: x['timestamp'], reverse=True)
        return files
    except Exception as e:
        print(f"Error getting overlay archive list: {e}")
        return []


# --- Example Usage (How you'd integrate this in your app's main loop/GUI actions) ---
if __name__ == "__main__":
    print("--- VoiceMaster App Logic Example ---")

    # 1. Fetch and display custom voices only (for your voice selection dropdown)
    print("\nFetching available custom voices...")
    voices = get_available_voices()
    if voices:
        print(f"Found {len(voices)} custom voices:")
        for voice in voices:
            print(f"- {voice['name']} (ID: {voice['voice_id']})")
            # You'd populate your GUI dropdown with these
        
        # Use the first custom voice as default if available
        selected_voice_id = voices[0]['voice_id']
        selected_voice_name = voices[0]['name']
        print(f"\nUsing first custom voice: {selected_voice_name} (ID: {selected_voice_id})")
    else:
        print("No custom voices found. Please create custom voices in your ElevenLabs account.")
        selected_voice_id = None

    # You would get this text from your GUI input
    script_text = "Hello, everyone! Welcome to VoiceMaster Pro. Today, we're discussing the future of AI voices."
    
    # Only proceed if we have custom voices available
    if ELEVENLABS_API_KEY and selected_voice_id:
        print(f"\nConverting text to speech using custom voice '{selected_voice_name}' (ID: {selected_voice_id})...")
        audio_file = text_to_speech(
            script_text,
            voice_id=selected_voice_id,
            filename="my_youtube_segment.mp3"
        )
        if audio_file:
            print(f"Successfully generated: {audio_file}")
        else:
            print("Failed to generate audio.")

        # 2. Update OBS Overlay
        print("\nUpdating OBS overlay...")
        generate_overlay_html(
            main_text=f"VOICEMASTER PRO: {selected_voice_name}",
            sub_text="Custom AI Voice Active"
        )
    else:
        print("\nSkipping TTS and overlay generation due to missing API key or voice ID.")