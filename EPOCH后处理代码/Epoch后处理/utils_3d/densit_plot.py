import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import os

def nd_plot_xy(ne, x, y, z=None, z_pos=None, x_range=None, y_range=None, ax=None):
    """
    绘制二维电子数密度 (x,y) 切片图，支持 x、y 方向范围裁剪，z方向用z_pos定位切片层。

    参数:
    - ne: ndarray，二维或三维电子数密度数据，形状 (Nx, Ny) 或 (Nx, Ny, Nz)
    - x, y: ndarray，一维坐标数组，单位 μm
    - z: ndarray 或 None，一维z坐标数组，单位 μm（可选，三维时用）
    - z_pos: float 或 None，z方向实际坐标，自动寻找最近层切片，默认中间层
    - x_range, y_range: tuple/list 或 None，裁剪范围
    - ax: matplotlib.axes.Axes 对象，传入则绘制在该ax上，否则新建图形
    """

    # 三维数据时，选取z层切片
    if ne.ndim == 3:
        if z is None:
            raise ValueError("三维数据时必须传入z坐标数组z")
        if z_pos is None:
            z_index = ne.shape[2] // 2  # 默认中间层
        else:
            z_index = np.abs(z - z_pos).argmin()
        ne = ne[:, :, z_index]
        z_actual = z[z_index]
    else:
        z_actual = None

    # 裁剪 x 范围
    if x_range is not None and len(x_range) == 2:
        mask_x = (x >= x_range[0]) & (x <= x_range[1])
        x = x[mask_x]
        ne = ne[mask_x, :]
    
    # 裁剪 y 范围
    if y_range is not None and len(y_range) == 2:
        mask_y = (y >= y_range[0]) & (y <= y_range[1])
        y = y[mask_y]
        ne = ne[:, mask_y]

    X, Y = np.meshgrid(x, y, indexing='ij')

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    c = ax.pcolormesh(X, Y, ne, shading='auto', cmap='OrRd', rasterized=True)
    plt.colorbar(c, ax=ax, label='$n_e / n_c$')

    title_z = f", z = {z_actual:.2f} μm" if z_actual is not None else ""
    ax.set_title(f'XY Slice\nx range: [{x.min():.2f}, {x.max():.2f}] μm, y range: [{y.min():.2f}, {y.max():.2f}] μm{title_z}')
    ax.set_xlabel('x (μm)')
    ax.set_ylabel('y (μm)')
    ax.grid(True, linestyle='--', alpha=0.7)

    if ax is None:
        plt.show()

    return ne

def nd_plot_yz(ne, x, y, z, x_value=None, x_range=None, y_range=None, z_range=None, ax=None):
    """
    绘制 YZ 切片图，支持单一切片或范围内的求和切片，并可指定 y 和 z 的范围。

    参数:
    - ne: 三维数组，电子数密度数据 (x, y, z)
    - x, y, z: 一维坐标数组，单位 μm
    - x_value: float，指定的 x 值（绘制单一切片）
    - x_range: tuple，x 的范围 (x_min, x_max)（绘制范围内的求和切片）
    - y_range, z_range: tuple，可选，指定 y, z 范围
    - ax: matplotlib.axes.Axes 对象，可选，传入则绘制在该ax上
    """

    if x_value is not None and x_range is not None:
        raise ValueError("只能指定 x_value 或 x_range 中的一个，不能同时指定。")

    if x_value is not None:
        x_idx = np.abs(x - x_value).argmin()
        x_actual = x[x_idx]
        ne_slice = ne[x_idx, :, :]  # shape (Ny, Nz)
        title = f'YZ slice at x = {x_actual:.2f} μm'
    elif x_range is not None:
        mask_x = (x >= x_range[0]) & (x <= x_range[1])
        if not np.any(mask_x):
            raise ValueError("x_range范围内无数据")
        ne_slice = np.sum(ne[mask_x, :, :], axis=0)  # shape (Ny, Nz)
        title = f'YZ slice: x in [{x_range[0]}, {x_range[1]}] μm'
    else:
        raise ValueError("必须指定 x_value 或 x_range 中的一个。")

    # 裁剪 y 范围
    if y_range is not None:
        mask_y = (y >= y_range[0]) & (y <= y_range[1])
        y = y[mask_y]
        ne_slice = ne_slice[mask_y, :]
    # 裁剪 z 范围
    if z_range is not None:
        mask_z = (z >= z_range[0]) & (z <= z_range[1])
        z = z[mask_z]
        ne_slice = ne_slice[:, mask_z]

    # 生成网格，注意 Y 和 Z 对应数据维度 (len(y), len(z))
    Y, Z = np.meshgrid(y, z, indexing='ij')

    # 创建图形或使用传入ax
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    c = ax.pcolormesh(Y, Z, ne_slice, shading='auto', cmap="OrRd", rasterized=True)
    plt.colorbar(c, ax=ax, label='$n_e / n_c$')
    ax.set_title(title + f'\ny range: [{y.min():.2f}, {y.max():.2f}] μm, z range: [{z.min():.2f}, {z.max():.2f}] μm')
    ax.set_xlabel('y (μm)')
    ax.set_ylabel('z (μm)')
    ax.grid(True, linestyle='--', alpha=0.7)

    if ax is None:
        plt.show()

    return ne_slice

def nd_plot_xsum(ne, x, y, z, x_range=None, y_range=None, z_range=None, ax=None):
    """
    在给定的 x、y 和 z 范围内对电子数密度数据求和，并绘制 x 方向的折线图。

    参数:
    - ne: ndarray，三维电子数密度数据 (x, y, z)
    - x, y, z: ndarray，分别是三个方向的坐标（单位：μm）
    - x_range: tuple/list 或 None，裁剪 x 范围 (x_min, x_max)
    - y_range: tuple/list 或 None，裁剪 y 范围 (y_min, y_max)
    - z_range: tuple/list 或 None，裁剪 z 范围 (z_min, z_max)
    - ax: matplotlib.axes.Axes 对象，传入则绘制在该ax上，否则新建图形
    """

    # 确定 x 范围索引
    if x_range is None:
        x_start, x_end = 0, len(x)
    else:
        x_indices = np.where((x >= x_range[0]) & (x <= x_range[1]))[0]
        if len(x_indices) == 0:
            raise ValueError("指定的 x_range 没有匹配的索引。")
        x_start, x_end = x_indices[0], x_indices[-1] + 1

    # 确定 y 范围索引
    if y_range is None:
        y_start, y_end = 0, len(y)
    else:
        y_indices = np.where((y >= y_range[0]) & (y <= y_range[1]))[0]
        if len(y_indices) == 0:
            raise ValueError("指定的 y_range 没有匹配的索引。")
        y_start, y_end = y_indices[0], y_indices[-1] + 1

    # 确定 z 范围索引
    if z_range is None:
        z_start, z_end = 0, len(z)
    else:
        z_indices = np.where((z >= z_range[0]) & (z <= z_range[1]))[0]
        if len(z_indices) == 0:
            raise ValueError("指定的 z_range 没有匹配的索引。")
        z_start, z_end = z_indices[0], z_indices[-1] + 1

    # 提取指定范围内的数据
    ne_sub = ne[x_start:x_end, y_start:y_end, z_start:z_end]

    # 对 y 和 z 方向求和
    ne_sum = np.sum(ne_sub, axis=(1, 2))

    # 取对应 x 范围的坐标
    x_sub = x[x_start:x_end]

    # 绘图
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x_sub, ne_sum, label='Sum of ne in specified ranges')
    ax.set_xlabel('x (μm)')
    ax.set_ylabel('Sum of ne')

    title_x = f"x range [{x_sub.min():.2f}, {x_sub.max():.2f}] μm"
    title_y = f"y range [{y_range[0]:.2f}, {y_range[1]:.2f}] μm" if y_range is not None else "full y range"
    title_z = f"z range [{z_range[0]:.2f}, {z_range[1]:.2f}] μm" if z_range is not None else "full z range"
    ax.set_title(f'Sum of ne in {title_x}, {title_y} and {title_z}')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    if ax is None:
        plt.show()

    return ne_sum
