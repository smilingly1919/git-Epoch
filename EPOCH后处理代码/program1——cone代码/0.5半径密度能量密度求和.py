import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sdf_helper as sh
import csv

# ----------- 文件路径和读取参数设置 -----------
base_path = '/media/lan/4248e56e-6d9a-4026-afad-e8b1d59ceab0/epoch/epoch3d/Cpf-Work/cone/cone1-a=145-0.75微米'
file_prefix = 'density'
file_suffix = '.sdf'
file_index = 18
den_crit = 0.17419597124e28

file_name = f"{file_prefix}{file_index:04d}{file_suffix}"
file_path = os.path.join(base_path, file_name)
data = sh.getdata(file_path)

ne = data.Derived_Number_Density_Photon.data / den_crit
ne_e = data.Derived_Number_Density_Photon.data 
E = data.Derived_Average_Particle_Energy_Photon.data
nE = ne_e * E

x = data.Grid_Grid_mid.data[0] / 1e-6
y = data.Grid_Grid_mid.data[1] / 1e-6
z = data.Grid_Grid_mid.data[2] / 1e-6

# ----------- 创建圆形掩膜（r < 0.5 μm） -----------
Y, Z = np.meshgrid(y, z, indexing='ij')
R2 = Y**2 + Z**2
circular_mask = R2 < 0.5**2

# ----------- 积分（对 y-z 平面上圆形区域） -----------
ne_sum_circular = np.array([np.sum(ne[i][circular_mask]) for i in range(ne.shape[0])])
nE_sum_circular = np.array([np.sum(nE[i][circular_mask]) for i in range(ne.shape[0])])

# ----------- 设置 x 区间列表 -----------
# x_ranges = [(42, 43.3), (43.3, 44.1), (44.1, 44.9),(44.9,45.7),(45.7,46.5),
#             (46.5,47.3),(47.3,48.3),(48.3,49.3),(49.3,50)] #0.5

x_ranges = [(42.5, 43.3), (43.3, 44.2), (44.2, 44.8),(44.8,45.7),
(45.7,46.5),(46.5,47.3),(47.3,48.2),(48.2,49),(49,50)] #0.75

# x_ranges = [(42.5, 43.3), (43.3, 44.1), (44.1, 44.9),(44.9,45.7),(45.7,46.5),
# (46.5,47.3),(47.3,48.3),(48.3,49.3),(49.3,50)] #1

# x_ranges = [(42.5, 43.3), (43.3, 44.1), (44.1, 44.9),(44.9,45.7),(45.7,46.7),
#             (46.7,47.3),(47.3,48.3),(48.3,49.3),(49.3,50)] #1.5，2

# x_ranges = [(42.5, 43.3), (43.3, 44.1), (44.1, 44.9),(44.9,45.7),
# (45.7,46.5),(46.5,47.5),(47.5,48.3),(48.3,48.9),(48.9,50)] #2.5

# x_ranges = [(42.5, 43.3), (43.3, 44.2), (44.2, 44.9),(44.9,45.9),
#             (45.9,46.7),(46.7,47.3),(47.3,48.3),(48.3,49.1),(49.1,50)] #3

# ----------- 创建图形与子图 -----------
fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
plt.subplots_adjust(hspace=0.3)


output_dir = '/media/lan/Lexar/EPOCH代码/program1——cone代码'   # 你想保存到其它文件夹，比如 /media/lan/output_csv/
os.makedirs(output_dir, exist_ok=True) # 如果目录不存在，可以先创建
csv_path = os.path.join(output_dir, f'0.75density_energy_peaks_{file_index:04d}.csv') # 新的 CSV 文件完整路径

# 然后写文件
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['x_min', 'x_max', 'x_peak_ne', 'ne_max', 'x_peak_nE', 'nE_max'])

    # ----------- 第一个子图：光子数密度积分 -----------
    ax1 = axes[0]
    ax1.plot(x, ne_sum_circular, color='gray', alpha=0.5, label='Full Curve')

    # ----------- 第二个子图：能量密度积分 -----------
    ax2 = axes[1]
    ax2.plot(x, nE_sum_circular, color='gray', alpha=0.5, label='Full Curve')

    for x_min, x_max in x_ranges:
        mask = (x >= x_min) & (x <= x_max)
        x_limited = x[mask]

        ne_limited = ne_sum_circular[mask]
        nE_limited = nE_sum_circular[mask]

        max_ne = ne_limited.max()
        max_x_ne = x_limited[np.argmax(ne_limited)]
        max_nE = nE_limited.max()
        max_x_nE = x_limited[np.argmax(nE_limited)]

        ax1.plot(x_limited, ne_limited, label=f'{x_min}-{x_max} μm')
        ax1.axvline(max_x_ne, linestyle='--', color='red', alpha=0.6)
        ax1.text(max_x_ne, max_ne, f'{max_ne:.2e}', fontsize=9, ha='center', va='bottom', color='red')

        ax2.plot(x_limited, nE_limited, label=f'{x_min}-{x_max} μm')
        ax2.axvline(max_x_nE, linestyle='--', color='blue', alpha=0.6)
        ax2.text(max_x_nE, max_nE, f'{max_nE:.2e}', fontsize=9, ha='center', va='bottom', color='blue')

        # 写入 CSV 行
        writer.writerow([x_min, x_max, max_x_ne, max_ne, max_x_nE, max_nE])

# ----------- 图像格式设置 -----------
ax1.set_ylabel(r'$n_\gamma/n_c$')
ax1.legend(fontsize=8)
ax1.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

ax2.set_xlabel(r'$x\ (\mu\mathrm{m})$')
ax2.set_ylabel(r'$n_\gamma E_\gamma$ (arb. units)')
ax2.legend(fontsize=8)
ax2.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
ax2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

# ----------- 保存 PDF 图像 -----------
# pdf_path = os.path.join(base_path, f'density_energy_sum_{file_index:04d}.pdf')
# plt.savefig(pdf_path)
plt.show()

