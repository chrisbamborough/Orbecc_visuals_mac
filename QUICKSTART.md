# Quick Start Guide

## Getting Started in 5 Minutes

### Prerequisites
- macOS 10.14 or later
- Python 3.8+
- Orbecc Astra Pro camera (optional)

### Fast Installation

```bash
# 1. Clone the repository
git clone https://github.com/chrisbamborough/Orbecc_visuals_mac.git
cd Orbecc_visuals_mac

# 2. Run the installation script
chmod +x install.sh
./install.sh

# 3. Run the application
source venv/bin/activate
python3 orbecc_visuals.py
```

### Manual Installation

If the installation script doesn't work:

```bash
# Install PortAudio (for audio support)
brew install portaudio

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 orbecc_visuals.py
```

## First Run

When you first run the application:

1. **Camera Permission**: macOS will ask for camera access
   - Click "OK" to enable motion detection
   - Click "Don't Allow" to run in audio-only mode

2. **Microphone Permission**: macOS will ask for microphone access
   - Click "OK" to enable audio reactivity
   - Click "Don't Allow" to run in camera-only mode

3. **Visual Window**: A pygame window will open showing the visual effects
   - Move in front of the camera to see motion-reactive particles
   - Make sounds or play music to see audio-reactive effects

## Controls

- **ESC** or **Q**: Quit the application
- Just close the window: Also quits cleanly

## What You'll See

### With Camera Only
- Particles that spawn and move based on detected motion
- More movement = more particles with faster velocity
- Background waves animating

### With Audio Only
- Particles that spawn based on sound volume
- Particle size changes with volume
- Particle colors change with frequency (pitch)
- Background waves animating

### With Both Camera and Audio
- Combined effects from both inputs
- Rich, dynamic visualization
- Particles react to both movement and sound

## Troubleshooting

### "Camera not detected"
✓ The app will still run with audio-only mode
✓ Check camera connection and permissions
✓ Try a different camera index in the code

### "Audio not working"
✓ The app will still run with camera-only mode
✓ Check microphone permissions
✓ Verify default input device in System Preferences

### "ModuleNotFoundError"
✓ Make sure you activated the virtual environment: `source venv/bin/activate`
✓ Re-run: `pip install -r requirements.txt`

### Performance Issues
✓ Close other apps using camera/microphone
✓ Lower the window resolution in `orbecc_visuals.py`
✓ Reduce max_particles in the code

## Next Steps

1. **Customize**: Edit `orbecc_visuals.py` to change colors, particle behavior, etc.
2. **Configure**: Copy `config.example.json` to `config.json` and customize settings
3. **Explore**: Read `EFFECTS.md` to understand the visual effects system
4. **Develop**: Check out `README.md` for development guidelines

## Tips

- **Best Results**: Use in a dimly lit room for better visual impact
- **Music**: Play music through your speakers for great audio-reactive effects
- **Movement**: Try different speeds and types of movement
- **Combine**: Dance while music plays for the full experience!

## Getting Help

- Check the main `README.md` for detailed documentation
- Review `EFFECTS.md` for visual effects details
- Look at the code comments in `orbecc_visuals.py`

Enjoy creating visual effects with your Orbecc Astra Pro!
