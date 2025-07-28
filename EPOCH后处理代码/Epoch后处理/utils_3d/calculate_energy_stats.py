import numpy as np
import sdf_helper as sh

def ek_stats(
    ek, x, y, z=None,
    x_range=None, y_range=None, z_range=None
):
    """
    在指定的 x, y, z 范围内，计算能量数据（ek）的方差与平均值。

    参数:
    - ek: ndarray，二维或三维平均能量数组（单位：J）
    - x, y: ndarray，x、y 的坐标轴（单位：μm）
    - z: ndarray 或 None，z 坐标轴（单位：μm），二维数据可不传
    - x_range, y_range, z_range: tuple(min, max) 或 None，筛选对应坐标范围

    返回:
    - result: dict，包含平均值与方差
    """

    # 判断维度
    if ek.ndim == 3 and z is None:
        raise ValueError("三维数据时必须传入 z 坐标数组")

    # 建立筛选掩码
    mask = np.ones_like(x, dtype=bool)
    if x_range is not None:
        mask &= (x >= x_range[0]) & (x <= x_range[1])
    if y_range is not None:
        mask &= (y >= y_range[0]) & (y <= y_range[1])
    if ek.ndim == 3 and z_range is not None:
        mask &= (z >= z_range[0]) & (z <= z_range[1])

    # 根据维度扁平化选取对应数据
    if ek.ndim == 3:
        # ek 是 3D，x, y, z 也应该是 3D 网格坐标，或一维坐标阵列与 ek 维度对应。
        # 这里假设 x, y, z 是一维坐标数组，对应 ek 的三个轴。
        # 使用掩码时，需要构造3D布尔数组：对三个轴分别掩码后广播组合。

        mask_3d = np.ones(ek.shape, dtype=bool)
        # x, y, z 是一维数组，ek 是 (len(x), len(y), len(z))
        # 对应维度做广播掩码
        x_mask = (x >= (x_range[0] if x_range else x[0])) & (x <= (x_range[1] if x_range else x[-1]))
        y_mask = (y >= (y_range[0] if y_range else y[0])) & (y <= (y_range[1] if y_range else y[-1]))
        z_mask = (z >= (z_range[0] if z_range else z[0])) & (z <= (z_range[1] if z_range else z[-1]))

        mask_3d = x_mask[:, None, None] & y_mask[None, :, None] & z_mask[None, None, :]
        sub_ek = ek[mask_3d]

    elif ek.ndim == 2:
        # 对二维数组，只用 x, y 筛选
        x_mask = (x >= (x_range[0] if x_range else x[0])) & (x <= (x_range[1] if x_range else x[-1]))
        y_mask = (y >= (y_range[0] if y_range else y[0])) & (y <= (y_range[1] if y_range else y[-1]))

        mask_2d = x_mask[:, None] & y_mask[None, :]
        sub_ek = ek[mask_2d]

    else:
        raise ValueError("ek 数据维度应为2或3维")

    if sub_ek.size == 0:
        raise ValueError("筛选后无匹配数据。")

    mean_val = np.mean(sub_ek)
    variance = np.var(sub_ek)

    print(f"x范围: [{x_range[0] if x_range else x[0]}, {x_range[1] if x_range else x[-1]}]")
    print(f"y范围: [{y_range[0] if y_range else y[0]}, {y_range[1] if y_range else y[-1]}]")
    if ek.ndim == 3:
        print(f"z范围: [{z_range[0] if z_range else z[0]}, {z_range[1] if z_range else z[-1]}]")
    print(f"平均能量 = {mean_val:.6e} J, 方差 = {variance:.6e}")

    return {
        'mean_energy': mean_val,
        'variance': variance
    }


