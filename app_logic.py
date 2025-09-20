import requests
import os
import json
import time
import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
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


# --- Speech Recognition Functions ---

def get_microphone_list():
    """Get list of available microphones."""
    try:
        mics = []
        for i in range(pyaudio.PyAudio().get_device_count()):
            device_info = pyaudio.PyAudio().get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                mics.append({
                    'index': i,
                    'name': device_info['name'],
                    'channels': device_info['maxInputChannels']
                })
        return mics
    except Exception as e:
        print(f"Error getting microphone list: {e}")
        return []


def record_audio_from_microphone(duration=5, mic_index=None):
    """Record audio from microphone for specified duration."""
    try:
        r = sr.Recognizer()
        
        # Use specific microphone or default
        if mic_index is not None:
            mic = sr.Microphone(device_index=mic_index)
        else:
            mic = sr.Microphone()
        
        print(f"Recording for {duration} seconds...")
        
        with mic as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("🎤 Recording started...")
            
            # Record audio
            audio = r.listen(source, timeout=duration, phrase_time_limit=duration)
            
        print("✅ Recording completed!")
        return audio
        
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None


def record_until_silence(mic_index=None, silence_threshold=1.0):
    """Record audio until silence is detected."""
    try:
        r = sr.Recognizer()
        
        # Use specific microphone or default
        if mic_index is not None:
            mic = sr.Microphone(device_index=mic_index)
        else:
            mic = sr.Microphone()
        
        print("🎤 Recording... (speak now, will stop automatically)")
        
        with mic as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            # Record with automatic silence detection
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            
        print("✅ Recording completed!")
        return audio
        
    except sr.WaitTimeoutError:
        print("⏰ Recording timed out")
        return None
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None


def speech_to_text(audio_data, engine="google"):
    """Convert recorded audio to text using speech recognition."""
    if audio_data is None:
        return None
        
    try:
        r = sr.Recognizer()
        
        if engine == "google":
            # Use Google Speech Recognition (free, but requires internet)
            text = r.recognize_google(audio_data)
        elif engine == "whisper":
            # Use OpenAI Whisper (more accurate, works offline if installed)
            text = r.recognize_whisper(audio_data)
        else:
            # Default to Google
            text = r.recognize_google(audio_data)
            
        print(f"🎯 Recognized text: '{text}'")
        return text
        
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"❌ Error with speech recognition service: {e}")
        return None
    except Exception as e:
        print(f"❌ Error in speech recognition: {e}")
        return None


def speech_to_cloned_voice(duration=5, voice_id=None, mic_index=None, filename=None):
    """Complete pipeline: Record speech -> Convert to text -> Generate with cloned voice."""
    try:
        # Step 1: Record audio
        print("🎤 Starting speech-to-clone pipeline...")
        audio_data = record_audio_from_microphone(duration, mic_index)
        
        if audio_data is None:
            return None, None
            
        # Step 2: Convert to text
        print("🔄 Converting speech to text...")
        text = speech_to_text(audio_data)
        
        if text is None:
            return None, None
            
        # Step 3: Generate speech with cloned voice
        print(f"🎭 Generating cloned speech: '{text}'")
        if filename is None:
            timestamp = int(time.time())
            filename = f"cloned_speech_{timestamp}.mp3"
            
        audio_file = text_to_speech(text, voice_id, filename)
        
        return text, audio_file
        
    except Exception as e:
        print(f"Error in speech-to-clone pipeline: {e}")
        return None, None


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