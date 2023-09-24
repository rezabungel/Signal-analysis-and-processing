'''
This module is used to playback the signal.
Signal from a file with the extension ".wav" is played from your speakers.
'''

import wave

import pyaudio

def signal_playback(FILENAME = "../data/output_signal.wav"): # FILENAME must contain the path and file name of the playback. FILENAME must end in ".wav"

    '''
    This function allows you to playback the signal using the speakers.
    The following parameters are passed to the function:
        FILENAME ("str") - the path where the file is stored and its name with the extension ".wav". (example: "../the_path_where_the_file_is_stored/file_name.wav").
    The result of the function will be a signal playback from the speakers.
    '''

    # Checking for the correctness of the input data
    if type(FILENAME) != str or '.wav' not in FILENAME:
        FILENAME = "../data/output_signal.wav"
        print(f'The filename for playback is set incorrectly. The default value is set:\n\t FILENAME = "{FILENAME}"')
    else:
        FILENAME = "./" + FILENAME

    with wave.open(FILENAME, 'rb') as wf:
        audio = pyaudio.PyAudio() # Initialize PyAudio object

        SAMPLE_FORMAT = audio.get_format_from_width(wf.getsampwidth()) # Sound depth
        CHANNELS = wf.getnchannels() # Number of channels
        RATE = wf.getframerate() # Sampling rate
        N_FRAMES = wf.getnframes() # The number of frames

        while True: # The loop runs until the correct data is entered
            try:
                # Selecting a playback device
                print(f"List of available devices:")
                for i in range(audio.get_device_count()):
                    print(f"\t{i} {audio.get_device_info_by_index(i)['name']}")

                while True:
                    output_device = int(input('Select the index of the playback device: '))
                    if (output_device >= 0) and (output_device <= i):
                        break
                    else:
                        print(f"Invalid input. Non-existent index.")
                        print(f"List of available devices:")
                        for i in range(audio.get_device_count()):
                            print(f"\t{i} {audio.get_device_info_by_index(i)['name']}")

                # Opening the stream for recording to the output device - speaker - with the same parameters with which the signal was created
                stream = audio.open(format=SAMPLE_FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    output_device_index=output_device,
                                    output=True)
                break
            
            except ValueError:
                print(f"Invalid input. You didn't enter a number.")
            except OSError:
                print(f"Invalid playback device.")

        print(f"Start of signal playback...")
        stream.write(wf.readframes(N_FRAMES)) # Sending a signal to the speaker
        print(f"End of signal playback!\n")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        audio.terminate() # Audio System Close

if __name__ == "__main__":
    signal_playback()
