# Detailed Setup Instructions

This document provides comprehensive instructions for setting up the Bird Sound Classification project on a Raspberry Pi 5.

## Hardware Setup

### Required Components

1. **Raspberry Pi 5 (4GB RAM model)**
   - Make sure you have the latest Raspberry Pi OS installed
   - Recommended: Raspberry Pi OS 64-bit Bullseye or newer

2. **USB Microphone**
   - Connect to any available USB port on the Raspberry Pi
   - Condenser microphones work best for capturing distant bird sounds

3. **Power Supply**
   - Use an official Raspberry Pi 5 power supply (5V 5A)
   - Insufficient power can cause system instability

4. **MicroSD Card**
   - Minimum 16GB, Class 10 recommended
   - A high-quality card improves overall system performance

5. **Optional: Bluetooth Earbuds/Speakers**
   - For audio feedback when birds are detected
   - Must be paired with Raspberry Pi before starting

### Physical Setup

For optimal bird sound detection:

1. Place the USB microphone in a position with minimal background noise
2. Consider using a microphone extension cable to position it closer to areas birds frequent
3. If using outdoors, provide proper weatherproofing for all components
4. For permanent installations, consider a weatherproof enclosure

## Software Setup

### Base System Setup

1. **Install Raspberry Pi OS**
   ```bash
   # Download and use Raspberry Pi Imager to flash OS
   # https://www.raspberrypi.org/software/
   ```

2. **Initial Configuration**
   ```bash
   # Update system
   sudo apt update
   sudo apt upgrade -y
   
   # Enable SSH if needed
   sudo raspi-config
   # Interface Options > SSH > Enable
   
   # Set up VNC if accessing remotely
   sudo raspi-config
   # Interface Options > VNC > Enable
   ```

3. **Audio Configuration**
   ```bash
   # Check that your USB microphone is detected
   arecord -l
   
   # Test recording (press Ctrl+C to end)
   arecord -D plughw:1,0 -f cd test.wav
   
   # Test playback
   aplay test.wav
   
   # Set USB mic as default input (if needed)
   sudo nano /etc/asound.conf
   ```
   
   Add the following to /etc/asound.conf:
   ```
   pcm.!default {
       type asym
       playback.pcm {
           type plug
           slave.pcm "hw:0,0"
       }
       capture.pcm {
           type plug
           slave.pcm "hw:1,0"  # Adjust this to match your USB mic
       }
   }
   ```

### Environment Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/bird-sound-classification.git
   cd bird-sound-classification
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   
   # Install system dependencies
   sudo apt install -y portaudio19-dev libatlas-base-dev
   ```

### Edge Impulse Model Setup

1. **Create Edge Impulse Account**
   - Visit [Edge Impulse](https://studio.edgeimpulse.com) and sign up for free

2. **Create a New Project**
   - Name: "Bird Sound Classification"
   - Type: Audio project

3. **Data Collection**
   - **Option 1: Use Public Dataset**
     - Go to "Data acquisition" > "Upload existing data"
     - Select "Public datasets" > Search for "Bird Sounds"
     - Find a suitable dataset and import it
   
   - **Option 2: Use Your Own Data**
     - Record bird sounds or download from free sources
     - Split into individual species folders
     - Upload to Edge Impulse using the Data Acquisition tab

4. **Create Impulse**
   - Add "Audio" processing block
     - Frame length: 1000ms
     - Frequency: 16000Hz
   - Add "Classification" learning block
     - Neural Network type

5. **Generate Features**
   - Go to "MFCC" tab
   - Click "Generate features"
   - Verify feature separation in the feature explorer

6. **Train Model**
   - Go to "NN Classifier" tab
   - Select "MobileNetV2 0.1" architecture (optimal for Raspberry Pi 5)
   - Set training cycles to 30
   - Click "Start training"
   - Target accuracy: 85%+ (retrain if needed)

7. **Deploy Model**
   - Go to "Deployment" tab
   - Select "Linux" as target platform
   - Build and download the .zip file

8. **Install Model on Raspberry Pi**
   ```bash
   # In your project directory
   unzip edge-impulse-standalone.zip
   # Verify model file exists
   ls -l edge-impulse-standalone.eim
   ```

## Running the System

1. **Basic Test Run**
   ```bash
   # Activate virtual environment
   source venv/bin/activate
   
   # Run detection script
   python detect_birds.py
   ```

2. **Auto-Start on Boot (Optional)**
   Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/bird-detection.service
   ```
   
   Add the following content:
   ```
   [Unit]
   Description=Bird Sound Classification Service
   After=network.target
   
   [Service]
   User=pi
   WorkingDirectory=/home/pi/bird-sound-classification
   ExecStart=/home/pi/bird-sound-classification/venv/bin/python /home/pi/bird-sound-classification/detect_birds.py
   Restart=on-failure
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start the service:
   ```bash
   sudo systemctl enable bird-detection.service
   sudo systemctl start bird-detection.service
   ```

3. **View Logs**
   ```bash
   # View service logs if running as service
   sudo journalctl -u bird-detection.service
   
   # View detection logs
   cat detection_logs/bird_detections_*.txt
   ```

## Troubleshooting

### Audio Issues

1. **Microphone Not Detected**
   ```bash
   # Check USB devices
   lsusb
   
   # Check audio devices
   arecord -l
   
   # If not showing, try a different USB port or reboot
   sudo reboot
   ```

2. **Audio Quality Problems**
   ```bash
   # Test recording quality
   arecord -D plughw:1,0 -f cd -d 10 test.wav
   aplay test.wav
   
   # Adjust microphone gain if needed
   alsamixer
   ```

### Model Performance

1. **Poor Detection Accuracy**
   - Retrain model with more diverse samples
   - Adjust THRESHOLD value in detect_birds.py
   - Check environmental noise levels

2. **High CPU Usage**
   ```bash
   # Monitor CPU usage
   top
   
   # Adjust sleep time in script if needed
   # Increase time.sleep(0.1) value in detect_birds.py
   ```

3. **Memory Issues**
   ```bash
   # Check memory usage
   free -h
   
   # Consider closing other applications
   ```

## Optimization Tips

1. **Performance Optimization**
   ```bash
   # Disable unnecessary services
   sudo systemctl disable bluetooth.service  # If not using Bluetooth
   sudo systemctl disable cups.service       # If not printing
   
   # Overclock (if using proper cooling)
   sudo nano /boot/config.txt
   # Add: over_voltage=6
   # Add: arm_freq=2200
   ```

2. **Audio Processing**
   - Reduce sampling rate if full quality not needed
   - Adjust the WINDOW_SIZE in detect_birds.py

3. **Power Saving**
   ```bash
   # Disable HDMI if using headless
   /usr/bin/tvservice -o
   
   # Add to /etc/rc.local to disable on boot
   ```

## Updates and Maintenance

1. **Update Software**
   ```bash
   # Update system
   sudo apt update
   sudo apt upgrade -y
   
   # Update Python packages
   source venv/bin/activate
   pip install --upgrade -r requirements.txt
   ```

2. **Update Model**
   - Retrain in Edge Impulse with new data periodically
   - Download and replace the edge-impulse-standalone.eim file

3. **Backup Configuration**
   ```bash
   # Backup logs and configuration
   mkdir -p ~/backups
   cp -r detection_logs ~/backups/
   cp detect_birds.py ~/backups/
   ```
