import numpy as np
import matplotlib.pyplot as plt
import os

def ef_plot_xy(x, y, z=None, field_data=None, field_name=None, 
                     x_range=None, y_range=None, z_value=None, ax=None):
    """
    绘制单一电场分量在指定 z 切片的 XY 面热力图。

    参数:
    - x, y: ndarray，一维坐标数组，单位 μm。
    - z: ndarray 或 None，一维z坐标数组，单位 μm（如果 field_data 是三维）。
    - field_data: ndarray，电场分量数据，二维 (Nx, Ny) 或三维 (Nx, Ny, Nz)。
    - field_name: str，电场分量名称（如 'Ex', 'Ey', 'Ez'）。
    - x_range, y_range: tuple，裁剪范围 (min, max)，默认全范围。
    - z_value: float，指定绘制的 z 层坐标，默认中间层。
    - ax: matplotlib.axes.Axes 对象，传入则绘制在此轴，否则新建图。
    """

    if field_data is None:
        raise ValueError("必须传入 field_data 电场分量数据")
    if field_name is None:
        field_name = "Field"

    # 处理三维数据，选取z切片
    if field_data.ndim == 3:
        if z is None:
            raise ValueError("三维数据时必须传入 z 坐标数组")
        if z_value is None:
            z_idx = field_data.shape[2] // 2
        else:
            z_idx = np.abs(z - z_value).argmin()
        field_slice = field_data[:, :, z_idx]
        z_actual = z[z_idx]
    elif field_data.ndim == 2:
        field_slice = field_data
        z_actual = None
    else:
        raise ValueError("field_data 维度应为2或3维")

    # 裁剪 x
    if x_range is not None and len(x_range) == 2:
        mask_x = (x >= x_range[0]) & (x <= x_range[1])
        x = x[mask_x]
        field_slice = field_slice[mask_x, :]

    # 裁剪 y
    if y_range is not None and len(y_range) == 2:
        mask_y = (y >= y_range[0]) & (y <= y_range[1])
        y = y[mask_y]
        field_slice = field_slice[:, mask_y]

    X, Y = np.meshgrid(x, y, indexing='ij')

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    c = ax.pcolormesh(X, Y, field_slice, shading='auto', cmap='RdBu_r', rasterized=True)
    plt.colorbar(c, ax=ax, label=field_name)

    title_z = f", z = {z_actual:.2f} μm" if z_actual is not None else ""
    ax.set_title(f'{field_name} XY Slice\nx range: [{x.min():.2f}, {x.max():.2f}] μm, y range: [{y.min():.2f}, {y.max():.2f}] μm{title_z}')
    ax.set_xlabel('x (μm)')
    ax.set_ylabel('y (μm)')
    ax.grid(True, linestyle='--', alpha=0.7)

    if ax is None:
        plt.show()

    return field_slice


