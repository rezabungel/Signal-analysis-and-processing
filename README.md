# Signal-analysis-and-processing

<a name="readme-top"></a>

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#libraries">Libraries</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- About The Project -->
## <a name="about-the-project"> About The Project </a>

This project provides a set of tools for working with audio signals.<br>

**Recording and Signal Generation**<br>
The project begins with obtaining an audio signal, which must be in the ".wav" format and monaural. You can use your own files or use the "signal_recording.py" module for recording signals via a microphone and the "signal_generator.py" module for signal generation using sinusoids.

**Concatenation of Files**<br>
If you need to concatenate multiple ".wav" files, you can use the "wave_concatenate" function from the "wave_worker.py" module.

**Signal Visualization**<br>
To visualize a signal on a graph, use the function from the "building_a_wave.py" module.

**Discrete Fourier Transform**<br>
For signal analysis, the discrete Fourier transform is used. The project provides three implementations of the discrete Fourier transform:
* "fourier_transform.py" - this is a direct calculation implementation using the formula;
* "fourier_transform_in_parallel.py" - here, the same direct formula is used, but calculations are parallelized on 8 cores, providing faster results;
* "fast_fourier_transform.py" - this is a fast calculation algorithm, which gives the fastest results but requires the data size to be a power of two.

All these modules have additional functionality that allows you to obtain not only the Fourier transform result but also the amplitude and frequency values, which can be passed to the "building_a_fourier_transform_graph" function in the "building_a_fourier_transform_graph.py" module for visualization. To pass data to the graph-building function, set the "need_to_plot" parameter to True in the Fourier transform function.

**Inverse Discrete Fourier Transform**<br>
Three implementations are also available for the inverse discrete Fourier transform:
* Direct formula in "inverse_fourier_transform.py";
* Parallelized version of the direct formula on 8 cores in "inverse_fourier_transform_in_parallel.py";
* Fast implementation in "inverse_fast_fourier_transform.py" (requires data size to be a power of two).

To reduce the number of calculations, in the direct direct discrete Fourier transform, calculations were performed only up to the Nyquist frequency. In the inverse discrete Fourier transform, the entire range is required, so you will need to apply the "mirror_image" function. To use the "mirror_image" function, set the "mirror_image" parameter to True in the inverse discrete Fourier transform function. If the data was obtained from elsewhere and already represents the full frequency range, then you don't need to apply the "mirror_image" function.

**Saving the Result**<br>
The result of the inverse discrete Fourier transform will be the result of the inverse discrete transform and the signal data. You can pass the signal data to the "wave_write" function in the "wave_worker.py" module to save this data to a ".wav" file.

**Signal Playback**<br>
To play the signal, use the function in the "signal_playback.py" module.

### <a name="built-with"> Built With </a>

In progress...

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Getting Started -->
## <a name="getting-started"> Getting Started </a>

In progress...

### <a name="installation"> Installation </a>

1. Clone the repository.
```sh
git clone https://github.com/rezabungel/Signal-analysis-and-processing.git
```
2. Be in the project's root directory.
3. Create a virtual environment.
```sh
python3.10 -m venv venv
```
4. Activate the created virtual environment.

For Linux/Mac
```sh
source venv/bin/activate
```
For Windows 
```sh
venv\Scripts\activate
```
5. Install the required libraries and dependencies.
```sh
python3.10 -m pip install -r requirements.txt
```

### <a name="libraries"> Libraries </a>

Required libraries
|   Library name  |        How to download manually        |                            Documentation                            |
| --------------- | -------------------------------------- | ------------------------------------------------------------------- |
| PyAudio         | `python3.10 -m pip install pyaudio`    | [PyAudio documentation][documentation-pyaudio]                      |
| NumPy           | `python3.10 -m pip install numpy`      | [NumPy documentation][documentation-numpy]                          |
| Matplotlib      | `python3.10 -m pip install matplotlib` | [Matplotlib documentation][documentation-matplotlib]                |
| Multiprocessing | installed by default                   | [Multiprocessing documentation][documentation-multiprocessing]      |
| Wave            | installed by default                   | [Wave documentation][documentation-wave]                            |
| CMath           | installed by default                   | [CMath documentation][documentation-cmath]                          |
| Math            | installed by default                   | [Math documentation][documentation-math]                            |
| Time            | installed by default                   | [Time documentation][documentation-time]                            |

But it would be best to use a virtual environment as demonstrated in the [Installation](#installation) section, rather than installing all the libraries manually.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Usage -->
## <a name="usage"> Usage </a>

In progress...

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- License -->
## <a name="license"> License </a>

Distributed under the BSD 3-Clause "New" or "Revised" License. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Markdown links -->
[documentation-pyaudio]: https://people.csail.mit.edu/hubert/pyaudio/docs/
[documentation-numpy]: https://numpy.org/doc/
[documentation-matplotlib]: https://matplotlib.org/stable/users/index.html
[documentation-multiprocessing]: https://docs.python.org/3.10/library/multiprocessing.html
[documentation-wave]: https://docs.python.org/3.10/library/wave.html
[documentation-cmath]: https://docs.python.org/3.10/library/cmath.html
[documentation-math]: https://docs.python.org/3.10/library/math.html
[documentation-time]: https://docs.python.org/3.10/library/time.html