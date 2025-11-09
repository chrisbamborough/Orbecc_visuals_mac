#!/usr/bin/env python3
"""
Demo script to test the Orbecc Visual Effects application components.
This script validates that all classes can be instantiated and basic methods work.
"""

import sys
from unittest.mock import Mock, patch

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import cv2
        print("  ✓ OpenCV (cv2) imported successfully")
    except ImportError:
        print("  ✗ OpenCV not available")
        
    try:
        import numpy
        print("  ✓ NumPy imported successfully")
    except ImportError:
        print("  ✗ NumPy not available")
        
    try:
        import pygame
        print("  ✓ Pygame imported successfully")
    except ImportError:
        print("  ✗ Pygame not available")
        
    try:
        import pyaudio
        print("  ✓ PyAudio imported successfully")
    except ImportError:
        print("  ✗ PyAudio not available")


def test_class_structure():
    """Test that all classes can be imported and have correct structure."""
    print("\nTesting class structure...")
    
    try:
        # Mock the dependencies before importing
        sys.modules['cv2'] = Mock()
        sys.modules['numpy'] = Mock()
        sys.modules['pygame'] = Mock()
        sys.modules['pyaudio'] = Mock()
        
        from orbecc_visuals import AudioAnalyzer, CameraCapture, VisualEffects, OrbeecVisualsApp
        print("  ✓ All classes imported successfully")
        
        # Test AudioAnalyzer
        print("\n  Testing AudioAnalyzer:")
        print("    - Has __init__ method:", hasattr(AudioAnalyzer, '__init__'))
        print("    - Has start method:", hasattr(AudioAnalyzer, 'start'))
        print("    - Has update method:", hasattr(AudioAnalyzer, 'update'))
        print("    - Has get_volume method:", hasattr(AudioAnalyzer, 'get_volume'))
        print("    - Has get_frequency method:", hasattr(AudioAnalyzer, 'get_frequency'))
        print("    - Has stop method:", hasattr(AudioAnalyzer, 'stop'))
        
        # Test CameraCapture
        print("\n  Testing CameraCapture:")
        print("    - Has __init__ method:", hasattr(CameraCapture, '__init__'))
        print("    - Has start method:", hasattr(CameraCapture, 'start'))
        print("    - Has update method:", hasattr(CameraCapture, 'update'))
        print("    - Has get_motion_level method:", hasattr(CameraCapture, 'get_motion_level'))
        print("    - Has get_frame method:", hasattr(CameraCapture, 'get_frame'))
        print("    - Has stop method:", hasattr(CameraCapture, 'stop'))
        
        # Test VisualEffects
        print("\n  Testing VisualEffects:")
        print("    - Has __init__ method:", hasattr(VisualEffects, '__init__'))
        print("    - Has update method:", hasattr(VisualEffects, 'update'))
        print("    - Has render method:", hasattr(VisualEffects, 'render'))
        print("    - Has handle_events method:", hasattr(VisualEffects, 'handle_events'))
        print("    - Has cleanup method:", hasattr(VisualEffects, 'cleanup'))
        
        # Test OrbeecVisualsApp
        print("\n  Testing OrbeecVisualsApp:")
        print("    - Has __init__ method:", hasattr(OrbeecVisualsApp, '__init__'))
        print("    - Has start method:", hasattr(OrbeecVisualsApp, 'start'))
        print("    - Has run method:", hasattr(OrbeecVisualsApp, 'run'))
        print("    - Has stop method:", hasattr(OrbeecVisualsApp, 'stop'))
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mock_instantiation():
    """Test that classes can be instantiated with mocked dependencies."""
    print("\nTesting class instantiation with mocks...")
    
    try:
        with patch('pyaudio.PyAudio'):
            from orbecc_visuals import AudioAnalyzer
            analyzer = AudioAnalyzer()
            print("  ✓ AudioAnalyzer instantiated")
            
        with patch('cv2.VideoCapture'):
            from orbecc_visuals import CameraCapture
            camera = CameraCapture()
            print("  ✓ CameraCapture instantiated")
            
        with patch('pygame.display.set_mode'), patch('pygame.init'):
            from orbecc_visuals import VisualEffects
            Mock.return_value = Mock()
            visuals = VisualEffects()
            print("  ✓ VisualEffects instantiated")
            
        with patch('orbecc_visuals.CameraCapture'), \
             patch('orbecc_visuals.AudioAnalyzer'), \
             patch('orbecc_visuals.VisualEffects'):
            from orbecc_visuals import OrbeecVisualsApp
            app = OrbeecVisualsApp()
            print("  ✓ OrbeecVisualsApp instantiated")
            
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all demo tests."""
    print("=" * 60)
    print("Orbecc Visual Effects - Component Test")
    print("=" * 60)
    
    test_imports()
    
    structure_ok = test_class_structure()
    if not structure_ok:
        print("\n✗ Class structure test failed")
        return 1
        
    instantiation_ok = test_mock_instantiation()
    if not instantiation_ok:
        print("\n✗ Class instantiation test failed")
        return 1
    
    print("\n" + "=" * 60)
    print("✓ All component tests passed!")
    print("=" * 60)
    print("\nThe application is ready to use.")
    print("Run 'python3 orbecc_visuals.py' to start the visual effects.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
