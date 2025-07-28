from matplotlib import rcParams

def use_times_new_roman_advanced():
    rcParams['font.family'] = ['Times New Roman', 'SimHei']  # 英文/中文字体
    rcParams['axes.unicode_minus'] = False  # 负号正常显示

    # 标题字体大小和加粗
    rcParams['axes.titlesize'] = 16
    # rcParams['axes.titleweight'] = 'bold'

    # 坐标轴标签字体大小
    rcParams['axes.labelsize'] = 20

    # 刻度字体大小
    rcParams['xtick.labelsize'] = 12
    rcParams['ytick.labelsize'] = 12

    # 坐标轴刻度向内
    rcParams['xtick.direction'] = 'in'
    rcParams['ytick.direction'] = 'in'

    # # 坐标轴刻度长度和宽度
    # rcParams['xtick.major.size'] = 6
    # rcParams['ytick.major.size'] = 6
    # rcParams['xtick.major.width'] = 1
    # rcParams['ytick.major.width'] = 1

    # # 网格线设置（可选）
    # rcParams['grid.linestyle'] = '--'
    # rcParams['grid.alpha'] = 0.3

    # 图例字体大小
    rcParams['legend.fontsize'] = 12
