#!/usr/bin/env python
"""
Demo of spectrum interpolation on EEG data (binary)

Useage:

This describes the script.
"""
from pathlib import Path

from numpy import ndarray
import numpy as np

from spectrum_interpolation import spectrum_interpolation, plot_freq_domain


if __name__ == '__main__':
    base_path: Path = Path('/Users/yukifujishima/Documents/eeg_example')
    fname: str = 'example_eeg.dat'
    fpath: str = str(base_path / fname)

    epoarray: ndarray = np.fromfile(fpath, dtype='float32')

    n_chn: int = 71
    n_trials: int = 60
    n_points: int = 1280

    # The data used in this example has been saved by Matlab (colum-major).
    epoarray = epoarray.reshape((n_chn, n_points*n_trials), order='F')
    epoarray = epoarray.reshape((n_chn, n_points, n_trials), order='F')
    epoarray = epoarray.swapaxes(1, 2).swapaxes(0, 1)
#   epoarray = epoarray.reshape(n_trials, n_points, n_chn)
#   epoarray = epoarray.swapaxes(1, 2)

    sample_rate: float = 512
    noise_freq: float = 60
    band: float = 1

    new_epo: ndarray = spectrum_interpolation(array=epoarray,
                                              sample_rate=sample_rate,
                                              noise_freq=noise_freq,
                                              band=band)
    print(False in np.isfinite(new_epo))
    fid: str = str(base_path / 'new_epo.dat')

    figname: str = 'before.jpg'
    figpath: str = str(base_path / figname)

    plot_freq_domain(array=epoarray,
                     sample_rate=sample_rate,
                     noise_freq=noise_freq,
                     band=band,
                     suptitle=figname,
                     save_path=figpath)

    figname2: str = 'after.jpg'
    figpath2: str = str(base_path / figname2)

    plot_freq_domain(array=new_epo,
                     sample_rate=sample_rate,
                     noise_freq=noise_freq,
                     band=band,
                     suptitle=figname2,
                     save_path=figpath2)

    # Swap axes to save the file in the column-major wise.
    new_epo2 = new_epo.swapaxes(0, 1).swapaxes(1, 2)
    new_epo2 = new_epo2.reshape((n_chn, n_trials*n_points), order='F')
    new_epo2 = new_epo2.reshape((n_chn*n_trials*n_points), order='F')

    new_epo2.tofile(fid, format='float32')
