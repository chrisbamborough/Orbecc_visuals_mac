# Orbecc Visual Effects for macOS

A Python application that creates dynamic visual effects using the Orbecc Astra Pro camera and audio input on macOS. The visuals react in real-time to movement detected by the camera and sound captured from the microphone.

## Features

- **Movement Detection**: Analyzes camera frames to detect motion and uses it to drive particle effects
- **Audio Reactivity**: Captures microphone input and visualizes volume and frequency
- **Real-time Visual Effects**: 
  - Dynamic particle system
  - Animated background waves
  - Color variations based on audio frequency
  - Particle intensity based on motion and volume
- **Graceful Degradation**: Works without camera (audio-only mode) or without audio (motion-only mode)

## Requirements

- macOS (tested on macOS 10.14+)
- Python 3.8 or higher
- Orbecc Astra Pro camera (optional - will run in demo mode without it)
- Microphone access (optional)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/chrisbamborough/Orbecc_visuals_mac.git
cd Orbecc_visuals_mac
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. On macOS, you may need to install PortAudio for PyAudio:
```bash
brew install portaudio
```

## Usage

Run the application:
```bash
python3 orbecc_visuals.py
```

### Controls

- **ESC** or **Q**: Quit the application

### Permissions

On first run, macOS may ask for permissions:
- **Camera access**: Allow to enable motion detection
- **Microphone access**: Allow to enable audio reactivity

You can deny these permissions and the app will still run with reduced functionality.

## How It Works

### Camera/Motion Detection
- Captures frames from the Orbecc Astra Pro (or any connected camera)
- Converts frames to grayscale and applies Gaussian blur
- Compares consecutive frames to detect motion
- Calculates motion level based on pixel differences
- Uses motion level to control particle velocity and spawn rate

### Audio Analysis
- Captures audio from the default microphone
- Calculates volume using RMS (Root Mean Square)
- Performs FFT (Fast Fourier Transform) to detect dominant frequency
- Uses volume to control particle spawn rate and size
- Uses frequency to determine particle colors

### Visual Effects
- **Particles**: Generated based on motion and audio, with:
  - Position: Random within window
  - Velocity: Influenced by motion level
  - Size: Influenced by audio volume
  - Color: Influenced by audio frequency
  - Life: Gradually fades out
- **Background Waves**: Animated sine waves that add depth to the visualization

## Configuration

You can modify the following parameters in `orbecc_visuals.py`:

- **Window size**: Change `width` and `height` in `VisualEffects.__init__()`
- **Camera resolution**: Modify `CAP_PROP_FRAME_WIDTH` and `CAP_PROP_FRAME_HEIGHT`
- **Motion sensitivity**: Adjust the threshold in `CameraCapture.update()`
- **Audio sensitivity**: Modify the amplification factors in `AudioAnalyzer`
- **Particle behavior**: Tune parameters in `VisualEffects.update()`

## Troubleshooting

### Camera not detected
- Ensure the Orbecc Astra Pro is properly connected
- Check camera permissions in System Preferences > Security & Privacy > Camera
- The app will run in demo mode if no camera is detected

### Audio not working
- Check microphone permissions in System Preferences > Security & Privacy > Microphone
- Verify your microphone is set as the default input device
- The app will continue with visual-only mode if audio fails

### Performance issues
- Lower the window resolution in the code
- Reduce the maximum particle count
- Close other applications using the camera or microphone

## Development

### Project Structure
```
Orbecc_visuals_mac/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── orbecc_visuals.py        # Main application
```

### Adding Features

The code is organized into four main classes:
- `AudioAnalyzer`: Handles audio capture and analysis
- `CameraCapture`: Handles camera capture and motion detection
- `VisualEffects`: Manages the pygame rendering and effects
- `OrbeecVisualsApp`: Main application coordinator

To add new visual effects, modify the `VisualEffects` class.

## License

MIT License - feel free to use and modify for your projects.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Orbecc for the Astra Pro camera
- OpenCV for computer vision capabilities
- Pygame for graphics rendering
- PyAudio for audio capture