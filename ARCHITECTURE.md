# System Architecture

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORBECC VISUAL EFFECTS                         │
│                        Main Application                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ coordinates
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ CameraCapture │      │ AudioAnalyzer │      │ VisualEffects │
│               │      │               │      │               │
│ - Orbecc Cam  │      │ - Microphone  │      │ - Pygame      │
│ - USB Camera  │      │ - System Audio│      │ - Rendering   │
│ - OpenCV      │      │ - PyAudio     │      │ - Particles   │
└───────────────┘      └───────────────┘      └───────────────┘
        │                       │                       ▲
        │ capture               │ capture               │
        ▼                       ▼                       │
┌───────────────┐      ┌───────────────┐               │
│ Video Frames  │      │ Audio Stream  │               │
│ (640x480)     │      │ (44.1kHz)     │               │
└───────────────┘      └───────────────┘               │
        │                       │                       │
        │ process               │ process               │
        ▼                       ▼                       │
┌───────────────┐      ┌───────────────┐               │
│Frame Diff     │      │ FFT Analysis  │               │
│Gaussian Blur  │      │ RMS Volume    │               │
└───────────────┘      └───────────────┘               │
        │                       │                       │
        │ calculate             │ calculate             │
        ▼                       ▼                       │
┌───────────────┐      ┌───────────────┐               │
│ Motion Level  │      │ Volume Level  │               │
│ (0.0 - 1.0)   │      │ (0.0 - 1.0)   │               │
│               │      │               │               │
│ Frequency     │      │ Frequency     │               │
│ (Hz)          │      │ (Hz)          │               │
└───────────────┘      └───────────────┘               │
        │                       │                       │
        └───────────────┬───────┘                       │
                        │                               │
                        │ combine                       │
                        ▼                               │
                ┌───────────────┐                       │
                │ Effect Params │                       │
                │               │                       │
                │ - Spawn Rate  │                       │
                │ - Velocity    │                       │
                │ - Size        │                       │
                │ - Color       │                       │
                └───────────────┘                       │
                        │                               │
                        └───────────────────────────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ Visual Output │
                        │ (1280x720)    │
                        │               │
                        │ - Particles   │
                        │ - Waves       │
                        │ - Background  │
                        └───────────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ Display       │
                        │ (60 FPS)      │
                        └───────────────┘
```

## Component Interaction

### 1. Initialization Phase
```
OrbeecVisualsApp.__init__()
    │
    ├─> CameraCapture.__init__(index=0)
    │   └─> Sets up OpenCV VideoCapture
    │
    ├─> AudioAnalyzer.__init__(rate=44100, chunk=1024)
    │   └─> Sets up PyAudio stream
    │
    └─> VisualEffects.__init__(width=1280, height=720)
        └─> Initializes Pygame display and particle list
```

### 2. Startup Phase
```
OrbeecVisualsApp.start()
    │
    ├─> CameraCapture.start()
    │   ├─> Opens camera device
    │   └─> Sets resolution (640x480)
    │
    ├─> AudioAnalyzer.start()
    │   └─> Opens audio input stream
    │
    └─> Prints status and controls
```

### 3. Main Loop (60 FPS)
```
OrbeecVisualsApp.run()
    │
    └─> while running:
        │
        ├─> VisualEffects.handle_events()
        │   └─> Check for quit (ESC, Q, close)
        │
        ├─> CameraCapture.update()
        │   ├─> Read frame
        │   ├─> Convert to grayscale
        │   ├─> Apply Gaussian blur
        │   ├─> Compare with previous frame
        │   └─> Calculate motion_level
        │
        ├─> AudioAnalyzer.update()
        │   ├─> Read audio chunk
        │   ├─> Calculate RMS volume
        │   └─> Perform FFT for frequency
        │
        ├─> Get values:
        │   ├─> motion = CameraCapture.get_motion_level()
        │   ├─> volume = AudioAnalyzer.get_volume()
        │   └─> freq = AudioAnalyzer.get_frequency()
        │
        ├─> VisualEffects.update(motion, volume, freq)
        │   ├─> Spawn new particles based on motion + volume
        │   ├─> Set color based on frequency (HSV)
        │   ├─> Set size based on volume
        │   ├─> Set velocity based on motion
        │   ├─> Update existing particles
        │   └─> Remove dead particles
        │
        └─> VisualEffects.render()
            ├─> Clear screen
            ├─> Draw background waves
            ├─> Draw all particles
            └─> Flip display buffer
```

### 4. Shutdown Phase
```
OrbeecVisualsApp.stop()
    │
    ├─> CameraCapture.stop()
    │   └─> Release camera device
    │
    ├─> AudioAnalyzer.stop()
    │   └─> Close audio stream
    │
    └─> VisualEffects.cleanup()
        └─> Quit Pygame
```

## Data Structures

### Particle Object
```python
particle = {
    'x': float,          # X position (0 to width)
    'y': float,          # Y position (0 to height)
    'vx': float,         # X velocity (-5 to 5)
    'vy': float,         # Y velocity (-5 to 5)
    'size': float,       # Radius (5 to 25)
    'color': (R, G, B),  # RGB tuple (0-255)
    'life': float        # Remaining life (0.0 to 1.0)
}
```

### Effect Parameters
```python
spawn_rate = int((motion_level + audio_volume) * 20)  # 0-40 particles/frame
velocity_factor = motion_level * 10                    # 0-10
size_factor = 5 + audio_volume * 20                    # 5-25
hue = (audio_freq / 1000.0) % 1.0                     # 0.0-1.0
```

## Performance Characteristics

### Timing
- **Frame Time**: ~16.67ms (60 FPS)
- **Camera Update**: ~5-10ms
- **Audio Update**: ~1-2ms
- **Particle Update**: ~3-5ms (500 particles)
- **Rendering**: ~5-8ms

### Memory Usage
- **Base Application**: ~30-50 MB
- **Per Particle**: ~100 bytes
- **1000 Particles**: ~100 KB
- **Total Typical**: ~50-100 MB

### CPU Usage
- **Camera Processing**: 5-10%
- **Audio Processing**: 2-5%
- **Particle System**: 5-15%
- **Rendering**: 5-10%
- **Total Typical**: 10-30%

## Error Handling Flow

```
Start
  │
  ├─> Try Camera
  │   ├─> Success → Use motion detection
  │   └─> Fail → Use random motion (demo mode)
  │
  ├─> Try Audio
  │   ├─> Success → Use audio reactivity
  │   └─> Fail → Skip audio features
  │
  └─> Main Loop
      ├─> Try update camera
      │   └─> Fail → Continue without camera
      │
      ├─> Try update audio
      │   └─> Fail → Continue without audio
      │
      └─> Continue rendering (always works)
```

## Extension Points

### Easy Customizations
1. **New Particle Effects**: Modify `VisualEffects.update()`
2. **Background Changes**: Modify `VisualEffects.render()`
3. **Color Schemes**: Modify HSV calculations
4. **Motion Sensitivity**: Adjust threshold values

### Advanced Extensions
1. **3D Rendering**: Replace Pygame with PyOpenGL
2. **Depth Data**: Use Orbecc SDK for actual depth
3. **Multiple Cameras**: Add more CameraCapture instances
4. **MIDI Control**: Add MIDI input for parameter control
5. **Recording**: Add video encoding
6. **Network Streaming**: Add OSC/WebSocket support

---

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Independent component testing
- ✅ Easy extension and customization
- ✅ Robust error handling
- ✅ Real-time performance
- ✅ Resource efficiency
