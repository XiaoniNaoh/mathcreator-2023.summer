import pandas as pd

# 读取订单数据
orders_df = pd.read_csv('装箱数据.csv', header=None, names=['编号', '长', '宽', '高', '数量'],
                        encoding='utf-8')

# 定义袋子和箱子的大小
bag_sizes = [(250, 190, 1), (300, 250, 1), (400, 330, 1), (450, 420, 1)]
box_sizes = [(165, 120, 55), (200, 140, 70), (200, 150, 150), (270, 200, 90), (300, 200, 170)]


# 定义装包函数
def pack_using_bags(order):
    bags_cnt = [0] * len(bag_sizes)  # 初始化袋子的数量
    total_volume = 0  # 初始化总体积
    for i in range(order['数量']):  # 根据订单中的数量，循环处理每个物品
        volume = order['长'] * order['宽'] * order['高']
        while volume > 0:  # 当物品的体积大于0时，进行装包
            packed = False
            for j, bag_size in enumerate(bag_sizes):  # 遍历每种包的大小和对应的索引
                if (bag_size[0] >= order['长']) and (bag_size[1] >= order['宽']) and (bag_size[2] >= order['高']):
                    bags_cnt[j] += 1  # 包的数量加1
                    total_volume += bag_size[0] * bag_size[1] * bag_size[2]  # 更新总体积
                    packed = True  # 标记已经装包
                    break
            if not packed:  # 如果没有装包，跳出循环
                break
            volume -= bag_size[0] * bag_size[1] * bag_size[2]  # 更新物品的体积
    return bags_cnt, total_volume


# 定义装箱函数
def pack_using_boxes(order):
    boxes_cnt = [0] * len(box_sizes)  # 初始化箱子的数量
    total_volume = 0  # 初始化总体积
    for i in range(order['数量']):  # 根据订单中的数量，循环处理每个物品
        volume = order['长'] * order['宽'] * order['高']
        while volume > 0:  # 当物品的体积大于0时，进行装箱
            packed = False
            for j, box_size in enumerate(box_sizes):  # 遍历每种箱子的大小和对应的索引
                if (box_size[0] >= order['长']) and (box_size[1] >= order['宽']) and (box_size[2] >= order['高']):
                    boxes_cnt[j] += 1
                    total_volume += box_size[0] * box_size[1] * box_size[2]
                    packed = True
                    break
            if not packed:
                break
            volume -= box_size[0] * box_size[1] * box_size[2]
    return boxes_cnt, total_volume


# 定义混合装包装箱函数
def pack_using_mixed(order):
    bags_cnt = [0] * len(bag_sizes)  # 初始化袋子的数量
    boxes_cnt = [0] * len(box_sizes)  # 初始化箱子的数量
    total_volume = 0  # 初始化总体积
    for i in range(order['数量']):  # 根据订单中的数量，循环处理每个物品
        volume = order['长'] * order['宽'] * order['高']
        while volume > 0:  # 当物品的体积大于0时，进行装箱
            packed_as_bag = False
            for j, bag_size in enumerate(bag_sizes):
                if (bag_size[0] >= order['长']) and (bag_size[1] >= order['宽']) and (bag_size[2] >= order['高']):
                    bags_cnt[j] += 1
                    total_volume += bag_size[0] * bag_size[1] * bag_size[2]
                    packed_as_bag = True
                    break
            if not packed_as_bag:
                for j, box_size in enumerate(box_sizes):
                    if (box_size[0] >= order['长']) and (box_size[1] >= order['宽']) and (box_size[2] >= order['高']):
                        boxes_cnt[j] += 1
                        total_volume += box_size[0] * box_size[1] * box_size[2]
                        break
                if not packed_as_bag:
                    break
            volume -= bag_size[0] * bag_size[1] * bag_size[2] if packed_as_bag else box_size[0] * box_size[1] * \
                                                                                    box_size[2]
    return bags_cnt, boxes_cnt, total_volume


# 定义装包函数
def pack_orders(orders):
    bags_cnt_list = []
    boxes_cnt_list = []
    mixed_cnt_list = []
    total_volume_using_bags = 0
    total_volume_using_boxes = 0
    total_volume_using_mixed = 0
    for _, order in orders.iterrows():
        bags_cnt, total_volume = pack_using_bags(order)
        bags_cnt_list.append(bags_cnt)
        total_volume_using_bags += total_volume

        boxes_cnt, total_volume = pack_using_boxes(order)
        boxes_cnt_list.append(boxes_cnt)
        total_volume_using_boxes += total_volume

        bags_cnt, boxes_cnt, total_volume = pack_using_mixed(order)
        mixed_cnt_list.append((bags_cnt, boxes_cnt))
        total_volume_using_mixed += total_volume

        materials_cnt = [sum(map(sum, bags_cnt_list)), sum(map(sum, boxes_cnt_list)),
                         sum(map(lambda x: sum(x[0]) + sum(x[1]), mixed_cnt_list))]
        total_volumes = [total_volume_using_bags, total_volume_using_boxes,
                         total_volume_using_mixed + min(total_volume_using_bags, total_volume_using_boxes)]

        min_materials_cnt = min(materials_cnt)
        min_materials_idx = materials_cnt.index(min_materials_cnt)
        if materials_cnt.count(min_materials_cnt) > 1:
            min_total_volumes = min([total_volumes[i] for i in range(3) if materials_cnt[i] == min_materials_cnt])
            min_total_volumes_idx = \
            [i for i in range(3) if materials_cnt[i] == min_materials_cnt and total_volumes[i] == min_total_volumes][0]
            return (min_materials_idx, min_total_volumes_idx), materials_cnt[min_total_volumes_idx], total_volumes[
                min_total_volumes_idx]
        else:
            return ((min_materials_idx, materials_cnt.index(min_materials_cnt)), min_materials_cnt,
                    total_volumes[materials_cnt.index(min_materials_cnt)])


# 调用pack_orders函数并输出结果
result = pack_orders(orders_df)
print(f'最优方案为：{result[0]}, 最小耗材数量为：{result[1]:.0f}, 最小总体积为：{result[2]:.0f}。')
