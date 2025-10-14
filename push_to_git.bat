@echo off
echo "Pushing voice parameter feature to git..."
echo.

echo "Checking git status..."
git status
echo.

echo "Adding all files..."
git add .
echo.

echo "Committing changes..."
git commit -m "Add advanced voice parameter controls with balanced layout

- Added professional voice parameter sliders (stability, similarity, style, speed)
- Implemented 2x2 grid layout for voice controls  
- Updated text_to_speech function to support custom voice parameters
- Enhanced GUI with real-time parameter adjustment
- Updated to ElevenLabs v2 model (eleven_monolingual_v2)
- Balanced layout: 35%% voice parameters, 30%% text input
- Added reset to defaults functionality
- Integrated with existing scaling and theming systems"
echo.

echo "Pushing to remote repository..."
git push origin main
echo.

echo "Git push completed!"
pause