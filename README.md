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

<details>
  <summary>This project provides a set of tools for working with audio signals. Click to see more information.</summary><br>

  **Recording and Signal Generation**<br>
  To get started, you will need an audio signal, which must be in the `.wav` format and monaural. You can use your own files or use the <a href="./code/signal_recording.py">`signal_recording.py`</a> module for recording signals via a microphone and the <a href="./code/signal_generator.py">`signal_generator.py`</a> module for signal generation using sinusoids.

  **Concatenation of Files**<br>
  If you need to concatenate multiple `.wav` files, you can use the `wave_concatenate` function from the <a href="./code/wave_worker.py">`wave_worker.py`</a> module.

  **Signal Visualization**<br>
  To visualize a signal on a graph, use the function from the <a href="./code/building_a_wave.py">`building_a_wave.py`</a> module.

  **Discrete Fourier Transform**<br>
  For signal analysis, the discrete Fourier transform is used. The project provides three implementations of the discrete Fourier transform:
  * <a href="./code/fourier_transform.py">`fourier_transform.py`</a> - this implementation is based on the forward formula;
  * <a href="./code/fourier_transform_in_parallel.py">`fourier_transform_in_parallel.py`</a> - this implementation uses the same forward formula, but calculations are performed in parallel on 8 cores;
  * <a href="./code/fast_fourier_transform.py">`fast_fourier_transform.py`</a> - this implementation employs the fast discrete Fourier transform algorithm, but here it requires the data size to be a power of two.

  The performance of these modules is distributed as follows: <a href="./code/fourier_transform.py">`fourier_transform.py`</a> < <a href="./code/fourier_transform_in_parallel.py">`fourier_transform_in_parallel.py`</a> < <a href="./code/fast_fourier_transform.py">`fast_fourier_transform.py`</a>. All of these modules have additional functionality that allows you to obtain not only the Fourier transform result but also amplitude and frequency values. These amplitude and frequency values can be passed to the function `building_a_fourier_transform_graph` in the <a href="./code/building_a_fourier_transform_graph.py">`building_a_fourier_transform_graph.py`</a> module for visualization on a graph. To pass data to the graph-building function, set the `need_to_plot` parameter to `True` in the Fourier transform function.

  **Inverse Discrete Fourier Transform**<br>
  Three implementations are also available for the inverse discrete Fourier transform:
  * <a href="./code/inverse_fourier_transform.py">`inverse_fourier_transform.py`</a> - this implementation is based on the forward formula;
  * <a href="./code/inverse_fourier_transform_in_parallel.py">`inverse_fourier_transform_in_parallel.py`</a> - this implementation uses the same forward formula, but calculations are performed in parallel on 8 cores;
  * <a href="./code/inverse_fast_fourier_transform.py">`inverse_fast_fourier_transform.py`</a> - this implementation employs the fast inverse discrete Fourier transform algorithm, but here it requires the data size to be a power of two.

  The performance of these modules is distributed as follows: <a href="./code/inverse_fourier_transform.py">`inverse_fourier_transform.py`</a> < <a href="./code/inverse_fourier_transform_in_parallel.py">`inverse_fourier_transform_in_parallel.py`</a> < <a href="./code/inverse_fast_fourier_transform.py">`inverse_fast_fourier_transform.py`</a>. To reduce the number of calculations, in the direct discrete Fourier transform, calculations were performed only up to the Nyquist frequency. In the inverse discrete Fourier transform, the entire frequency range is required, so you will need to apply the `mirror_image` function to obtain the complete frequency range. To use the `mirror_image` function, set the `mirror_image` parameter to `True` in the inverse discrete Fourier transform function. If the data was obtained from elsewhere and already represents the full frequency range, then you don't need to apply the `mirror_image` function.

  **Saving the Result**<br>
  The result of the inverse discrete Fourier transform will be the result of the inverse discrete transform and the signal data. You can pass the signal data to the `wave_write` function in the <a href="./code/wave_worker.py">`wave_worker.py`</a> module to save this data to a `.wav` file.

  **Signal Playback**<br>
  To play the signal, use the function in the <a href="./code/signal_playback.py">`signal_playback.py`</a> module.
</details>

### <a name="built-with"> Built With </a>

[![Badge Python][Badge_Python]][Python_home]
[![Badge PyAudio][Badge_PyAudio]][PyAudio_home]
[![Badge NumPy][Badge_NumPy]][NumPy_home]
[![Badge Matplotlib][Badge_Matplotlib]][Matplotlib_home]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Getting Started -->
## <a name="getting-started"> Getting Started </a>

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

Several examples with descriptions of what happens are provided in <a href="./code/main.py">main.py</a>. Furthermore descriptions of these examples can be found in <a href="./data/source/help.txt">help.txt</a> or by viewing the help when running <a href="./code/main.py">main.py</a> and passing `-1` as a parameter during program execution. All modules and functions have documentation, so you can refer to them for additional information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- License -->
## <a name="license"> License </a>

Distributed under the BSD 3-Clause "New" or "Revised" License. See [LICENSE](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Markdown links -->
[Python_home]: https://www.python.org
[PyAudio_home]: https://pypi.org/project/PyAudio/
[NumPy_home]: https://numpy.org
[Matplotlib_home]: https://matplotlib.org

[documentation-pyaudio]: https://people.csail.mit.edu/hubert/pyaudio/docs/
[documentation-numpy]: https://numpy.org/doc/
[documentation-matplotlib]: https://matplotlib.org/stable/users/index.html
[documentation-multiprocessing]: https://docs.python.org/3.10/library/multiprocessing.html
[documentation-wave]: https://docs.python.org/3.10/library/wave.html
[documentation-cmath]: https://docs.python.org/3.10/library/cmath.html
[documentation-math]: https://docs.python.org/3.10/library/math.html
[documentation-time]: https://docs.python.org/3.10/library/time.html

[Badge_Python]: https://img.shields.io/badge/3.10-ffffff?logo=python&logoColor=FFFFFF&label=Python&labelColor=000000
[Badge_PyAudio]: https://img.shields.io/badge/PyAudio-000000
[Badge_NumPy]: https://img.shields.io/badge/NumPy-000000?logo=numpy
[Badge_Matplotlib]: https://img.shields.io/badge/Matplotlib-000000