import multiprocessing

import matplotlib.pyplot as plt

import signal_recording
import signal_playback
import signal_generator
import building_a_wave
import fourier_transform # Does not require data of degree two
import fourier_transform_in_parallel # Does not require data of degree two
import fast_fourier_transform # Requires data of degree two
import inverse_fourier_transform # Does not require data of degree two
import inverse_fourier_transform_in_parallel # Does not require data of degree two
import inverse_fast_fourier_transform # Requires data of degree two
import wave_worker

def example1():

    '''
    Example 1: The direct and inverse discrete Fourier transform algorithms are used directly based on the forward formula.
    note: A signal will be recorded from a microphone, its graph will be plotted,
	    the direct discrete Fourier transform will be applied with a graph of the result,
	    then the inverse discrete Fourier transform will be applied,
	    the signal will be reconstructed from the obtained data,
	    its graph will be plotted, and finally, it will be reproduced through the speakers.
    note: The graphs of the "input" and "output" signals will coincide.
    '''

    filename_input = "../data/input_signal.wav"
    filename_output = "../data/output_signal.wav"
    rate_low = 4000

    signal_recording.signal_recording(FILENAME=filename_input, SECONDS=3.0, RATE=rate_low, CHUNK=1024, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_input)

    FT, amplitude, frequency = fourier_transform.fourier_transform(path_to_signal=filename_input, need_to_plot=True)

    iFT, data_signal = inverse_fourier_transform.inverse_fourier_transform(FT=FT, mirror_image=True)

    print(f"Signal creation has started.")
    wave_worker.wave_write(FILENAME=filename_output, FRAMES=data_signal, RATE=rate_low, CHANNELS=1)
    print(f'Finished signal creation. The signal is saved in the "{filename_output}" file!\n')
    building_a_wave.building_a_wave(path_to_signal=filename_output)
    signal_playback.signal_playback(FILENAME=filename_output)

def example2():

    '''
    Example 2: The direct and inverse discrete Fourier transform algorithms are used directly based on the forward formula with computation parallelized across 8 cores.
    note: A signal will be recorded from a microphone, its graph will be plotted,
	    the direct discrete Fourier transform (computation parallelized across 8 cores) will be applied with a graph of the result,
	    then the inverse discrete Fourier transform (computation parallelized across 8 cores) will be applied,
	    the signal will be reconstructed from the obtained data,
	    its graph will be plotted, and finally, it will be reproduced through the speakers.
    note: The graphs of the "input" and "output" signals will coincide.
    '''

    filename_input = "../data/input_signal2.wav"
    filename_output = "../data/output_signal2.wav"
    rate_mid = 9000

    signal_recording.signal_recording(FILENAME=filename_input, SECONDS=3.0, RATE=rate_mid, CHUNK=1024, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_input)

    FT, amplitude, frequency = fourier_transform_in_parallel.fourier_transform_in_parallel(path_to_signal=filename_input, need_to_plot=True)

    iFT, data_signal = inverse_fourier_transform_in_parallel.inverse_fourier_transform_in_parallel(FT=FT, mirror_image=True)

    print(f"Signal creation has started.")
    wave_worker.wave_write(FILENAME=filename_output, FRAMES=data_signal, RATE=rate_mid, CHANNELS=1)
    print(f'Finished signal creation. The signal is saved in the "{filename_output}" file!\n')
    building_a_wave.building_a_wave(path_to_signal=filename_output)
    signal_playback.signal_playback(FILENAME=filename_output)

def example3():

    '''
    Example 3: The fast direct and fast inverse discrete Fourier transform algorithms are used.
    note: It may be necessary to match the parameters of the recording to use the FFT and IFFT algorithms.
	    The matching will be done by adjusting the duration of the recording. The function "signal_recording" will suggest doing this if necessary.
    note: A signal will be recorded from a microphone, its graph will be plotted,
	    the fast direct discrete Fourier transform will be applied with a graph of the result,
	    then the inverse fast discrete Fourier transform will be applied,
	    the signal will be reconstructed from the obtained data,
	    its graph will be plotted, and finally, it will be reproduced through the speakers.
    note: The graphs of the "input" and "output" signals will coincide.
    '''

    filename_input = "../data/input_signal3.wav"
    filename_output = "../data/output_signal3.wav"
    rate_high = 44100

    signal_recording.signal_recording(FILENAME=filename_input, SECONDS=10, RATE=rate_high, CHUNK=1024, CHANNELS=1)
    building_a_wave.building_a_wave(path_to_signal=filename_input)

    FT, amplitude, frequency = fast_fourier_transform.fast_fourier_transform(path_to_signal=filename_input, need_to_plot=True)

    iFT, data_signal = inverse_fast_fourier_transform.inverse_fast_fourier_transform(FT=FT, mirror_image=True)

    print(f"Signal creation has started.")    
    wave_worker.wave_write(FILENAME=filename_output, FRAMES=data_signal, RATE=rate_high, CHANNELS=1)
    print(f'Finished signal creation. The signal is saved in the "{filename_output}" file!\n')
    building_a_wave.building_a_wave(path_to_signal=filename_output)
    signal_playback.signal_playback(FILENAME=filename_output)

def example4():

    '''
    Example 4: The fast direct and fast inverse discrete Fourier transform algorithms are used for a signal with a frequency of 440 Hz.
    note: It assumes the existence of a file with a frequency of 440 Hz, and the volume of its data allows for the application of fast algorithms.
    	One of such files exists in the "examples" folder located within the "data" directory.
    note: A signal of 440 Hz with a duration of 11 seconds and 89 milliseconds will be played, its graph will be plotted,
    	the fast direct discrete Fourier transform will be applied with a graph of the result,
    	then the inverse fast discrete Fourier transform will be applied,
    	the signal will be reconstructed from the obtained data,
    	its graph will be plotted, and finally, it will be reproduced through the speakers.
    note: The graphs of the "input" and "output" signals will coincide.
    '''

    filename_input = "../data/examples/signal_440hz_duration_11s-89ms.wav"
    filename_output = "../data/reconstructed_signal_440hz_duration_11s-89ms.wav"
    rate = 11025

    print(f"A signal with a frequency of 440 Hz and a duration of 11 seconds 89 milliseconds will be played.")
    signal_playback.signal_playback(FILENAME=filename_input)
    building_a_wave.building_a_wave(path_to_signal=filename_input)

    FT, amplitude, frequency = fast_fourier_transform.fast_fourier_transform(path_to_signal=filename_input, need_to_plot=True)

    iFT, data_signal = inverse_fast_fourier_transform.inverse_fast_fourier_transform(FT=FT, mirror_image=True)

    print(f"Signal creation has started.")
    wave_worker.wave_write(FILENAME=filename_output, FRAMES=data_signal, RATE=rate, CHANNELS=1)
    print(f'Finished signal creation. The signal is saved in the "{filename_output}" file!\n')
    building_a_wave.building_a_wave(path_to_signal=filename_output)
    print(f"The reconstructed signal with a frequency of 440 Hz and a duration of 11 seconds 89 milliseconds will be played.")
    signal_playback.signal_playback(FILENAME=filename_output) 

def example5():

    '''
    Example 5: The fast direct and fast inverse Fourier transform algorithms are used for the generated signal (sum of sinusoids with specified frequencies).
    note: It may be necessary to match the parameters of the recording to use the FFT and IFFT algorithms.
	    The matching will be done by adjusting the duration of the recording. The function "signal_generator" will suggest doing this if necessary.
    note: The signal will be generated from the sum of sinusoids with specified frequencies, its graph will be plotted,
	    the fast direct discrete Fourier transform will be applied with a graph of the result,
	    then the inverse fast discrete Fourier transform will be applied,
	    the signal will be reconstructed from the obtained data,
	    its graph will be plotted, and finally, it will be reproduced through the speakers.
    note: The graphs of the "input" and "output" signals will coincide.
    '''

    filename_input = "../data/input_generated_signal5.wav"
    filename_output = "../data/output_generated_signal5.wav"
    rate_high = 44100
    frequencies = [200, 350, 400, 550, 700, 850, 1000]

    signal_generator.signal_generator_sum(FILENAME=filename_input, SECONDS=3, RATE=rate_high, FREQUENCIES=frequencies)
    building_a_wave.building_a_wave(path_to_signal=filename_input)

    FT, amplitude, frequency = fast_fourier_transform.fast_fourier_transform(path_to_signal=filename_input, need_to_plot=True)

    iFT, data_signal = inverse_fast_fourier_transform.inverse_fast_fourier_transform(FT=FT, mirror_image=True)

    print(f"Signal creation has started.")
    wave_worker.wave_write(FILENAME=filename_output, FRAMES=data_signal, RATE=rate_high, CHANNELS=1)
    print(f'Finished signal creation. The signal is saved in the "{filename_output}" file!\n')
    building_a_wave.building_a_wave(path_to_signal=filename_output)
    signal_playback.signal_playback(FILENAME=filename_output)

def choose_example():
    print(f"\n\n\n********************************************************************************")
    print(f"Choose the example you want to use:")
    print(f"\t1 -> Example 1: The direct and inverse discrete Fourier transform algorithms are used directly based on the forward formula.")
    print(f"\t2 -> Example 2: The direct and inverse discrete Fourier transform algorithms are used directly based on the forward formula with computation parallelized across 8 cores.")
    print(f"\t3 -> Example 3: The fast direct and fast inverse discrete Fourier transform algorithms are used.")
    print(f"\t4 -> Example 4: The fast direct and fast inverse discrete Fourier transform algorithms are used for a signal with a frequency of 440 Hz.")
    print(f"\t5 -> Example 5: The fast direct and fast inverse Fourier transform algorithms are used for the generated signal (sum of sinusoids with specified frequencies).")
    print(f"\t0 -> All examples.")
    print(f"\t-1 -> Help.")
    print(f"\t-10 -> Exit.")

    while True:
        try:
            while True:
                answer = int(input("Your choice?\t"))
                if answer >= -1 and answer <= 5 or answer == -10:
                    print(f"********************************************************************************\n\n\n")
                    break
                else:
                    print(f"Invalid input. Non-existent answer.")
            break
        except ValueError:
            print(f"Invalid input. You didn't enter a number.")

    return answer

def help():
    try:
        with open('../data/source/help.txt', 'r', encoding='utf-8') as f:
            print(*f)
    except FileNotFoundError:
        print(f'The file "help.txt", which contains information about the examples, was not found in "/data/source/".')

def main():
    print(f"Signal analysis and processing.")

    while True:
        answer = choose_example()

        if answer == 1 or answer == 0:
            example1()

        if answer == 2 or answer == 0:
            example2()

        if answer == 3 or answer == 0:
            example3()

        if answer == 4 or answer == 0:
            example4()

        if answer == 5 or answer == 0:
            example5()

        if answer == -1:
            help()

        if answer == -10:
            break

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Enable support for multiprocessing
    plt.ion()  # Enables interactive mode (The program continues to work after the graph is displayed)
    main()
    input("Have a great day! Press enter...\t")
