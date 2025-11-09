# Examples and Use Cases

This document provides examples of how to use and customize the Orbecc Visual Effects application.

## Basic Usage

### Starting the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python3 orbecc_visuals.py
```

### Stopping the Application

- Press `ESC` key
- Press `Q` key
- Close the window
- Press `Ctrl+C` in the terminal

## Use Cases

### 1. Live Music Visualization

Perfect for:
- DJ sets
- Live performances
- Music production
- Personal music listening

**Setup:**
1. Connect Orbecc camera
2. Position camera to capture audience/dancer
3. Route music to system audio (internal or external)
4. Run the application

**Result:** Visuals that react to both the music and movement

### 2. Interactive Art Installation

Perfect for:
- Museums
- Galleries
- Public spaces
- Events

**Setup:**
1. Mount camera at viewing height
2. Set up projection screen or large display
3. Optionally add ambient music
4. Run in fullscreen mode

**Result:** Visitors interact with visuals through movement

### 3. Motion-Based Game/Toy

Perfect for:
- Children's activities
- Physical therapy exercises
- Interactive play
- Movement tracking

**Setup:**
1. Position camera to capture full body
2. Disable audio or use quiet mode
3. Run the application

**Result:** Movement creates particle effects

### 4. Meditation/Relaxation Tool

Perfect for:
- Meditation sessions
- Relaxation exercises
- Breathing exercises
- Calming visuals

**Setup:**
1. Use gentle music or nature sounds
2. Minimize motion detection sensitivity
3. Use calming color schemes

**Result:** Gentle, flowing visuals

## Customization Examples

### Change Window Size

Edit `orbecc_visuals.py`:

```python
# Change from default 1280x720 to fullscreen
class OrbeecVisualsApp:
    def __init__(self):
        # For fullscreen
        self.visuals = VisualEffects(width=1920, height=1080)
```

Or use pygame's fullscreen mode:

```python
# In VisualEffects.__init__
self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
```

### Adjust Motion Sensitivity

Edit `orbecc_visuals.py`, in `CameraCapture.update()`:

```python
# More sensitive (lower threshold)
thresh = cv2.threshold(frame_delta, 15, 255, cv2.THRESH_BINARY)[1]

# Less sensitive (higher threshold)
thresh = cv2.threshold(frame_delta, 35, 255, cv2.THRESH_BINARY)[1]
```

### Change Color Scheme

Edit `orbecc_visuals.py`, in `VisualEffects.update()`:

```python
# Original (rainbow based on frequency)
hue = (audio_freq / 1000.0) % 1.0

# Blue/Purple only
hue = 0.6 + (audio_freq / 1000.0) * 0.2

# Red/Orange only
hue = (audio_freq / 1000.0) * 0.1

# Green/Cyan only
hue = 0.3 + (audio_freq / 1000.0) * 0.2
```

### Adjust Particle Lifetime

Edit `orbecc_visuals.py`, in `VisualEffects.update()`:

```python
# Longer lifetime (particles last longer)
particle['life'] -= 0.01  # Default is 0.02

# Shorter lifetime (particles disappear faster)
particle['life'] -= 0.04
```

### Change Background

Edit `orbecc_visuals.py`, in `VisualEffects.render()`:

```python
# Darker background
self.screen.fill((5, 5, 10))

# Lighter background
self.screen.fill((30, 30, 40))

# Colored background (dark blue)
self.screen.fill((10, 10, 40))
```

### Disable Background Waves

Edit `orbecc_visuals.py`, in `VisualEffects.render()`:

```python
# Comment out the wave drawing section
# for i in range(5):
#     offset = self.time * (i + 1) * 0.5
#     ...
```

### Increase Maximum Particles

Edit `orbecc_visuals.py`, in `VisualEffects.update()`:

```python
# Increase from 1000 to 2000
if len(self.particles) > 2000:
    self.particles = self.particles[-2000:]
```

### Add Gravity Effect

Edit `orbecc_visuals.py`, in `VisualEffects.update()`:

```python
# In the particle update section
for particle in self.particles:
    particle['x'] += particle['vx']
    particle['y'] += particle['vy']
    particle['vy'] += 0.2  # Add gravity
    particle['life'] -= 0.02
    particle['size'] *= 0.98
```

### Make Particles Bounce

Edit `orbecc_visuals.py`, in `VisualEffects.update()`:

```python
# In the particle update section
for particle in self.particles:
    particle['x'] += particle['vx']
    particle['y'] += particle['vy']
    
    # Bounce off walls
    if particle['x'] < 0 or particle['x'] > self.width:
        particle['vx'] *= -0.8
        particle['x'] = max(0, min(self.width, particle['x']))
    
    if particle['y'] < 0 or particle['y'] > self.height:
        particle['vy'] *= -0.8
        particle['y'] = max(0, min(self.height, particle['y']))
    
    particle['life'] -= 0.02
    particle['size'] *= 0.98
```

## Advanced Examples

### Multiple Camera Support

```python
# In orbecc_visuals.py, modify OrbeecVisualsApp.__init__
def __init__(self):
    self.camera1 = CameraCapture(camera_index=0)
    self.camera2 = CameraCapture(camera_index=1)
    # Use average of both cameras for motion
```

### Record Output

Use a screen recording tool:
- macOS: QuickTime Player > File > New Screen Recording
- OBS Studio: Free, open-source recording software

### Use with Projector

1. Connect projector to Mac
2. Set projector as primary display or extended display
3. Run application in fullscreen on projector

### Integration with Other Software

Export visual data:

```python
# Add to VisualEffects class
def get_metrics(self):
    return {
        'particle_count': len(self.particles),
        'avg_particle_size': np.mean([p['size'] for p in self.particles]),
        'avg_particle_life': np.mean([p['life'] for p in self.particles])
    }
```

## Performance Tips

### For Better Performance

1. **Lower Resolution:**
   ```python
   self.visuals = VisualEffects(width=800, height=600)
   ```

2. **Reduce Camera Resolution:**
   ```python
   self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
   self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   ```

3. **Limit Particles:**
   ```python
   if len(self.particles) > 500:  # Lower from 1000
   ```

4. **Lower Frame Rate:**
   ```python
   self.clock.tick(30)  # Down from 60
   ```

### For Better Quality

1. **Increase Resolution:**
   ```python
   self.visuals = VisualEffects(width=1920, height=1080)
   ```

2. **More Particles:**
   ```python
   num_particles = int((motion_level + audio_volume) * 40)  # Up from 20
   ```

3. **Smoother Motion:**
   ```python
   self.clock.tick(120)  # Up from 60
   ```

## Debugging

### Enable Debug Output

Add to `OrbeecVisualsApp.run()`:

```python
def run(self):
    self.running = True
    frame_count = 0
    
    while self.running:
        # Existing code...
        
        # Debug output every 60 frames (1 second at 60 FPS)
        frame_count += 1
        if frame_count % 60 == 0:
            print(f"Motion: {motion:.2f}, Volume: {volume:.2f}, "
                  f"Freq: {freq:.0f}Hz, Particles: {len(self.visuals.particles)}")
```

### Test Without Hardware

The application works without camera or microphone:
- Without camera: Uses random motion values
- Without audio: Skips audio analysis
- Without both: Still shows animated background

## Community Examples

Share your customizations! Fork the repository and submit pull requests with:
- New visual effects
- Color schemes
- Particle behaviors
- Integration examples

Enjoy creating with Orbecc Visual Effects!
