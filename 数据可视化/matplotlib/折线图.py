# 需要安装matplotlib依赖，安装方法 pip install matplotlib
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8')
"""采用预设的内置样式
plt.style.available
['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 
'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 
'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 
'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 
'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 
'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']"""

fig, ax = plt.subplots()
"""fig表示整个图形面板, ax表示绘图的图形"""

x_values = range(1, 1001)
y_values = [x**2 for x in x_values]
"""
#绘制二维线段
ax.plot(input_values, squares, linewidth = 3) # linewidth表示绘制线条的粗细
"""

"""绘制点"""
#ax.scatter(x_values, y_values, color='red', s=10)
point_numbers = range(1000)
ax.scatter(x_values, y_values, c=point_numbers, cmap=plt.cm.Blues, edgecolors='none', s=10) # 使用渐变颜色
"""
渐变颜色查询进入官方网站 https://matplotlib.org/

"""
#设置图题并给坐标轴加上标签
ax.set_title("Square Numbers", fontsize=24) # 绘图的标题, fontsize表示字体大小
ax.set_xlabel("Value", fontsize=14) # 绘图x轴标记
ax.set_ylabel("Square of Value", fontsize=14) # 绘图y轴标记
ax.tick_params(labelsize=14) # 刻度线标记尺寸
ax.axis([0, 1100, 0, 1100000]) # 设置每个坐标轴的取值范围
ax.ticklabel_format(style='plain') #采用非科学计数法

plt.show()
#plt.savefig('squares_plot.png', bbox_inches='tight')