import pyaudio
import wave

FILENAME = "../data/output_signal.wav"

def signal_playback():
    with wave.open(FILENAME, 'rb') as wf:
        audio = pyaudio.PyAudio()  # Initialize PyAudio object

        SAMPLE_FORMAT = audio.get_format_from_width(wf.getsampwidth()) # Sound depth
        CHANNELS = wf.getnchannels() # Number of channels
        RATE = wf.getframerate() # Sampling rate
        N_FRAMES = wf.getnframes() # The number of frames

        # Selecting a playback device
        print("List of available devices:")
        for i in range(audio.get_device_count()):
            print(f"\t{i} {audio.get_device_info_by_index(i)['name']}")

        output_device = int(input('Select the index of the playback device: '))

        # Opening the stream for recording to the output device - speaker - with the same parameters with which the signal was created
        stream = audio.open(format=SAMPLE_FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            output_device_index=output_device,
                            output=True)

        print(f"Start of signal playback...")
        stream.write(wf.readframes(N_FRAMES)) # Sending a signal to the speaker
        print(f"End of signal playback!\n")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        audio.terminate()  # Audio System Close


if __name__ == "__main__":
    signal_playback()
