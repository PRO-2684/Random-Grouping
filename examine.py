import re
import statistics


# 获取特定格式文件的信息
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
            teplist[i1].append(re.split(r'[ ]', orgin_list1[int(person[2:5]) - 1]))
        i1 += 1
    return teplist


# 计算每组人员平均能力并返回一列表
def average_ability(team_list):
    aver_ability = []
    for team in team_list:
        tep_list = []
        for person in team:
            tep_list.append(int(person[3]))
        aver_ability.append(statistics.mean(tep_list))
    return aver_ability


# 计算各组成员的男女比例
def gender(team_list):
    sex_ratio = []
    for team in team_list:
        male = 0
        female = 0
        for person in team:
            if person[2] == '男':
                male += 1
            else:
                female += 1
        sex_ratio.append('%.2f' % (male / female))
    return sex_ratio


# 检验队伍中是否有人在同一寝室
def exam_dorm(team_list):
    for team in team_list:
        dorm = []
        for person in team:
            if person[4] not in dorm:
                dorm.append(person[4])
            else:
                return 0
    return 1


result_file = input("请输入结果文件名:")
name_list = read(result_file)[1:]
teamlist = [[]]
k = 1
for i in name_list:
    if int(i[0]) == k:
        teamlist[k - 1].append(i)
    else:
        teamlist.append([])
        k += 1
        teamlist[k - 1].append(i)
orgin_file = input("请输入原始文件名:")
orgin_list = read(orgin_file)
teamlist = trans(orgin_list, teamlist)
aver = average_ability(teamlist)
print("各组平均能力" + str(aver))
print("各组平均能力值的极差为" + str(max(aver) - min(aver)))
sexradio = gender(teamlist)
print("各组男女比例" + str(sexradio))
if exam_dorm(teamlist) == 0:
    print("组中存在同寝室成员")
else:
    print("各组中不存在同寝室成员")
