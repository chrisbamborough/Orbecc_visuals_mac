"""
Unit tests for Orbecc Visual Effects application.

Note: These tests validate the structure and basic functionality.
Full integration testing requires hardware (camera, microphone).
"""

import unittest
import numpy as np
from unittest.mock import Mock, patch, MagicMock


class TestAudioAnalyzer(unittest.TestCase):
    """Test the AudioAnalyzer class."""
    
    @patch('pyaudio.PyAudio')
    def test_initialization(self, mock_pyaudio):
        """Test AudioAnalyzer initialization."""
        from orbecc_visuals import AudioAnalyzer
        
        analyzer = AudioAnalyzer(rate=44100, chunk=1024)
        self.assertEqual(analyzer.rate, 44100)
        self.assertEqual(analyzer.chunk, 1024)
        self.assertEqual(analyzer.volume, 0.0)
        self.assertEqual(analyzer.frequency, 0.0)
    
    @patch('pyaudio.PyAudio')
    def test_get_volume(self, mock_pyaudio):
        """Test volume getter."""
        from orbecc_visuals import AudioAnalyzer
        
        analyzer = AudioAnalyzer()
        analyzer.volume = 0.5
        
        # Should be amplified by 5.0
        volume = analyzer.get_volume()
        self.assertLessEqual(volume, 1.0)
        self.assertGreaterEqual(volume, 0.0)


class TestCameraCapture(unittest.TestCase):
    """Test the CameraCapture class."""
    
    @patch('cv2.VideoCapture')
    def test_initialization(self, mock_videocapture):
        """Test CameraCapture initialization."""
        from orbecc_visuals import CameraCapture
        
        camera = CameraCapture(camera_index=0)
        self.assertEqual(camera.camera_index, 0)
        self.assertIsNone(camera.frame)
        self.assertEqual(camera.motion_level, 0.0)
    
    @patch('cv2.VideoCapture')
    def test_get_motion_level(self, mock_videocapture):
        """Test motion level getter."""
        from orbecc_visuals import CameraCapture
        
        camera = CameraCapture()
        camera.motion_level = 0.05
        
        # Should be amplified by 10.0 but capped at 1.0
        motion = camera.get_motion_level()
        self.assertLessEqual(motion, 1.0)
        self.assertGreaterEqual(motion, 0.0)


class TestVisualEffects(unittest.TestCase):
    """Test the VisualEffects class."""
    
    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_initialization(self, mock_init, mock_set_mode):
        """Test VisualEffects initialization."""
        from orbecc_visuals import VisualEffects
        
        mock_set_mode.return_value = Mock()
        visuals = VisualEffects(width=800, height=600)
        
        self.assertEqual(visuals.width, 800)
        self.assertEqual(visuals.height, 600)
        self.assertEqual(len(visuals.particles), 0)
    
    @patch('pygame.display.set_mode')
    @patch('pygame.init')
    def test_hsv_to_rgb(self, mock_init, mock_set_mode):
        """Test HSV to RGB conversion."""
        from orbecc_visuals import VisualEffects
        
        mock_set_mode.return_value = Mock()
        visuals = VisualEffects()
        
        # Test red (h=0)
        r, g, b = visuals._hsv_to_rgb(0.0, 1.0, 1.0)
        self.assertEqual(r, 255)
        self.assertEqual(g, 0)
        self.assertEqual(b, 0)
        
        # Test values are in valid range
        r, g, b = visuals._hsv_to_rgb(0.5, 0.5, 0.5)
        self.assertGreaterEqual(r, 0)
        self.assertLessEqual(r, 255)
        self.assertGreaterEqual(g, 0)
        self.assertLessEqual(g, 255)
        self.assertGreaterEqual(b, 0)
        self.assertLessEqual(b, 255)


class TestOrbeecVisualsApp(unittest.TestCase):
    """Test the main application class."""
    
    @patch('orbecc_visuals.VisualEffects')
    @patch('orbecc_visuals.AudioAnalyzer')
    @patch('orbecc_visuals.CameraCapture')
    def test_initialization(self, mock_camera, mock_audio, mock_visuals):
        """Test application initialization."""
        from orbecc_visuals import OrbeecVisualsApp
        
        app = OrbeecVisualsApp()
        self.assertIsNotNone(app.camera)
        self.assertIsNotNone(app.audio)
        self.assertIsNotNone(app.visuals)
        self.assertFalse(app.running)


if __name__ == '__main__':
    unittest.main()
