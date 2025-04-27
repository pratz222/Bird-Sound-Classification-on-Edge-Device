import sys
import time
import numpy as np
import sounddevice as sd
from edge_impulse_linux.audio import AudioImpulseRunner

# Settings
MODEL_PATH = './edge-impulse-standalone.eim'
SAMPLE_RATE = 16000
WINDOW_SIZE = int(SAMPLE_RATE * 1.0)  # 1 second window
THRESHOLD = 0.6  # Confidence threshold

# Initialize buffer and runner
audio_buffer = np.zeros(WINDOW_SIZE, dtype=np.float32)
runner = None

def audio_callback(indata, frames, time, status):
    global audio_buffer
    if status:
        print(f'Audio status: {status}')
    # For USB mic (mono)
    audio_buffer = indata[:, 0].astype(np.float32)

def main():
    global runner
    
    # Initialize Edge Impulse model
    try:
        runner = AudioImpulseRunner(MODEL_PATH)
        print('Model loaded successfully')
        print(f'Classes: {", ".join(runner.model_info.model_parameters["labels"])}')
    except Exception as e:
        print(f'ERROR: Failed to initialize runner: {e}')
        sys.exit(1)
    
    # Setup audio stream with USB mic
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        blocksize=WINDOW_SIZE
    )
    
    stream.start()
   
    print("Listening for bird sounds...")
    
    last_detection = 0
    cooldown = 2  # seconds between detections
    
    try:
        while True:
            audio_data = np.copy(audio_buffer)
            
            # Run inference if audio level is above threshold
            if np.mean(np.abs(audio_data)) > 0.01:
                features = runner.get_features_from_audio(audio_data)
                if features is not None:
                    res = runner.classify(features)
                    
                    if res["result"] and res["result"]["classification"]:
                        predictions = res["result"]["classification"]
                        top_class = max(predictions.items(), key=lambda x: x[1])
                        bird, confidence = top_class
                        
                        # Report detection if confidence is high enough
                        current_time = time.time()
                        if confidence > THRESHOLD and (current_time - last_detection) > cooldown:
                            print(f"\n DETECTED: {bird} (Confidence: {confidence:.2f})")
                            last_detection = current_time
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        stream.stop()
        stream.close()
        if runner:
            runner.stop()

if __name__ == "__main__":
    main()
