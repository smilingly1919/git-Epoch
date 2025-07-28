import numpy as np
import sdf_helper as sh
import pandas as pd

def calc_angmom_x(
    py, pz, x, y, z, weight=1.0,
    x_range=None, y_range=None, z_range=None,):
    """
    计算绕 x 轴的加权角动量总和和均值：Lx = y*pz - z*py。
    可按位置范围筛选粒子。

    参数:
    - py, pz, x, y, z: 一维 ndarray，动量和位置数据
    - weight: 标量或数组，权重，默认 1.0
    - x_range, y_range, z_range: tuple(min, max) 或 None，筛选粒子位置范围

    返回:
    - total_Lx: float，加权角动量总和
    - mean_Lx: float，加权角动量均值
    """

    # 建立筛选掩码
    mask = np.ones_like(x, dtype=bool)
    if x_range is not None:
        mask &= (x >= x_range[0]) & (x <= x_range[1])
    if y_range is not None:
        mask &= (y >= y_range[0]) & (y <= y_range[1])
    if z_range is not None:
        mask &= (z >= z_range[0]) & (z <= z_range[1])

    # 筛选数据
    py_sel = py[mask]
    pz_sel = pz[mask]
    x_sel = x[mask]
    y_sel = y[mask]
    z_sel = z[mask]

    # 更鲁棒的权重处理
    if isinstance(weight, (int, float)):
        weight_sel = weight
        total_weight = weight * len(py_sel)
    else:
        weight = np.asarray(weight)
        weight_sel = weight[mask]
        total_weight = weight_sel.sum()

    # 计算加权角动量
    Lx = (y_sel * pz_sel - z_sel * py_sel) * weight_sel

    total_Lx = Lx.sum()
    mean_Lx = total_Lx / total_weight if total_weight != 0 else 0.0
    max_Lx = Lx.max()
    min_Lx = Lx.min()

    # 打印筛选后的位置范围和角动量
    print(f"x范围: [{x_sel.min()}, {x_sel.max()}]")
    print(f"y范围: [{y_sel.min()}, {y_sel.max()}]")
    print(f"z范围: [{z_sel.min()}, {z_sel.max()}]")
    print(f"加权角动量总和 Lx = {total_Lx}")
    print(f"加权角动量均值 mean_Lx = {mean_Lx}")
    print(f"加权角动量最小值 min_Lx = {min_Lx}")
    print(f"加权角动量最大值 max_Lx = {max_Lx}")

    return total_Lx, mean_Lx, min_Lx, max_Lx
