import subprocess

# 调用的Python程序的文件路径
python_program_path = 'bin/GyoiThon/gyoithon.py'

# 使用subprocess模块运行另一个Python程序，并将其输出显示在当前终端中
process = subprocess.Popen(['python', '-u', python_program_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# 将输出解码为字符串并打印出来
for line in process.stdout:
    print(line, end='')

# 等待子进程结束
process.wait()
