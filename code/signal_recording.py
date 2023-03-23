import pyaudio
import wave

SAMPLE_FORMAT = pyaudio.paInt16  # Sound depth = 16 bits = 2 bytes
CHANNELS = 1 # Mono
RATE = 44100 # Sampling rate - number of frames per second
CHUNK = 1024 # The number of frames per one "request" to the microphone (read in pieces)
SECONDS = 5 # Recording duration
FILENAME = "../data/input_signal.wav" # Output file name

def signal_recording():
    audio = pyaudio.PyAudio()  # Initialize PyAudio object

    # Selecting a recording device
    print("List of available devices:")
    for i in range(audio.get_device_count()):
        print(f"\t{i} {audio.get_device_info_by_index(i)['name']}")

    input_device = int(input('Select the index of the recording device: '))

    # Open the stream to read data from the default recording device and set the parameters
    stream = audio.open(format=SAMPLE_FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        frames_per_buffer=CHUNK,
                        input_device_index=input_device,
                        input=True)
    
    frames = [] # Declaring an array for storing frames

    print(f"Recording...")

    for i in range(0, int(RATE / CHUNK * SECONDS)): # RATE / CHUNK - number of requests per second
        data = stream.read(CHUNK) # reading a string of bytes long CHUNK * SAMPLE_FORMAT
        frames.append(data)

    print(f"Finished recording!\n")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    audio.terminate() # Audio System Close

    # Save the recorded data as a WAV file
    with wave.open(FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))


if __name__ == "__main__":
    signal_recording()
