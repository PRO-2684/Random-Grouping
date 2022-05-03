import argparse


class Student:
    def __init__(self, info: str):
        """id name gender ability room"""
        info = info.split()
        self.id = info[0]
        self.name = info[1]
        self.gender = get_gender(info[2])
        self.ability = int(info[3])
        self.room = info[4]


def get_gender(s: str) -> bool:
    if s == "男":
        return True
    elif s == "女":
        return False
    else:
        raise ValueError("Invalid gender: " + s)


def from_file(path: str) -> set[Student]:
    result = set()
    with open(path, encoding="utf-8") as f:
        for line in f.readlines():
            student = Student(line)
            result.add(student)
    return result


def average(students: list[Student], attr: str) -> float:
    sum = 0
    for student in students:
        sum += student.__getattribute__(attr)
    return sum / len(students)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple grouping proogram.")
    parser.add_argument("file", help="Input file path.")
    parser.add_argument("count", help="Number of people inside a group.", type=int)
    args = parser.parse_args()
    students = from_file(args.file)
    count = args.count
    male_percentage = average(students, "gender")
    average_ability = average(students, "ability")
    print(male_percentage, average_ability)
