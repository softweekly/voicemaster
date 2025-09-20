import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY") # Get API key from .env
VOICE_ID = "21m00Tcm4TlvDq8ikWAM" # Rachel voice from ElevenLabs
OUTPUT_AUDIO_DIR = "generated_audio"
OVERLAY_HTML_PATH = "overlay.html" # This is the file OBS will read

# Create directories if they don't exist
os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)

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

# --- OBS Overlay Generation Function ---

def generate_overlay_html(main_text, sub_text=""):
    """
    Generates or updates the HTML file for the OBS overlay.
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
        with open(OVERLAY_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Overlay HTML updated: {OVERLAY_HTML_PATH}")
    except IOError as e:
        print(f"Error writing overlay HTML: {e}")


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