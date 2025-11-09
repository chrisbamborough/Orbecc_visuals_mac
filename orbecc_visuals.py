#!/usr/bin/env python3
"""
Orbecc Astra Pro Visual Effects Application for macOS

This application captures data from an Orbecc Astra Pro camera and audio input,
then generates visual effects that react to movement and sound.
"""

import cv2
import numpy as np
import pygame
import pyaudio
import sys
import time
from typing import Tuple, Optional


class AudioAnalyzer:
    """Analyzes audio input and extracts features for visualization."""
    
    def __init__(self, rate=44100, chunk=1024):
        self.rate = rate
        self.chunk = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.volume = 0.0
        self.frequency = 0.0
        
    def start(self):
        """Start audio capture."""
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            print("Audio capture started")
        except Exception as e:
            print(f"Warning: Could not start audio capture: {e}")
            
    def update(self):
        """Update audio analysis."""
        if self.stream is None:
            return
            
        try:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Calculate volume (RMS)
            self.volume = np.sqrt(np.mean(audio_data**2)) / 32768.0
            
            # Simple frequency detection using FFT
            fft = np.fft.fft(audio_data)
            freqs = np.fft.fftfreq(len(fft))
            peak_freq = freqs[np.argmax(np.abs(fft))]
            self.frequency = abs(peak_freq * self.rate)
            
        except Exception as e:
            print(f"Audio update error: {e}")
            
    def get_volume(self) -> float:
        """Get current audio volume (0.0 to 1.0)."""
        return min(self.volume * 5.0, 1.0)  # Amplify for better response
        
    def get_frequency(self) -> float:
        """Get dominant frequency in Hz."""
        return self.frequency
        
    def stop(self):
        """Stop audio capture and cleanup."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()


class CameraCapture:
    """Captures RGB and depth data from Orbecc Astra Pro camera."""
    
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.frame = None
        self.prev_frame = None
        self.motion_level = 0.0
        
    def start(self):
        """Initialize camera capture."""
        # Try to open camera (RGB stream)
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            print(f"Warning: Could not open camera {self.camera_index}")
            print("Running in demo mode without camera")
            return False
            
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print(f"Camera {self.camera_index} opened successfully")
        return True
        
    def update(self):
        """Capture and process a new frame."""
        if self.cap is None or not self.cap.isOpened():
            # Demo mode: generate synthetic motion
            self.motion_level = np.random.random() * 0.3
            return
            
        ret, frame = self.cap.read()
        if not ret:
            return
            
        # Convert to grayscale for motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        self.frame = frame
        
        # Calculate motion
        if self.prev_frame is not None:
            frame_delta = cv2.absdiff(self.prev_frame, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            
            # Calculate motion level as percentage of pixels that changed
            self.motion_level = np.count_nonzero(thresh) / (thresh.shape[0] * thresh.shape[1])
        
        self.prev_frame = gray.copy()
        
    def get_motion_level(self) -> float:
        """Get current motion level (0.0 to 1.0)."""
        return min(self.motion_level * 10.0, 1.0)  # Amplify for better response
        
    def get_frame(self) -> Optional[np.ndarray]:
        """Get current camera frame."""
        return self.frame
        
    def stop(self):
        """Release camera resources."""
        if self.cap:
            self.cap.release()


class VisualEffects:
    """Generates visual effects based on movement and audio."""
    
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Orbecc Visual Effects")
        
        self.clock = pygame.time.Clock()
        self.particles = []
        self.time = 0
        
    def update(self, motion_level: float, audio_volume: float, audio_freq: float):
        """Update visual effects based on input parameters."""
        self.time += 0.016  # Approximate 60 FPS
        
        # Add new particles based on motion and audio
        num_particles = int((motion_level + audio_volume) * 20)
        for _ in range(num_particles):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            
            # Color based on audio frequency
            hue = (audio_freq / 1000.0) % 1.0
            color = self._hsv_to_rgb(hue, 0.8, 1.0)
            
            # Size based on audio volume
            size = 5 + audio_volume * 20
            
            # Velocity based on motion
            vx = (np.random.random() - 0.5) * motion_level * 10
            vy = (np.random.random() - 0.5) * motion_level * 10
            
            self.particles.append({
                'x': x, 'y': y,
                'vx': vx, 'vy': vy,
                'size': size,
                'color': color,
                'life': 1.0
            })
        
        # Update existing particles
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 0.02
            particle['size'] *= 0.98
            
        # Remove dead particles
        self.particles = [p for p in self.particles if p['life'] > 0 and p['size'] > 0.5]
        
        # Keep particle count reasonable
        if len(self.particles) > 1000:
            self.particles = self.particles[-1000:]
            
    def render(self):
        """Render the current frame."""
        # Clear screen with dark background
        self.screen.fill((10, 10, 20))
        
        # Draw background waves based on time
        for i in range(5):
            offset = self.time * (i + 1) * 0.5
            points = []
            for x in range(0, self.width, 10):
                y = self.height / 2 + np.sin(x * 0.01 + offset) * (50 + i * 20)
                points.append((x, int(y)))
            
            if len(points) > 1:
                color = self._hsv_to_rgb(i * 0.2, 0.5, 0.3)
                pygame.draw.lines(self.screen, color, False, points, 2)
        
        # Draw particles
        for particle in self.particles:
            alpha = int(particle['life'] * 255)
            color = tuple(int(c * particle['life']) for c in particle['color'])
            
            x = int(particle['x'])
            y = int(particle['y'])
            size = int(particle['size'])
            
            if 0 <= x < self.width and 0 <= y < self.height and size > 0:
                pygame.draw.circle(self.screen, color, (x, y), size)
        
        pygame.display.flip()
        self.clock.tick(60)
        
    def _hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convert HSV color to RGB."""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))
        
    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return False
        return True
        
    def cleanup(self):
        """Cleanup pygame resources."""
        pygame.quit()


class OrbeecVisualsApp:
    """Main application class."""
    
    def __init__(self):
        self.camera = CameraCapture()
        self.audio = AudioAnalyzer()
        self.visuals = VisualEffects()
        self.running = False
        
    def start(self):
        """Initialize and start the application."""
        print("Starting Orbecc Visual Effects Application")
        print("=" * 50)
        
        # Start camera
        camera_ok = self.camera.start()
        if not camera_ok:
            print("\nNote: Running without camera input")
            print("Visual effects will still work with audio only")
        
        # Start audio
        self.audio.start()
        
        print("\nControls:")
        print("  ESC or Q - Quit application")
        print("\nPress ESC or Q to exit...")
        print("=" * 50)
        
    def run(self):
        """Main application loop."""
        self.running = True
        
        while self.running:
            # Handle events
            if not self.visuals.handle_events():
                break
            
            # Update inputs
            self.camera.update()
            self.audio.update()
            
            # Get current values
            motion = self.camera.get_motion_level()
            volume = self.audio.get_volume()
            freq = self.audio.get_frequency()
            
            # Update and render visuals
            self.visuals.update(motion, volume, freq)
            self.visuals.render()
            
    def stop(self):
        """Cleanup and stop the application."""
        print("\nStopping application...")
        self.camera.stop()
        self.audio.stop()
        self.visuals.cleanup()
        print("Application stopped")


def main():
    """Main entry point."""
    app = OrbeecVisualsApp()
    
    try:
        app.start()
        app.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        app.stop()
        

if __name__ == "__main__":
    main()
