from pathlib import Path
import csv
import matplotlib.pyplot as plt

path = Path(R'数据可视化\csvandjson\data\sitka_weather_07-2021_simple.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

# 提取最高温度
highs = []
for row in reader:
    high = int(row[4])
    highs.append(high)

print('读取'+ header_row[4] + '数据如下：',highs)
print('共计数据：',len(highs))

# 根据最高温度绘图
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(highs, color = 'red')

#设置格式
ax.set_title("Daily High Temperatures, July 2021", fontsize=24)
ax.set_xlabel('', fontsize = 16)
ax.set_ylabel('Temperature(F)', fontsize = 16)
ax.tick_params(labelsize = 16)

plt.show()

