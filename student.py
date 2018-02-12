#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import sys
import random


class Student(object):
    def __init__(self, num=0, name='unknow', height=150, duty=False):
        self.num = num
        self.name = name
        self.height = height
        self.duty = duty

    def __repr__(self):
        return '{},{},{},{}'.format(self.num, self.name, self.height, self.duty)

    def __str__(self):
        return self.__repr__()


def student_factory(filename):
    students = []
    with open(filename, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            if line[0] in ('#', '\n'):
                continue

            line = line.strip('\n')
            num, name, height, duty = line.split(',')
            st = Student(num, name, height, duty)
            students.append(st)
    return students
        

def make_config_file():
    lines = []
    for i in range(1,41):
        line = '{},unknow,{},0\n'.format(i, random.randint(149, 165))
        lines.append(line)

    with open('config.txt', 'w', encoding='utf-8') as fw:
        fw.writelines(lines)


if __name__ == '__main__':
    #make_config_file()

    students = student_factory('config.txt')
    [print(st) for st in students]
