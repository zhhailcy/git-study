f = open('file.txt', 'r')

# data = f.read()
# print('读取到的内容:', data)
#
# while True:
#     data = f.read(3)
#     if not data:   # not data 等于 data == ''
#         break
#     print(data)

# data = f.readline()
# print(data)

# data = f.readlines()
# print(data)

for line in f:
    print(line, end='')


f.close()
