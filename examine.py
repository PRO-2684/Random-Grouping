import re
import statistics

# 获取特定格式文件的信息
import numpy


def read(filename):
    try:
        fil = open(filename, "r", encoding="utf-8")
    except OSError as reason:
        print("出错了:" + str(reason))
    else:
        namelist = []
        while True:
            line = fil.readline()
            if not line:
                break
            namelist.append(line)
        fil.close()
        return namelist


# 将编号信息转化为成绩与性别信息
def trans(orgin_list1, teamlist1):
    teplist = []
    i1 = 0
    for team in teamlist1:
        teplist.append([])
        for person in team:
            k1 = int((re.split(r'[ ]', person))[1])
            teplist[i1].append(re.split(r'[ ]', orgin_list1[k1 - 1]))
        i1 += 1
    return teplist


# 计算各组人数的极差
def exam_num(team_list):
    numlis = []
    for team in team_list:
        numlis.append(len(team))
    print("各组人数的极差为:" + str(max(numlis) - min(numlis)))


# 计算每组人员平均能力并返回一列表
def average_ability(team_list):
    aver_ability = []
    for team in team_list:
        tep_list = []
        for person in team:
            tep_list.append(int(person[3]))
        aver_ability.append(round(statistics.mean(tep_list), 2))
    return aver_ability


# 计算各组成员的男生比例
def gender(team_list):
    sex_ratio = []
    for team in team_list:
        male = 0
        total = 0
        for person in team:
            if person[2] == '男':
                male += 1
                total += 1
            else:
                total += 1
        sex_ratio.append(round(male / total, 2))
    return sex_ratio


# 检验队伍中是否有人在同一寝室
def exam_dorm(team_list):
    for team in team_list:
        dorm = []
        for person in team:
            if person[4] not in dorm:
                dorm.append(person[4])
            else:
                return False
    return True


result_file = input("请输入结果文件名:")
name_list = read(result_file)[1:]  # 去除无用行
teamlist = [[]]
k = 1
for i in name_list:
    if int((re.split(r'[ ]', i))[0]) == k:
        teamlist[k - 1].append(i)
    else:
        teamlist.append([])
        k += 1
        teamlist[k - 1].append(i)  # 将同组人员放在一起
orgin_file = input("请输入原始文件名:")
orgin_list = read(orgin_file)  # 读入原始名单
teamlist = trans(orgin_list, teamlist)  # 在原始名单内查找相关信息
aver = average_ability(teamlist)
exam_num(teamlist)
print("各组平均能力" + str(aver))
print("各组平均能力值的极差为" + str(round(max(aver) - min(aver), 2)))
sexradio = gender(teamlist)
print("各组男生所占比例" + str(sexradio))
if exam_dorm(teamlist):
    print("各组中不存在同寝室成员")
else:
    print("组中存在同寝室成员")
