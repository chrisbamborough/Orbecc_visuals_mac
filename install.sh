#!/bin/bash

# Installation script for Orbecc Visual Effects on macOS

echo "========================================="
echo "Orbecc Visual Effects - Installation"
echo "========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Found Python version: $PYTHON_VERSION"

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Warning: Homebrew is not installed."
    echo "PortAudio installation may be required for PyAudio."
    echo "Install Homebrew from https://brew.sh/"
    echo ""
else
    echo "Homebrew found, checking for PortAudio..."
    
    # Install PortAudio if not present
    if ! brew list portaudio &> /dev/null; then
        echo "Installing PortAudio..."
        brew install portaudio
    else
        echo "PortAudio already installed"
    fi
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "========================================="
echo "Installation complete!"
echo "========================================="
echo ""
echo "To run the application:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo "  2. Run the application:"
echo "     python3 orbecc_visuals.py"
echo ""
echo "To deactivate the virtual environment later:"
echo "  deactivate"
echo ""
