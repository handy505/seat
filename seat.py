#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import random
import collections
import copy
import numpy as np
import time

import student

ROW_MAX = 6
COLUMN_MAX = 7

'''
Gene Algorithm Concept:
    chromosome - SeatTable
    fitness - SeatTable score
    select - wheel select
    mating
    mutation
'''
class SeatTable(object):
    def __init__(self, students, mating_pair=None, row=ROW_MAX, column=COLUMN_MAX):
        self.mating_pair = mating_pair
        self.students = students

        # 2 dimention list
        if self.mating_pair:
            self._init_by_mating()
        else:
            self._init_by_random_np()

    def _init_by_random_np(self):
        st_nums = copy.deepcopy(list(students.keys()))
        self.table = np.zeros((ROW_MAX, COLUMN_MAX), dtype='int32')
        rows, cols = self.table.shape
        locations = [(r,c) for r in range(rows) for c in range(cols)]

        while st_nums:
            st_num = random.choice(st_nums)
            st_nums.remove(st_num)
            loc = random.choice(locations)
            locations.remove(loc)

            r = loc[0]
            c = loc[1]
            self.table[r,c] = st_num


    def score(self):
        hscore = self.height_score()
        return hscore

    def height_score(self):
        result = 0
        rows, cols = self.table.shape
        tt = self.table.transpose()
        for c in tt:
            height_score = self.col_height_score(c)
            result += height_score
        return result

    def col_height_score(self, col):
        result = 0
        for idx, sn in enumerate(col):
            if sn == 0: continue
            st = self.students[sn]
            h = st.height

            for sn2 in col[:idx]:
                if sn2 == 0: continue
                if sn2 != sn:
                    front_st = self.students[sn2]
                    h2 = front_st.height
                    diff = h2 - h
                    result += diff 
        return result


    def __repr__(self):
        lines = []
        rows, cols = self.table.shape
        for r in range(rows):
            st_infos = []
            for c in range(cols):
                sn = self.table[r, c]
                if sn:
                    st = self.students[sn]
                    info = '#{:02d},{:03d},{}'.format(st.num, st.height, st.duty)
                    st_infos.append(info)
                else:
                    st_infos.append('#--,---,-')
            line = ' '.join(st_infos)
            lines.append(line)
        result = '\n'.join(lines)
        return result

    def __str__(self):
        return str(self.table)


if __name__ == '__main__':
    students = student.student_factory('config.txt')

    for _ in range(3):
        t = SeatTable(students)
        print()
        print(t)
        print(repr(t))
        t1 = time.time()
        print('score: {}'.format(t.score()))
        print('{} sec'.format(time.time() - t1))


