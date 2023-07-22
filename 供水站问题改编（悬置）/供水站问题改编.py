# 此代码目前存在的问题：按照建模原题，固定了一级水电站的基础上进行下面的求解，但是在中，一级本题水电站的位置是可以变化的，所以需要对代码进行修改，
# 使之可以自动寻找最佳的一级水电站位置。解决了这个问题，我们整个代码就算完成了。


# 本代码的目的是为了解决供水站问题，即在给定的站点中，选择最优的站点连接路线，使得总的管道长度最短。


# 本代码需要的python库：numpy, math, matplotlib.pyplot


# 准备原始数据
# initialData.py
coordinate_A = [26, 31]
coordinate_A_V = [[26, 31], [5, 33], [8, 9], [10, 24], [13, 34], [17, 23], [20, 10], [25, 47], [31, 18], [35, 42], [36, 25],
             [41, 31], [45, 38]]
coordinate_A_V_P = [[26, 31], [5, 33], [8, 9], [10, 24], [13, 34], [17, 23], [20, 10], [25, 47], [31, 18], [35, 42],
               [36, 25], [41, 31], [45, 38], [41, 35], [40, 34], [38, 35], [38, 37], [33, 37], [31, 36], [33, 35],
               [28, 32], [24, 30], [21, 31], [22, 27], [28, 29], [43, 37], [44, 39], [25, 27], [21, 29], [22, 30],
               [24, 32], [37, 33], [38, 33], [37, 36], [14, 13], [16, 9], [14, 7], [18, 14], [12, 6], [15, 14],
               [20, 13], [13, 46], [16, 39], [21, 39], [26, 44], [28, 40], [27, 42], [29, 38], [29, 44], [36, 44],
               [41, 40], [39, 52], [27, 49], [23, 46], [20, 46], [16, 46], [22, 44], [40, 44], [42, 40], [37, 42],
               [35, 49], [35, 51], [35, 52], [34, 55], [26, 53], [27, 51], [31, 51], [31, 45], [31, 41], [28, 45],
               [27, 35], [24, 38], [26, 39], [13, 37], [17, 36], [21, 41], [18, 41], [21, 43], [13, 39], [14, 43],
               [12, 43], [10, 44], [16, 44], [18, 44], [24, 44], [25, 49], [24, 49], [24, 51], [21, 48], [17, 51],
               [10, 34], [9, 35], [7, 37], [4, 37], [5, 42], [2, 44], [7, 32], [7, 30], [1, 24], [2, 16], [3, 18],
               [2, 20], [4, 24], [5, 28], [6, 24], [9, 29], [2, 33], [7, 34], [3, 30], [3, 41], [10, 36], [17, 34],
               [20, 22], [24, 21], [22, 17], [21, 16], [27, 19], [26, 16], [9, 16], [12, 17], [14, 15], [19, 26],
               [14, 28], [13, 25], [9, 19], [2, 1], [6, 6], [7, 8], [6, 14], [5, 17], [5, 16], [16, 19], [26, 13],
               [29, 11], [31, 14], [28, 17], [20, 19], [17, 22], [15, 23], [21, 23], [24, 23], [26, 23], [25, 25],
               [15, 31], [15, 29], [10, 28], [38, 26], [37, 25], [33, 21], [40, 24], [44, 44], [41, 30], [33, 24],
               [32, 27], [40, 14], [42, 26], [45, 33], [29, 23], [31, 30], [30, 25], [31, 23], [35, 15], [40, 16],
               [40, 20], [37, 20], [35, 24], [43, 23], [45, 26], [37, 28], [35, 28], [33, 29], [37, 30], [39, 30],
               [41, 29], [43, 31], [47, 34], [46, 43], [42, 43], [48, 45], [42, 44], [43, 50]]

# distance.py

import numpy as np
import math as m

# 计算站点之间距离,并返回一个数组
def Distance(coordinate_sites):
    number_sites = len(coordinate_sites)
    distance = np.zeros((number_sites,number_sites))
    for i in range(number_sites):
        for j in range(number_sites):
            distance_i_j = m.sqrt((coordinate_sites[i][0] - coordinate_sites[j][0])**2 + (coordinate_sites[i][1] - coordinate_sites[j][1])**2)
            if distance_i_j !=0:
                distance[i,j] = distance_i_j
            else:
                distance_i_j = 1000     #粗略估计，算出的不同两点间的距离都小于1000（大数即可），将1000作为自身到自身的距离，
    return distance

#bool.py

def BoolSites(coordinate_sites):
    if len(coordinate_sites) == 13:
        bool_A_V = np.zeros((13, 13))
        return bool_A_V
    elif len(coordinate_sites) == 181:
        bool_A_V_P = np.zeros((181, 181))
        for i in range(13):
            for j in range(13):
                bool_A_V_P[i, j] = 1
        bool_A_V_P[0, :] = 1
        bool_A_V_P[:, 0] = 1
        return bool_A_V_P

# prim.py


def Prim(coordinate_sites):
    number = len(coordinate_sites)
    distance_sites = Distance(coordinate_sites)
    Bool = BoolSites(coordinate_sites)      #用于屏蔽处理

    if number ==13:
        Already_sites = [0]     #已经连上的站点，从中心供水站A开始计数0
        route_sites = []  # 选取的站点连接路线
    elif number == 181:
        Already_sites = Prim(coordinate_A_V)[1] #因为下面的while len(Already_sites) != number中的Already_sites是以之前的为基础
        route_sites = Prim(coordinate_A_V)[0]
    while len(Already_sites) != number:
        # 做屏蔽处理
        for i in Already_sites:
            for j in Already_sites:
                if Bool[i, j] == 0 and [i, j] not in route_sites and [j, i] not in route_sites:
                    Bool[i, j] = 1
                    Bool[j, i] = 1

        min_distance = 1000  # 用于判断选取最短距离，即局部最小权
        count = 0
        original_len = len(Already_sites)
        # 循环用于选择并增加新路径
        for i in Already_sites:
            # 在结束一次循环后，对于Already_sites的更改会反馈到‘for i in Already_sites'中，因为是列表。
            # 所以该判别语句用语循环的跳出。
            if original_len < len(Already_sites) and i == Already_sites[-1]:
                break

            # Bool[i,j]为0，表示可以建立新的连线；通过min_distance判断
            # 这里的min_distance会保留到下一个i的循环，继续对count=1时扩充的位置进行修正和确定
            for j in range(1, number):
                if min_distance >= distance_sites[i][j] and Bool[i, j] == 0:
                    min_distance = distance_sites[i][j]
                    count = count + 1
                    # 相当于在route_sites和Already_sites中分别扩充一个位置
                    if count == 1:
                        route_sites.append([i, j])
                        Bool[i, j] = 1
                        Bool[j, i] = 1
                        Already_sites.append(j)

                    # 在本次的i下，对扩充的位置进行数据的修正和确定
                    else:
                        # print(count)
                        Bool[route_sites[len(route_sites) - 1][0], route_sites[len(route_sites) - 1][1]] = 0
                        Bool[route_sites[len(route_sites) - 1][1], route_sites[len(route_sites) - 1][0]] = 0
                        route_sites[len(route_sites) - 1] = [i, j]
                        Bool[route_sites[len(route_sites) - 1][0], route_sites[len(route_sites) - 1][1]] = 1
                        Bool[route_sites[len(route_sites) - 1][1], route_sites[len(route_sites) - 1][0]] = 1
                        Already_sites[len(Already_sites) - 1] = j

    # 以下两次屏蔽处理没有实际意义
    Bool[:, Already_sites[-1]] = 1
    Bool[Already_sites[-1], :] = 1

    return [route_sites, Already_sites]     # 导出路径结果

# pipeLaying.py

import matplotlib.pyplot as plt


route_A_V = Prim(coordinate_A_V)[0]
print(route_A_V)
# 绘制AV站点之间的最优路线图
for i in route_A_V:
    x = [coordinate_A_V[i[0]][0], coordinate_A_V[i[1]][0]]
    y = [coordinate_A_V[i[0]][1], coordinate_A_V[i[1]][1]]
    plt.plot(x, y)
plt.show()

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
for i in route_A_V_P:
    count += 1
    x = [coordinate_A_V_P[i[0]][0], coordinate_A_V_P[i[1]][0]]
    y = [coordinate_A_V_P[i[0]][1], coordinate_A_V_P[i[1]][1]]
    if count <= 12:
        plt.plot(x, y, color='red')
        sum_pipeline_A_V += Distance(coordinate_A_V_P)[i[0], i[1]]
    else:
        plt.plot(x, y, color='blue')
    sum_pipeline_A_V_P += Distance(coordinate_A_V_P)[i[0], i[1]]
print("sum_pipeline_A_V={}, sum_pipeline_A_V_P={}, sum_pipeline_A_V_P - sum_pipeline_A_V={}".format(sum_pipeline_A_V, sum_pipeline_A_V_P, sum_pipeline_A_V_P - sum_pipeline_A_V))
plt.show()
