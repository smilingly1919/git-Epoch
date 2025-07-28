import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设置
E_J_to_MeV = 1.0 / 1.6e-13
step = 5
species = "Photon"

# 设置你要读取的单个文件路径
base_dir = '/media/lan/4248e56e-6d9a-4026-afad-e8b1d59ceab0/epoch-set2/epoch3d/ju2024+b2'
file_name = 'distfun0030.sdf'  # 你要查看的文件名
label = 'B2_T0=30'

file_path = os.path.join(base_dir, file_name)

# === 数据读取与处理 ===
data = sh.getdata(file_path)
E_J = getattr(data, f'Grid_allenergy0_{species}').data[0]
dN = getattr(data, f'dist_fn_allenergy0_{species}').data

E_MeV = E_J * E_J_to_MeV

length = len(E_MeV)
if length % step != 0:
    E_MeV = E_MeV[:-(length % step)]
    dN = dN[:-(length % step)]

# 多点合并bin
E_merged = np.mean(E_MeV.reshape(-1, step), axis=1)  # 每step个bin的能量均值
N_merged = np.sum(dN.reshape(-1, step), axis=1)       # 每step个bin的粒子数求和

dE_merged = np.mean(np.diff(E_merged))
spectrum_merged = N_merged / dE_merged

# === 绘图 ===
plt.figure(figsize=(7, 6))
plt.semilogy(E_merged, spectrum_merged, label=label, linewidth=2, alpha=0.8)

plt.xlabel(rf'{species} Energy $E$ (MeV)', fontsize=14)
plt.ylabel(r'd$N$/d$E$', fontsize=14)
plt.title(f'Energy Spectrum: {label}', fontsize=15)
plt.xlim(1, 100)
plt.tick_params(axis='both', direction='in', which='both', labelsize=12)
plt.legend(fontsize=10)
plt.tight_layout()
plt.show()
