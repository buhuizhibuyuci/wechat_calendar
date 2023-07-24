# import subprocess
#
# # 获取用户输入的用户名和密码
# username = input("Enter MySQL username: ")
# password = input("Enter MySQL password: ")
#
# # 构建要执行的命令
# command = f"mysql -u {username} -p{password}"
#
# # 打开子进程并与MySQL终端进行交互
# process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#
# while True:
#     # 执行SQL语句
#     sql_statement = input("Enter SQL statement (or 'quit' to exit): ")
#     if sql_statement == "quit":
#         break
#
#     # 向子进程发送输入并获取输出结果
#     process.stdin.write((sql_statement + "\n").encode())
#     process.stdin.flush()
#
#     output, error = process.communicate()
#
#     if output:
#         print(output.decode())
#     if error:
#         print(error.decode())
#
# process.wait()

import subprocess
child = subprocess.Popen('mysql -uroot -proot',shell=True)
x = subprocess.Popen('show databases',shell=True)
x.wait()
child.wait() # 等待子进程结束
print('ok')