import numpy as np
import sdf_helper as sh

def load_xyz_grid(file_path):
    """
    从 SDF 文件中提取坐标轴 x, y, z（单位：μm）

    参数:
    - file_path: str，SDF 文件路径

    返回:
    - x, y: ndarray，单位：μm（二维数据）或
    - x, y, z: ndarray，单位：μm（三维数据）
    """
    data = sh.getdata(file_path)
    
    # 获取坐标数据
    x = data.Grid_Grid_mid.data[0] / 1e-6
    y = data.Grid_Grid_mid.data[1] / 1e-6

    # 检查是否有 z 轴数据
    if len(data.Grid_Grid_mid.data) == 3:  # 如果有三个数组，认为是三维数据
        z = data.Grid_Grid_mid.data[2] / 1e-6
        return x, y, z
    else:
        # 如果是二维数据，不返回 z
        return x, y

def load_ne(file_path, species='Photon'):
    """
    加载指定粒子的归一化数密度数据（单位：ne / nc）

    参数:
    - file_path: str，SDF 文件路径
    - species: str，粒子种类，如 'Photon'、'Electron'

    返回:
    - ne: ndarray，归一化密度数据
    """
    valid_species = ['Photon', 'Electron']
    if species not in valid_species:
        raise ValueError(f"不支持的粒子类型：{species}，可选值为 {valid_species}")

    data = sh.getdata(file_path)
    nc = 0.17419597124e28  # 临界密度，单位 m⁻³（对应 1 μm 波长）

    ne = getattr(data, f"Derived_Number_Density_{species}").data / nc
    return ne

def load_ek(file_path, species='Photon'):
    """
    加载指定粒子的归一化数密度数据（单位：ne / nc）

    参数:
    - file_path: str，SDF 文件路径
    - species: str，粒子种类，如 'Photon'、'Electron'

    返回:
    - ne: ndarray，归一化密度数据
    """
    valid_species = ['Photon', 'Electron']
    if species not in valid_species:
        raise ValueError(f"不支持的粒子类型：{species}，可选值为 {valid_species}")

    data = sh.getdata(file_path)

    ek = getattr(data, f"Derived_Average_Particle_Energy_{species}").data
    return ek

