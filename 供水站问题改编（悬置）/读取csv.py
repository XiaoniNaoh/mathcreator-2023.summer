import csv

csv_file = '地点信息.csv'  # CSV文件路径

coordinates = []  # 存储坐标的列表

with open(csv_file, newline='') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行

    for row in reader:
        # 提取X坐标和Y坐标
        x = int(row[2])
        y = int(row[3])

        # 添加坐标到列表
        coordinates.append([x, y])

print(coordinates)