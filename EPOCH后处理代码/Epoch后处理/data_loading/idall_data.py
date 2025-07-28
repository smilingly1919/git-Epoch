import numpy as np
import sdf_helper as sh
import pandas as pd

def load_ppos(file_path, species):
    """
    加载指定粒子的空间位置 (x, y, z)。

    参数:
    - file_path: str，SDF 文件路径
    - species: str，粒子类型，如 'Photon' 或 'Electron'

    返回:
    - x, y, z: ndarray，单位为微米 (um)
    """
    data = sh.getdata(file_path)
    
    if species == "Photon":
        key = "Grid_Particles_subset_testp_Photon"
    elif species == "Electron":
        key = "Grid_Particles_subset_teste_Electron"
    else:
        raise ValueError(f"不支持的粒子类型: {species}")

    grid = getattr(data, key).data
    x, y, z = grid[0] / 1e-6, grid[1] / 1e-6, grid[2] / 1e-6  # 转换为微米
    return x, y, z

def load_pm(file_path, species='Photon'):
    """
    加载指定粒子的动量 (px, py, pz)。

    参数:
    - file_path: str，SDF 文件路径
    - species: str，粒子类型，如 'Photon' 或 'Electron'

    返回:
    - px, py, pz: ndarray
    """
    data = sh.getdata(file_path)

    # 根据粒子种类确定前缀
    if species == 'Photon':
        prefix = 'subset_testp'
    elif species == 'Electron':
        prefix = 'subset_teste'
    else:
        raise ValueError(f"不支持的粒子类型: {species}")

    px = getattr(data, f"Particles_Px_{prefix}_{species}").data
    py = getattr(data, f"Particles_Py_{prefix}_{species}").data
    pz = getattr(data, f"Particles_Pz_{prefix}_{species}").data
    return px, py, pz








