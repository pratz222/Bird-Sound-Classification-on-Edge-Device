# Bird-Sound-Classification-on-Edge-Device
# Overview
This project implements real-time bird sound classification on a Raspberry Pi 5 using Edge Impulse and machine learning. The system can detect and identify specific bird species from audio input using a USB microphone.
The classifier is optimized to run efficiently on the Raspberry Pi 5 with 4GB RAM, making it an excellent example of edge AI implementation for wildlife monitoring.

## Supported Bird Species
The current model is trained to detect:

Asian Koel
Laughing Kookaburra
Rose-ringed Parakeet
Square-Tailed Drongo

## Hardware Requirements

Raspberry Pi 5 (4GB RAM model)
USB microphone or audio input device
Bluetooth earbuds/speakers (optional, for audio playback)
Power supply for Raspberry Pi
MicroSD card (16GB+ recommended)
Internet connection (for setup only)

## Software Requirements

Raspberry Pi OS (64-bit recommended)
Python 3.9+
Edge Impulse account (free)
VNC Server/Viewer (if accessing remotely)

## Quick Start

Clone this repository:

git clone [https://github.com/yourusername/bird-sound-classification.git ](https://github.com/pratz222/Bird-Sound-Classification-on-Edge-Device.git)

cd bird-sound-classification

Set up a virtual environment:
bashpython3 -m venv venv
source venv/bin/activate

Install dependencies:
bashpip install -r requirements.txt

Download the model (see Model Setup below)
Run the detection script:
bashpython detect_birds.py


## Detailed Setup
Environment Setup
This project uses a Python virtual environment to manage dependencies:
bash# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required system dependencies
sudo apt install -y python3-pip python3-venv portaudio19-dev

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Model Setup
The bird sound classification model is trained using Edge Impulse. To set up the model:

Create a free Edge Impulse account at Edge Impulse
Create a new project named "Bird Sound Classification"
Navigate to your Edge Impulse project dashboard
Either:

Upload your own bird sound dataset, or
Use a public dataset like "Bird Audio Detection"


Create an impulse with:

Audio (MFCC) processing block
Neural Network classification block


Train the model (MobileNetV2 0.1 recommended for Raspberry Pi 5)
Deploy as "Linux" target and download the .zip file
Extract in your project directory:
bashunzip edge-impulse-standalone.zip


Usage
Basic Usage
Run the main detection script:
bashpython detect_birds.py
The script will continuously listen for bird sounds and display detected species with their confidence levels in the terminal.

## Example Output

Listening for bird sounds...

classifyRes 1ms. {
  Asian_Koel: '0.5122',
  Laughing_Kookaburra: '0.4574',
  Rose-ringed_Parakeet: '0.0003',
  Square_Tailed_Drongo: '0.0001',
  _noise: '0.0300',
}

classifyRes 1543ms. {
  Asian_Koel: '0.1725',
  Laughing_Kookaburra: '0.3650',
  Rose-ringed_Parakeet: '0.0013',
  Square_Tailed_Drongo: '0.4281',
  _noise: '0.0330',
}

Collect audio samples of the new bird species
Add them to your Edge Impulse project
Retrain the model
Update the SPECIES list in detect_birds.py

Adjusting Sensitivity
To adjust detection sensitivity:

Modify the THRESHOLD value in detect_birds.py (default: 0.40)

Lower values increase sensitivity but may cause false positives
Higher values reduce sensitivity but increase confidence in detections

# Troubleshooting
Common Issues

USB Microphone Not Detected

Check connection with arecord -l
Ensure microphone permissions are set correctly


High CPU Usage

Adjust the sleep interval in the main loop
Reduce audio processing frequency


Low Detection Accuracy

Ensure quiet recording environment
Retrain model with more diverse samples
Adjust the detection threshold


## Acknowledgements

Edge Impulse for the machine learning platform
Raspberry Pi Foundation
Various open bird sound datasets used for training
