import numpy as np
import matplotlib.pyplot as plt

import wave

FILENAME = "../data/output_signal.wav"

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def building_a_wave():
    with wave.open(FILENAME, 'rb') as wf:

        SAMPLE_FORMAT = wf.getsampwidth() # Sound depth
        CHANNELS = wf.getnchannels() # Number of channels
        RATE = wf.getframerate() # Sampling rate
        N_FRAMES = wf.getnframes() # The number of frames

        print(f"\nInfo about input signal...")
        print(f"SAMPLE_FORMAT={SAMPLE_FORMAT}")
        print(f"CHANNELS={CHANNELS}")
        print(f"RATE={RATE}")
        print(f"N_FRAMES={N_FRAMES}")
        print(F"Signal time {N_FRAMES/RATE} sec.\n")

        data_signal = np.frombuffer(wf.readframes(N_FRAMES), dtype=types[SAMPLE_FORMAT]) # Reading the signal from the file and converting bytes to int

        time = np.linspace(0.0, N_FRAMES/RATE, num=N_FRAMES) # Time for the X axis

        # Plotting the input signal
        plt.plot(time, data_signal)
        plt.title('Input signal')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.grid(alpha=0.1)
        plt.savefig("../data/input_signal_graph.png")
        plt.show()


if __name__ == "__main__":
    building_a_wave()
