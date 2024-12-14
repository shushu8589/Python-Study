from die import Die
#需要安装库 pip install plotly,pandas
import plotly.express as px

#创建一个D6的骰子
die_1 = Die()
die_2 = Die(10)

#骰多少次
die_num = 50000

#生成数据列表
results = []
for roll_num in range(die_num):
    result = die_1.roll() + die_2.roll()
    results.append(result)

#生成分析报表
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
poss_results = range(1, max_result + 1)
for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

# 对结果进行可视化
title = "Results of Rolling Two D6 Dice 1,000 Times"
lables = {'x': 'Result', 'y': 'Frequency of Result'}
fig = px.bar(x=poss_results, y=frequencies, title=title, labels=lables)
fig.update_layout(xaxis_dtick=1)
fig.show()

fig.write_html('lee123.html')
#keep_running = input("Make another walk? (y/n): ")