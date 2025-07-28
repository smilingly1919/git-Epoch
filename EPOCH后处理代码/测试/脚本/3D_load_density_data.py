import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
import csv
import sdf_helper as sh

def load_density_data(file_path, den_crit=0.17419597124e28):
    data = sh.getdata(file_path)
    ne = data.Derived_Number_Density_Photon.data / den_crit
    x = data.Grid_Grid_mid.data[0] / 1e-6
    y = data.Grid_Grid_mid.data[1] / 1e-6
    z = data.Grid_Grid_mid.data[2] / 1e-6
    return ne, x, y, z