import numpy as np
import math as m
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial import distance

def find_closest_points(points, k):
    # 使用KMeans算法进行聚类
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(points)

    # 获取聚类的中心点坐标
    centers = kmeans.cluster_centers_

    # 寻找距离中心点最近的点的坐标
    labels = kmeans.labels_
    distances = kmeans.transform(points)

    closest_points = []

    # 遍历每个中心点
    for i in range(k):
        # 获取距离第i个中心点最近的点的索引
        closest_point_index = np.argmin(distances[:, i])

        # 获取最近的点的坐标
        closest_point = points[closest_point_index]

        closest_points.append(closest_point)

    return np.array(closest_points)

# 计算站点之间距离,并返回一个数组
def calculate_distance(coordinate_sites):
    return distance.cdist(coordinate_sites, coordinate_sites, 'euclidean')

# 根据站点数量创建布尔矩阵
def create_bool_matrix(coordinate_sites, k):
    number_sites = len(coordinate_sites)
    bool_A_V_P = np.zeros((number_sites, number_sites))
    for i in range(number_sites):
        for j in range(number_sites):
            if i == j:
                bool_A_V_P[i, j] = 1
            elif i < k and j < k:
                bool_A_V_P[i, j] = 1
    return bool_A_V_P

# Prim算法计算最优路线
def prim_algorithm(coordinate_sites, max_pipeline_length):
    number = len(coordinate_sites)
    distance_sites = calculate_distance(coordinate_sites)
    Bool = create_bool_matrix(coordinate_sites, number)      # 用于屏蔽处理

    Already_sites = [0]     # 已经连上的站点，从中心供水站A开始计数0
    route_sites = []  # 选取的站点连接路线

    while len(Already_sites) != number:
        # 做屏蔽处理
        for i in Already_sites:
            for j in Already_sites:
                if Bool[i, j] == 0 and [i, j] not in route_sites and [j, i] not in route_sites:
                    Bool[i, j] = 1
                    Bool[j, i] = 1

        min_distance = float('inf')  # 用于判断选取最短距离，即局部最小权
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
            for j in range(number):
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
                        Bool[route_sites[-1][0], route_sites[-1][1]] = 0
                        Bool[route_sites[-1][1], route_sites[-1][0]] = 0
                        route_sites[-1] = [i, j]
                        Bool[route_sites[-1][0], route_sites[-1][1]] = 1
                        Bool[route_sites[-1][1], route_sites[-1][0]] = 1
                        Already_sites[-1] = j

        # 判断路径总长度是否超过最大限制
        pipeline_length = sum([distance_sites[i][j] for i, j in route_sites])
        if pipeline_length > max_pipeline_length:
            print("路径总长度超过最大限制")
            return None

    Bool[:, Already_sites[-1]] = 1
    Bool[Already_sites[-1], :] = 1

    return [route_sites, Already_sites]     # 导出路径结果

# 生成站点坐标
points = np.array([[26, 31], [5, 33], [8, 9], [10, 24], [13, 34], [17, 23], [20, 10], [25, 47], [31, 18], [35, 42], [36, 25],
             [41, 31], [45, 38], [26, 31], [5, 33], [8, 9], [10, 24], [13, 34], [17, 23], [20, 10], [25, 47], [31, 18], [35, 42],
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
               [41, 29], [43, 31], [47, 34], [46, 43], [42, 43], [48, 45], [42, 44], [43, 50]])

k_start = 12
k_end = 20
max_pipeline_length = 30

# 计算I型管道的费用
def calculate_I_pipeline_cost(distance):
    pipeline_length = distance / 1000  # 转换为千米
    pipeline_cost = pipeline_length * 720
    return pipeline_cost

# 计算II型管道的费用
def calculate_II_pipeline_cost(distance):
    pipeline_length = distance / 1000  # 转换为千米
    pipeline_cost = pipeline_length * 210
    return pipeline_cost

for k in range(k_start, k_end+1):
    closest_points = find_closest_points(points, k)
    print("k =", k)
    print("一级站点坐标：")
    print(closest_points)

    route_A_V_P = prim_algorithm(closest_points, max_pipeline_length)

    if route_A_V_P is None:
        print("一级站点与二级站点的路径总长度超过最大限制")
        continue

    print("AVP站点之间的最优路线：")
    print(route_A_V_P)

    # 计算最小费用和管道长度
    min_cost = 0
    total_I_pipeline_length = 0
    total_II_pipeline_length = 0

    # 计算中心供水站A到一级供水站的I型管道费用和长度
    for i, j in route_A_V_P[0]:
        if i == 0:
            distance = distance.euclidean(points[i], points[j])
            pipeline_cost = calculate_I_pipeline_cost(distance)
            min_cost += pipeline_cost
            total_I_pipeline_length += distance

    # 计算一级供水站到二级供水站的II型管道费用和长度
    for i, j in route_A_V_P[0]:
        if i != 0:
            distance = distance.euclidean(points[i], points[j])
            pipeline_cost = calculate_II_pipeline_cost(distance)
            min_cost += pipeline_cost
            total_II_pipeline_length += distance

    print("最小费用:", min_cost)
    print("I型管道长度:", total_I_pipeline_length)
    print("II型管道长度:", total_II_pipeline_length)

    # 绘制AVP站点之间的最优路线图
    x = []
    y = []
    for i in closest_points:
        x.append(i[0])
        y.append(i[1])
    plt.scatter(x[:k], y[:k], 15, "red")
    plt.scatter(x[k:], y[k:], 10, "blue")
    count = 0
    for i in route_A_V_P[0]:
        count += 1
        x = [closest_points[i[0]][0], closest_points[i[1]][0]]
        y = [closest_points[i[0]][1], closest_points[i[1]][1]]
        if count <= k:
            plt.plot(x, y, color='red')
        else:
            plt.plot(x, y, color='blue')
    plt.show()
