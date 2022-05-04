import argparse
from random import shuffle
from os import get_terminal_size


WEIGHTS = 1000, 1, 0.01
"""The weights of dormitory, sex ratio and ability used in calculating conflicts."""


class Student:
    """Main class representing a student."""

    def __init__(self, info: str):
        """`info` should be in the format of `id name gender ability room`."""
        info = info.split()
        self.id = info[0]
        self.name = info[1]
        self.sex = get_gender(info[2])
        self.ability = int(info[3])
        self.dorm = info[4]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} name={self.name} sex={'男' if self.sex else '女'} ability={self.ability} dorm={self.dorm}>"

    def __str__(self) -> str:
        return f"#{self.id}\t{self.name}\t{'男' if self.sex else '女'}\t{self.ability}\t{self.dorm}"


def get_gender(s: str) -> bool:
    """Translate genders into booleans."""
    if s == "男":
        return True
    elif s == "女":
        return False
    else:
        raise ValueError("Invalid gender: " + s)


def from_file(path: str) -> list[Student]:
    """Generate a student list from a file."""
    result = []
    with open(path, encoding="utf-8") as f:
        for line in f.readlines():
            student = Student(line)
            result.append(student)
    return result


def average(students: list[Student], attr: str) -> float:
    """Average of given attribute."""
    sum_ = sum(map(lambda stu: getattr(stu, attr), students))
    return sum_ / len(students)


def conflict(
    students: list[Student], group_size: int, sex_ratio: float, average_ability: float
) -> float:
    """Conflict value consists of 3 aspects: dormitory, sex ratio and ability."""
    left = len(students) % group_size
    div = len(students) - left * group_size
    result = 0
    group_sex_ratio = 0
    group_average_ability = 0
    dorm = set()
    for i, student in enumerate(students[:div]):
        if student.dorm in dorm:
            result += WEIGHTS[0]
        else:
            dorm.add(student.dorm)
        group_sex_ratio += student.sex
        group_average_ability += student.ability
        if not (i + 1) % group_size:  # End of a group.
            group_sex_ratio /= group_size
            group_average_ability /= group_size
            result += (
                abs(group_sex_ratio - sex_ratio) * WEIGHTS[1]
                + abs(group_average_ability - average_ability) * WEIGHTS[2]
            )
            dorm.clear()
            group_sex_ratio = 0
            group_average_ability = 0
    for i, student in enumerate(students[div:]):
        if student.dorm in dorm:
            result += WEIGHTS[0]
        else:
            dorm.add(student.dorm)
        group_sex_ratio += student.sex
        group_average_ability += student.ability
        if not (i + 1 - div) % (group_size + 1):  # End of a group.
            group_sex_ratio /= group_size
            group_average_ability /= group_size
            result += (
                abs(group_sex_ratio - sex_ratio) * WEIGHTS[1]
                + abs(group_average_ability - average_ability) * WEIGHTS[2]
            )
            dorm.clear()
            group_sex_ratio = 0
            group_average_ability = 0
    return result


def min_conf_point(students: list[Student], target: int, base_conf: float, *statistics) -> tuple[int]:
    """Find the minimum conflict pos for students[target]. Returns the pos and conflict."""
    result = target
    min_conf = base_conf
    for pos in range(target + 1, len(students)):
        students_ = students[:]
        students_[target], students_[pos] = students_[pos], students_[target]
        conf = conflict(students_, *statistics)
        if conf < min_conf:
            min_conf = conf
            result = pos
    return result, min_conf


def group(students: list[Student], size: int) -> int:
    """Main grouping function (in place)."""
    sex_ratio = average(students, "sex")
    average_ability = average(students, "ability")
    statistics = size, sex_ratio, average_ability
    shuffle(students)
    conf = conflict(students, *statistics)
    flag = True
    while flag:
        flag = False
        for target in range(len(students) - 1):
            pos, conf = min_conf_point(students, target, conf, *statistics)
            if pos != target:
                flag = True
                students[target], students[pos] = students[pos], students[target]
    return conf


def show(students: list[Student], group_size: int) -> None:
    left = len(students) % group_size
    div = len(students) - left * group_size
    cnt = 0
    group_id = 0
    term_size = get_terminal_size()
    print('ID\tName\tSex\tAbility\tDormitory')
    print('-' * term_size.columns, end='')
    for i, student in enumerate(students):
        if not cnt:
            group_id += 1
            print(f'\nGroup {group_id}:')
        cnt = (cnt + 1) % (group_size + (i > div))
        print(student)
    print('-' * term_size.columns)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple grouping program.")
    parser.add_argument("file", help="Input file path.")
    parser.add_argument("size", help="The expected size of a group.", type=int)
    args = parser.parse_args()
    print(f'Loading data from "{args.file}"...')
    students = from_file(args.file)
    print(f'Dividing into groups of {args.size}...\n')
    conf = group(students, args.size)
    show(students, args.size)
    print('Conflict value:', conf)
