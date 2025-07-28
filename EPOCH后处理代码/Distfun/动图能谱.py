import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# 路径设定
base_path = '/media/lan/4248e56e-6d9a-4026-afad-e8b1d59ceab0/epoch-set2/epoch2d/激光电子对撞/无激光5GeV+bx磁场1e10'
file_prefix = 'distfun'
file_suffix = '.sdf'

# 常数定义
E_eV_to_E_J = 1.6e-19
E_J_to_E_eV = 1 / E_eV_to_E_J

# 预读取第一个文件获取横轴能量坐标
first_file = os.path.join(base_path, f"{file_prefix}{1:04d}{file_suffix}")
first_data = sh.getdata(first_file)
dE = first_data.Grid_en_Photon.data[0]
dE_MeV = 1e-6 * E_J_to_E_eV * dE
Delta_E_MeV = np.mean(np.diff(dE_MeV))

# 初始化画布
fig, ax = plt.subplots(figsize=(6,6))
line, = ax.semilogy([], [], label="ele", linewidth=2, alpha=0.7)
ax.set_xlim(dE_MeV.min(), dE_MeV.max())
ax.set_ylim(1e0, 1e12)  # 根据实际数据设置范围
ax.set_xlabel(r'$E$ (MeV)', fontsize=14)
ax.set_ylabel(r'd$N$/d$E$', fontsize=14)
ax.set_title('Energy Spectrum')
ax.tick_params(axis='both', direction='in', which='both', labelsize=12)

# 更新函数
def update(frame):
    index = frame + 1  # 从1开始
    file_name = f"{file_prefix}{index:04d}{file_suffix}"
    file_path = os.path.join(base_path, file_name)
    
    if not os.path.exists(file_path):
        print(f"File {file_name} not found.")
        return line,

    distfun_Data = sh.getdata(file_path)
    dN = distfun_Data.dist_fn_en_Photon.data
    spectrum = dN / Delta_E_MeV

    line.set_data(dE_MeV, spectrum)
    ax.set_title(f"Energy Spectrum - Frame {index}")
    return line,

# 创建动画
ani = animation.FuncAnimation(fig, update, frames=80, blit=True)

# 保存为 gif（可选）
# ani.save("spectrum_animation.gif", writer="pillow", fps=5)

plt.show()
