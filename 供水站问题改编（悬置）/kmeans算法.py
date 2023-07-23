
from sklearn.cluster import KMeans
import numpy as np

# 给定的点的坐标
points = np.array([[26, 31], [5, 33], [8, 9], [10, 24], [13, 34], [17, 23], [20, 10], [25, 47], [31, 18], [35, 42], [36, 25], [41, 31], [45, 38], [41, 35], [40, 34], [38, 35], [38, 37], [33, 37], [31, 36], [33, 35], [28, 32], [24, 30], [21, 31], [22, 27], [28, 29], [43, 37], [44, 39], [25, 27], [21, 29], [22, 30], [24, 32], [37, 33], [38, 33], [37, 36], [14, 13], [16, 9], [14, 7], [18, 14], [12, 6], [15, 14], [20, 13], [13, 46], [16, 39], [21, 39], [26, 44], [28, 40], [27, 42], [29, 38], [29, 44], [35, 43], [41, 40], [39, 52], [27, 49], [23, 46], [20, 46], [16, 46], [22, 44], [40, 44], [42, 40], [37, 42], [35, 49], [35, 51], [35, 52], [34, 55], [26, 53], [27, 51], [31, 51], [31, 45], [31, 41], [28, 45], [27, 35], [25, 38], [26, 39], [13, 37], [17, 36], [21, 41], [18, 41], [21, 43], [13, 39], [14, 43], [12, 43], [10, 44], [16, 44], [18, 44], [24, 44], [25, 49], [24, 49], [24, 51], [21, 48], [17, 51], [10, 34], [9, 35], [7, 37], [4, 37], [5, 42], [2, 44], [7, 32], [7, 30], [1, 24], [2, 16], [3, 18], [2, 20], [4, 24], [5, 28], [6, 24], [9, 29], [2, 33], [7, 34], [3, 30], [3, 41], [10, 36], [17, 34], [20, 22], [24, 21], [22, 17], [21, 16], [27, 19], [26, 16], [9, 16], [12, 17], [14, 15], [19, 26], [14, 28], [13, 25], [9, 19], [2, 1], [6, 6], [7, 8], [6, 14], [5, 17], [5, 16], [16, 19], [26, 13], [29, 11], [31, 14], [28, 17], [20, 19], [17, 22], [15, 23], [21, 23], [24, 23], [26, 23], [25, 25], [15, 31], [15, 29], [10, 28], [38, 26], [37, 25], [33, 21], [40, 24], [44, 44], [42, 31], [33, 24], [32, 27], [40, 14], [42, 26], [45, 33], [29, 23], [31, 30], [30, 25], [31, 23], [35, 15], [40, 16], [40, 20], [37, 20], [35, 24], [43, 23], [45, 26], [37, 28], [35, 28], [33, 29], [37, 30], [39, 30], [41, 29], [43, 31], [47, 34], [46, 43], [42, 43], [48, 45], [42, 44], [43, 50]])

# 设置k值，即要聚类的中心点数目
k = 10

# 使用KMeans算法进行聚类
kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(points)

# 获取聚类的中心点坐标
centers = kmeans.cluster_centers_

# 寻找距离中心点最近的点的坐标
labels = kmeans.labels_
distances = kmeans.transform(points)

# 遍历每个中心点
for i in range(k):
    # 获取距离第i个中心点最近的点的索引
    closest_point_index = np.argmin(distances[:, i])

    # 获取最近的点的坐标
    closest_point = points[closest_point_index]

    # 打印结果
    print(f"中心点{i + 1}的坐标：{centers[i]}")
    print(f"距离中心点{i + 1}最近的点的坐标：{closest_point}")