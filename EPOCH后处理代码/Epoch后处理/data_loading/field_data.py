import numpy as np
import sdf_helper as sh

def load_efields(file_path):
    """
    加载指定粒子的归一化数密度数据（单位：ne / nc）

    参数:
    - file_path: str，SDF 文件路径
    - species: str，粒子种类，如 'Photon'、'Electron'

    返回:
    - ne: ndarray，归一化密度数据
    """
    data = sh.getdata(file_path)
    ex = getattr(data, f"Electric_Field_Ex").data 
    ey = getattr(data, f"Electric_Field_Ey").data 
    ez = getattr(data, f"Electric_Field_Ez").data 
    return ex,ey,ez

def load_bfields(file_path):
    """
    加载指定粒子的归一化数密度数据（单位：ne / nc）

    参数:
    - file_path: str，SDF 文件路径
    - species: str，粒子种类，如 'Photon'、'Electron'

    返回:
    - ne: ndarray，归一化密度数据
    """
    data = sh.getdata(file_path)
    bx = getattr(data, f"Magnetic_Field_Bx").data 
    by = getattr(data, f"Magnetic_Field_By").data 
    bz = getattr(data, f"Magnetic_Field_Bz").data 
    return bx,by,bz