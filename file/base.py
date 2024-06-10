#Path类载入
from pathlib import Path

myFiles = ['accounts.txt','details.csv','invite.docx']
#多平台文件地址操作方法
#Path(A,B，...)地址连接
print('1: ' , Path(myFiles[0],myFiles[1],myFiles[2]))

#Path用运算符连接地址/
print('2: ' , Path(myFiles[0]) / myFiles[1])

#获取当前工作目录Path.cwd()
print('3: ' , Path.cwd())
print('4: ' , Path.cwd() / 'file' / 'base.py')

#改变工作目录os.chdir()
import os
os.chdir(Path.cwd() / 'file')
print('5: ' , Path.cwd())
#如果被更改的目录不存都在会报错FileNotFoundError
try:
    os.chdir("D:\lee\ss")
except FileNotFoundError as err:
    print("    目录不存在:",err)

#主目录获取Path.home
print('6: ' , Path.home())

#创建文件夹
workPath = Path.cwd()
print('7:  当前目录为:', workPath)
workPath = workPath.parents[0] / 'temp测试'
print('    我们在这个目录下创建目录:', workPath)
Path.mkdir(workPath / 'Path方法')
print('    Path方法创建目录:', workPath / 'Path方法')
os.makedirs(workPath / 'os方法')
print('    os方法创建目录:', workPath / 'os方法')

#删除文件夹
Path.rmdir(workPath / 'Path方法')
print('8:  Path方法删除目录:',workPath / 'Path方法')
os.rmdir(workPath / 'os方法')
print('    os方法删除目录:',workPath / 'os方法')

