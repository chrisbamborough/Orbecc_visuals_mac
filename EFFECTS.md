# Visual Effects Guide

This document describes the visual effects implemented in the Orbecc Visual Effects application.

## Effect Components

### 1. Particle System

The particle system is the primary visual effect that responds to both motion and audio.

#### Particle Properties
- **Position (x, y)**: Randomly spawned across the screen
- **Velocity (vx, vy)**: Influenced by motion level (more motion = faster particles)
- **Size**: Influenced by audio volume (louder = larger particles)
- **Color**: Determined by audio frequency (different frequencies = different colors)
- **Life**: Each particle has a lifetime and gradually fades out

#### Particle Behavior
1. **Spawning**: Number of new particles per frame = `(motion_level + audio_volume) * 20`
2. **Movement**: Particles move according to their velocity
3. **Aging**: Life decreases by 0.02 per frame (50 frames = 1 second at 60 FPS)
4. **Shrinking**: Size multiplied by 0.98 per frame
5. **Death**: Particles are removed when life ≤ 0 or size < 0.5

### 2. Background Waves

Animated sine waves that provide a dynamic background.

#### Wave Properties
- **Count**: 5 waves by default
- **Color**: HSV-based, different hue for each wave
- **Amplitude**: Increases with wave index (50 + i * 20 pixels)
- **Frequency**: 0.01 cycles per pixel
- **Speed**: Varies per wave (time * (i + 1) * 0.5)

#### Wave Formula
```
y = height/2 + sin(x * 0.01 + time * speed) * amplitude
```

### 3. Color System

Colors are generated using HSV (Hue, Saturation, Value) color space for smooth transitions.

#### Audio Frequency to Color Mapping
- Frequency range is normalized: `hue = (frequency / 1000.0) % 1.0`
- Low frequencies (0-333 Hz): Red to Yellow
- Mid frequencies (333-666 Hz): Green to Cyan
- High frequencies (666-1000 Hz): Blue to Magenta
- Above 1000 Hz: Cycles back through the spectrum

#### Background Wave Colors
- Wave 0: Red (hue = 0.0)
- Wave 1: Yellow (hue = 0.2)
- Wave 2: Cyan (hue = 0.4)
- Wave 3: Blue (hue = 0.6)
- Wave 4: Magenta (hue = 0.8)

## Responsiveness Levels

### Motion Detection
- **Low motion (0.0 - 0.1)**: Few slow particles
- **Medium motion (0.1 - 0.5)**: Moderate particle generation with visible movement
- **High motion (0.5 - 1.0)**: Intense particle generation with rapid movement

### Audio Volume
- **Quiet (0.0 - 0.2)**: Small particles, minimal spawning
- **Moderate (0.2 - 0.6)**: Medium-sized particles
- **Loud (0.6 - 1.0)**: Large particles, intense spawning

### Audio Frequency
- **Bass (20-250 Hz)**: Red/Orange particles
- **Midrange (250-2000 Hz)**: Green/Yellow/Cyan particles
- **Treble (2000+ Hz)**: Blue/Purple particles

## Performance Optimization

### Particle Management
- Maximum particles: 1000 (configurable)
- Particles are removed when they exceed the limit (oldest first)
- Dead particles are cleaned up each frame

### Rendering Optimization
- Background cleared once per frame
- Waves drawn as line segments (efficient)
- Particles use simple circle drawing
- Frame rate capped at 60 FPS

## Customization Ideas

### Easy Modifications
1. **Change colors**: Modify the HSV values in `_hsv_to_rgb()` calls
2. **Adjust sensitivity**: Change amplification factors in motion/audio getters
3. **Particle lifespan**: Modify the life decrement rate (default: 0.02)
4. **Wave animation speed**: Adjust the time multiplier for waves

### Advanced Modifications
1. **Add new particle shapes**: Use pygame.draw polygon/rect/etc
2. **Implement trails**: Keep particle history and draw lines
3. **Add gravity**: Modify vy by adding a constant each frame
4. **Collision detection**: Make particles bounce off edges
5. **Audio beat detection**: Detect beats and create pulse effects
6. **Depth-based effects**: Use actual depth data from Orbecc Astra Pro

## Technical Details

### Frame Timing
- Target: 60 FPS
- Time increment per frame: 0.016 seconds (1/60)
- Wave animation speed scales with this timing

### Coordinate System
- Origin (0,0) is top-left corner
- X increases to the right
- Y increases downward
- Default window: 1280x720 pixels

### Performance Metrics
- Typical particle count: 200-600 (depends on activity)
- Maximum particle count: 1000
- CPU usage: ~10-30% on modern hardware
- Memory usage: ~50-100 MB
