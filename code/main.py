import signal_recording
import signal_playback
import building_a_wave
import creating_a_signal
import fourier_transform # Does not require data of degree two
import fourier_transform_in_parallel # Does not require data of degree two
import fast_fourier_transform # Requires data of degree two
import inverse_fourier_transform # Does not require data of degree two
import inverse_fourier_transform_in_parallel # Does not require data of degree two
import inverse_fast_fourier_transform # Requires data of degree two

import matplotlib.pyplot as plt
import multiprocessing

def main():

    # example 1
    # In this example, the direct and inverse discrete Fourier transform algorithms are used directly based on the forward formula.

    filename_input = "../data/input_signal.wav"
    filename_output = "../data/output_signal.wav"
    rate_low = 4000

    signal_recording.signal_recording(FILENAME=filename_input, SECONDS=5.0, RATE=rate_low, CHUNK=1024, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_input)

    FT, amplitude, frequency = fourier_transform.fourier_transform(path_to_signal=filename_input, need_to_plot=True)

    iFT, data_signal = inverse_fourier_transform.inverse_fourier_transform(FT=FT, mirror_image=True)

    creating_a_signal.creating_a_signal(data_signal=data_signal, FILENAME=filename_output, RATE=rate_low, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_output)
    signal_playback.signal_playback(FILENAME=filename_output)

    # note: A signal was recorded, its graph was plotted, the direct discrete Fourier transform
            # was applied with a graph of the result, then the inverse discrete Fourier transform
            # was applied, the signal was reconstructed from the obtained data, its graph was
            # plotted, and finally, it was reproduced through the speakers.
    # note: The graphs of the "input" and "output" signals will coincide.

    # example 2
    # In this example, the direct and inverse discrete Fourier transform algorithms are used directly based on the forward formula with computation parallelized across 8 cores.

    filename_input = "../data/input_signal2.wav"
    filename_output = "../data/output_signal2.wav"
    rate_mid = 9000

    signal_recording.signal_recording(FILENAME=filename_input, SECONDS=5.0, RATE=rate_mid, CHUNK=1024, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_input)

    FT, amplitude, frequency = fourier_transform_in_parallel.fourier_transform_in_parallel(path_to_signal=filename_input, need_to_plot=True)

    iFT, data_signal = inverse_fourier_transform_in_parallel.inverse_fourier_transform_in_parallel(FT=FT, mirror_image=True)

    creating_a_signal.creating_a_signal(data_signal=data_signal, FILENAME=filename_output, RATE=rate_mid, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_output)
    signal_playback.signal_playback(FILENAME=filename_output)

    # note: A signal was recorded, its graph was plotted, the direct discrete Fourier transform
            # was applied with a graph of the result, then the inverse discrete Fourier transform
            # was applied, the signal was reconstructed from the obtained data, its graph was
            # plotted, and finally, it was reproduced through the speakers.
    # note: The graphs of the "input" and "output" signals will coincide.

    # example 3
    # In this example, the fast direct and inverse discrete Fourier transform algorithms are used.
    # note: It may be necessary to match the parameters of the recording to use the FFT and IFFT algorithms.
            # The matching is done by adjusting the duration of the recording. The function "signal_recording" will suggest doing this if necessary.

    filename_input = "../data/input_signal3.wav"
    filename_output = "../data/output_signal3.wav"
    rate_high = 44100

    signal_recording.signal_recording(FILENAME=filename_input, SECONDS=10, RATE=rate_high, CHUNK=1024, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_input)

    FT, amplitude, frequency = fast_fourier_transform.fast_fourier_transform(path_to_signal=filename_input, need_to_plot=True)

    iFT, data_signal = inverse_fast_fourier_transform.inverse_fast_fourier_transform(FT=FT, mirror_image=True)

    creating_a_signal.creating_a_signal(data_signal=data_signal, FILENAME=filename_output, RATE=rate_high, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_output)
    signal_playback.signal_playback(FILENAME=filename_output)

    # note: A signal was recorded, its graph was plotted, the direct discrete Fourier transform
            # was applied with a graph of the result, then the inverse discrete Fourier transform
            # was applied, the signal was reconstructed from the obtained data, its graph was
            # plotted, and finally, it was reproduced through the speakers.
    # note: The graphs of the "input" and "output" signals will coincide.

    # example 4
    # In this example, the fast direct and inverse discrete Fourier transform algorithms are used for a signal with a frequency of 440 Hz.
    # note: It assumes the existence of a file with a frequency of 440 Hz, and the volume of its data allows for the application of fast algorithms.
            # One of such files exists in the "examples" folder located within the "data" directory.

    filename_input = "../data/examples/signal_440hz_duration_11s-89ms.wav"
    filename_output = "../data/reconstructed_signal_440hz_duration_11s-89ms.wav"
    rate = 11025

    print(f"A signal with a frequency of 440 Hz and a duration of 11 seconds 89 milliseconds will be played.")
    signal_playback.signal_playback(FILENAME=filename_input)
    building_a_wave.building_a_wave(path_to_signal=filename_input)

    FT, amplitude, frequency = fast_fourier_transform.fast_fourier_transform(path_to_signal=filename_input, need_to_plot=True)

    iFT, data_signal = inverse_fast_fourier_transform.inverse_fast_fourier_transform(FT=FT, mirror_image=True)

    creating_a_signal.creating_a_signal(data_signal=data_signal, FILENAME=filename_output, RATE=rate, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_output)
    print(f"The reconstructed signal with a frequency of 440 Hz and a duration of 11 seconds 89 milliseconds will be played.")
    signal_playback.signal_playback(FILENAME=filename_output) 

    # note: A signal of 440 Hz with a duration of 11 seconds 89 milliseconds was played, its graph
            # was plotted, the direct discrete Fourier transform was applied with a graph of the
            # result, then the inverse discrete Fourier transform was applied, the signal was
            # reconstructed from the obtained data, its graph was plotted, and finally, it was
            # reproduced through the speakers.
    # note: The graphs of the "input" and "output" signals will coincide.

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Enable support for multiprocessing
    plt.ion()  # Enables interactive mode (The program continues to work after the graph is displayed)
    main()
    input("End of program, press enter...\t")
