# 傻瓜式问卷信息录入

import pandas as pd

name = input('请输入调查问卷的名称')


def collect_survey():
    # 收集问卷
    survey = []
    while True:
        question = input("请输入问题（输入 'q' 结束）: ")
        if question == 'q':
            break
        options = input("请输入选项，用逗号分隔: ").split(',')  # 输入选项，用逗号分隔
        survey.append((question, options))  # 将问题和选项添加到问卷列表中
    return survey  # 返回问卷列表


def survey_to_excel(survey, filename):
    # 将问卷数据保存到Excel文件中
    data = {'问题': [q for q, _ in survey]}  # 创建一个字典，问题列表作为'问题'列的值
    for i, (_, options) in enumerate(survey):
        # 遍历问卷列表中的每个问题及其选项
        for j, option in enumerate(options):
            if f'问卷{j + 1}' not in data:
                # 如果'问卷j'列不存在，创建一个空的列
                data[f'问卷{j + 1}'] = [''] * len(survey)
            # 将选项添加到相应的列中
            data[f'问卷{j + 1}'][i] = option
    df = pd.DataFrame(data)  # 创建数据帧
    df.to_excel(filename, index=False)  # 将数据帧保存到Excel文件中，不包含索引列


survey = collect_survey()  # 收集问卷
survey_to_excel(survey, f'{name}.xlsx')  # 将问卷保存到Excel文件
