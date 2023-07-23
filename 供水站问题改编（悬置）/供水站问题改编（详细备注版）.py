coordinate_A = [26, 31]
coordinate_A_V = [[26, 31], [5, 33], [8, 9], [10, 24], [13, 34], [17, 23], [20, 10], [25, 47], [31, 18], [35, 42], [36, 25],
             [41, 31], [45, 38]]
coordinate_A_V_P = [[26, 31], [5, 33], [8, 9], [10, 24], [13, 34], [17, 23], [20, 10], [25, 47], [31, 18], [35, 42], [36, 25], [41, 31], [45, 38], [41, 35], [40, 34], [38, 35], [38, 37], [33, 37], [31, 36], [33, 35], [28, 32], [24, 30], [21, 31], [22, 27], [28, 29], [43, 37], [44, 39], [25, 27], [21, 29], [22, 30], [24, 32], [37, 33], [38, 33], [37, 36], [14, 13], [16, 9], [14, 7], [18, 14], [12, 6], [15, 14], [20, 13], [13, 46], [16, 39], [21, 39], [26, 44], [28, 40], [27, 42], [29, 38], [29, 44], [35, 43], [41, 40], [39, 52], [27, 49], [23, 46], [20, 46], [16, 46], [22, 44], [40, 44], [42, 40], [37, 42], [35, 49], [35, 51], [35, 52], [34, 55], [26, 53], [27, 51], [31, 51], [31, 45], [31, 41], [28, 45], [27, 35], [25, 38], [26, 39], [13, 37], [17, 36], [21, 41], [18, 41], [21, 43], [13, 39], [14, 43], [12, 43], [10, 44], [16, 44], [18, 44], [24, 44], [25, 49], [24, 49], [24, 51], [21, 48], [17, 51], [10, 34], [9, 35], [7, 37], [4, 37], [5, 42], [2, 44], [7, 32], [7, 30], [1, 24], [2, 16], [3, 18], [2, 20], [4, 24], [5, 28], [6, 24], [9, 29], [2, 33], [7, 34], [3, 30], [3, 41], [10, 36], [17, 34], [20, 22], [24, 21], [22, 17], [21, 16], [27, 19], [26, 16], [9, 16], [12, 17], [14, 15], [19, 26], [14, 28], [13, 25], [9, 19], [2, 1], [6, 6], [7, 8], [6, 14], [5, 17], [5, 16], [16, 19], [26, 13], [29, 11], [31, 14], [28, 17], [20, 19], [17, 22], [15, 23], [21, 23], [24, 23], [26, 23], [25, 25], [15, 31], [15, 29], [10, 28], [38, 26], [37, 25], [33, 21], [40, 24], [44, 44], [42, 31], [33, 24], [32, 27], [40, 14], [42, 26], [45, 33], [29, 23], [31, 30], [30, 25], [31, 23], [35, 15], [40, 16], [40, 20], [37, 20], [35, 24], [43, 23], [45, 26], [37, 28], [35, 28], [33, 29], [37, 30], [39, 30], [41, 29], [43, 31], [47, 34], [46, 43], [42, 43], [48, 45], [42, 44], [43, 50]]

import numpy as np
import math as m

# 计算站点之间距离,并返回一个数组
def Distance(coordinate_sites):
    # 获取站点数量
    number_sites = len(coordinate_sites)
    # 创建一个全零矩阵，用于存储站点之间的距离
    distance = np.zeros((number_sites,number_sites))
    # 计算每两个站点之间的距离
    for i in range(number_sites):
        for j in range(number_sites):
            # 计算站点i和站点j之间的距离
            distance_i_j = m.sqrt((coordinate_sites[i][0] - coordinate_sites[j][0])**2 + (coordinate_sites[i][1] - coordinate_sites[j][1])**2)
            # 如果站点i和站点j不是同一个站点
            if distance_i_j !=0:
                # 将站点i和站点j之间的距离存入矩阵
                distance[i,j] = distance_i_j
            else:
                # 如果站点i和站点j是同一个站点，将距离设为1000
                distance_i_j = 1000
    return distance

# 创建一个布尔矩阵，用于后续的屏蔽处理
def BoolSites(coordinate_sites):
    # 获取站点数量
    number_sites = len(coordinate_sites)
    # 如果站点数量是13
    if number_sites == 13:
        # 创建一个13x13的全零矩阵
        bool_A_V = np.zeros((13, 13))
        return bool_A_V
    # 如果站点数量是181
    elif number_sites == 181:
        # 创建一个181x181的全零矩阵
        bool_A_V_P = np.zeros((181, 181))
        # 将第一行和第一列以及前13x13的部分设为1
        for i in range(13):
            for j in range(13):
                bool_A_V_P[i, j] = 1
        bool_A_V_P[0, :] = 1
        bool_A_V_P[:, 0] = 1
        return bool_A_V_P

def Prim(coordinate_sites):
    # 获取站点数量
    number = len(coordinate_sites)
    # 计算站点之间的距离
    distance_sites = Distance(coordinate_sites)
    # 创建一个布尔矩阵，用于后续的屏蔽处理
    Bool = BoolSites(coordinate_sites)

    # 如果站点数量是13
    if number == 13:
        # 已经连上的站点，从中心供水站A开始计数0
        Already_sites = [0]
        route_sites = []  # 选取的站点连接路线
    # 如果站点数量是 181
    elif number == 181:
        Already_sites = Prim(coordinate_A_V)[1]  # 已经连上的站点
        route_sites = Prim(coordinate_A_V)[0]  # 选取的站点连接路线

    while len(Already_sites) != number:
        # 做屏蔽处理
        for i in Already_sites:
            for j in Already_sites:
                if Bool[i, j] == 0 and [i, j] not in route_sites and [j, i] not in route_sites:
                    Bool[i, j] = 1
                    Bool[j, i] = 1

        min_distance = 1000  # 初始设定的最小距离
        count = 0  # 计数器
        original_len = len(Already_sites)

        # 循环用于选择并增加新路径
        for i in Already_sites:
            # 当已连上路径数量增加并且已经循环结束时，跳出循环
            if original_len < len(Already_sites) and i == Already_sites[-1]:
                break

            # Bool[i,j]为0，表示可以建立新的连线；通过min_distance判断
            for j in range(number):
                if min_distance >= distance_sites[i][j] and Bool[i, j] == 0:
                    min_distance = distance_sites[i][j]
                    count = count + 1
                    # 扩充路径和已连接站点
                    if count == 1:
                        route_sites.append([i, j])
                        Bool[i, j] = 1
                        Bool[j, i] = 1
                        Already_sites.append(j)
                    # 在本次的i下，对扩充的位置进行数据的修正和确定
                    else:
                        Bool[route_sites[-1][0], route_sites[-1][1]] = 0
                        Bool[route_sites[-1][1], route_sites[-1][0]] = 0
                        route_sites[-1] = [i, j]
                        Bool[i, j] = 1
                        Bool[j, i] = 1
                        Already_sites[-1] = j

    # 最终路径的屏蔽处理
    Bool[:, Already_sites[-1]] = 1
    Bool[Already_sites[-1], :] = 1

    return [route_sites, Already_sites]  # 返回路径结果


import matplotlib.pyplot as plt

# 计算AV站点之间的最优路线
route_A_V = Prim(coordinate_A_V)[0]
print(route_A_V)

# 绘制AV站点之间的最优路线图
for i in route_A_V:
    x = [coordinate_A_V[i[0]][0], coordinate_A_V[i[1]][0]]
    y = [coordinate_A_V[i[0]][1], coordinate_A_V[i[1]][1]]
    plt.plot(x, y)
plt.show()

# 计算AVP站点之间的最优路线
route_A_V_P = Prim(coordinate_A_V_P)[0]
print(route_A_V_P)

# 绘制AVP站点之间的最优路线图
x = []
y = []
for i in coordinate_A_V_P:
    x.append(i[0])
    y.append(i[1])
plt.scatter(x[:13], y[:13], 15, "red")
plt.scatter(x[13:], y[13:], 10, "blue")

count = 0
sum_pipeline_A_V = 0
sum_pipeline_A_V_P = 0

# 遍历AVP站点之间的最优路线
for i in route_A_V_P:
    count += 1
    x = [coordinate_A_V_P[i[0]][0], coordinate_A_V_P[i[1]][0]]
    y = [coordinate_A_V_P[i[0]][1], coordinate_A_V_P[i[1]][1]]

    if count <= 12:
        # 前12条路线绘制为红色
        plt.plot(x, y, color='red')
        sum_pipeline_A_V += Distance(coordinate_A_V_P)[i[0], i[1]]
    else:
        # 后面的路线绘制为蓝色
        plt.plot(x, y, color='blue')

    sum_pipeline_A_V_P += Distance(coordinate_A_V_P)[i[0], i[1]]

# 输出管道长度统计结果
print("sum_pipeline_A_V={}, sum_pipeline_A_V_P={}, sum_pipeline_A_V_P - sum_pipeline_A_V={}".format(sum_pipeline_A_V,
                                                                                                    sum_pipeline_A_V_P,
                                                                                                    sum_pipeline_A_V_P - sum_pipeline_A_V))
plt.show()

def check_distance(coordinate_A_V, coordinate_A_V_P):
    # 计算一级站点与二级站点之间的距离
    distance_A_V_P = Distance(coordinate_A_V_P)
    # 初始化一个变量，用于记录所有的二级站点是否都正常
    all_normal = True
    # 遍历所有的二级站点
    for i in range(13, len(coordinate_A_V_P)):
        # 找出每个二级站点距离最近的一级站点
        min_distance = min(distance_A_V_P[i][:13])
        if min_distance > 30:
            print(f"警告：二级站点{i}距离最近的一级站点的距离超过30，具体距离为{min_distance}")
            all_normal = False
        else:
            print(f"正常：二级站点{i}距离最近的一级站点的距离等于或小于30，具体距离为{min_distance}")
    # 检查所有的二级站点是否都正常
    if all_normal:
        print("全部正常：所有二级站点距离最近的一级站点的距离都等于或小于30。")
    else:
        print("存在警告：有些二级站点距离最近的一级站点的距离超过30。")

# 在计算AVP站点之间的最优路线之后调用这个函数
route_A_V_P = Prim(coordinate_A_V_P)[0]
print(route_A_V_P)
check_distance(coordinate_A_V, coordinate_A_V_P)
