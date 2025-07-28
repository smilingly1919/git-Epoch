import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
import csv
import sdf_helper as sh

def plot_yz_slice(ne, x, y, z, x_value=None, x_range=None, y_range=None, z_range=None, save=False, output_dir=None):
    """
    绘制 YZ 切片图，支持单一切片或范围内的求和切片，并可指定 y 和 z 的范围。

    参数:
    - ne: 三维数组，电子数密度数据 (x, y, z)
    - x: 一维数组，x 方向的坐标 (单位：μm)
    - y: 一维数组，y 方向的坐标 (单位：μm)
    - z: 一维数组，z 方向的坐标 (单位：μm)
    - x_value: float，指定的 x 值（绘制单一切片）
    - x_range: 元组，x 的范围 (x_min, x_max)（绘制范围内的求和切片）
    - y_range: 元组，y 的范围 (y_min, y_max)，可选
    - z_range: 元组，z 的范围 (z_min, z_max)，可选
    - save: 是否保存图片
    - output_dir: 保存图片的目录路径
    """
    if x_value is not None and x_range is not None:
        raise ValueError("只能指定 x_value 或 x_range 中的一个，不能同时指定。")

    if x_value is not None:
        # 找到最接近 x_value 的索引
        x_idx = np.argmin(np.abs(x - x_value))
        x_actual = x[x_idx]  # 实际的 x 值
        ne_slice = ne[x_idx, :, :]  # 提取该 x 值处的 YZ 切片
        title = f'YZ slice at x = {x_actual:.2f} μm'
    elif x_range is not None:
        # 筛选 x 范围内的数据
        mask_x = (x >= x_range[0]) & (x <= x_range[1])
        ne_sum = np.sum(ne[mask_x, :, :], axis=0)  # 对 x 范围内的数据求和
        ne_slice = ne_sum
        title = f'YZ slice: x in [{x_range[0]}, {x_range[1]}] μm'
    else:
        raise ValueError("必须指定 x_value 或 x_range 中的一个。")

    # 应用 y 和 z 的范围（如果指定）
    if y_range is not None:
        mask_y = (y >= y_range[0]) & (y <= y_range[1])
        y = y[mask_y]
        ne_slice = ne_slice[:, mask_y]
    if z_range is not None:
        mask_z = (z >= z_range[0]) & (z <= z_range[1])
        z = z[mask_z]
        ne_slice = ne_slice[mask_z, :]

    # 生成网格坐标
    Y, Z = np.meshgrid(y, z, indexing='ij')

    # 绘制 YZ 切片图
    plt.figure(figsize=(10, 6))
    c = plt.pcolormesh(Y, Z, ne_slice, shading='auto', cmap="OrRd",rasterized=True)
    plt.colorbar(c, label='$n_e / n_c$')
    plt.title(title + f'\ny range: [{y.min():.2f}, {y.max():.2f}] μm, z range: [{z.min():.2f}, {z.max():.2f}] μm')
    plt.xlabel('y (μm)')
    plt.ylabel('z (μm)')
    plt.grid(True, linestyle='--', alpha=0.7)

    # 保存图片
    if save and output_dir:
        if x_value is not None:
            plt.savefig(os.path.join(output_dir, f"yz_density_at_x_{x_actual:.2f}.jpg"), dpi=300, bbox_inches='tight')
        else:
            plt.savefig(os.path.join(output_dir, f"yz_density_x_{x_range[0]}_{x_range[1]}.jpg"), dpi=300, bbox_inches='tight')
    plt.show()

    return ne_slice