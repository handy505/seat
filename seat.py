#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import random
import collections
import copy
import numpy as np

import student

ROW_MAX = 6
COLUMN_MAX = 7


class SeatTable(object):
    def __init__(self, students, mating_pair=None):
        self.mating_pair = mating_pair
        self.students = students

        if self.mating_pair: self.init_by_mating()
        else:                self.init_by_random()

        self.score = self.calc_score()


    def init_by_mating(self):
        st_nums = copy.deepcopy(list(self.students.keys()))
        self.table = np.zeros((ROW_MAX, COLUMN_MAX), dtype='int32')
        rows, cols = self.table.shape
        locations = [(r,c) for r in range(rows) for c in range(cols)]
        a = self.mating_pair[0]
        b = self.mating_pair[1]

        # copy the same gene(seat location)
        for r, c in locations:
            if a.table[r, c] == b.table[r, c]:
                st_num = a.table[r, c]
                if st_num != 0:
                    st_nums.remove(st_num)
                    locations.remove((r,c))
                    self.table[r,c] = st_num

        while st_nums:
            st_num = random.choice(st_nums) # random choice student
            st_nums.remove(st_num)
            loc = random.choice(locations) # random choice location
            locations.remove(loc)

            r, c = loc[0], loc[1]
            self.table[r,c] = st_num

        self.mutation()


    def init_by_random(self):
        st_nums = copy.deepcopy(list(self.students.keys()))
        self.table = np.zeros((ROW_MAX, COLUMN_MAX), dtype='int32')
        rows, cols = self.table.shape
        locations = [(r,c) for r in range(rows) for c in range(cols)]

        while st_nums:
            st_num = random.choice(st_nums) # random choice student
            st_nums.remove(st_num)
            loc = random.choice(locations) # random choice location
            locations.remove(loc)

            r, c = loc[0], loc[1]
            self.table[r,c] = st_num


    def mutation(self):
        while random.random() < 0.6:
            rows, cols = self.table.shape
            locations = [(r,c) for r in range(rows) for c in range(cols)]

            # random selcect 2 locations
            loc1 = random.choice(locations)
            loc2 = loc1
            while loc2 == loc1: 
                loc2 = random.choice(locations)
            
            # swap
            r1, c1 = loc1[0], loc1[1]
            r2, c2 = loc2[0], loc2[1]
            tmp = self.table[r1, c1]
            self.table[r1, c1] = self.table[r2, c2]
            self.table[r2, c2] = tmp


    def calc_score(self):
        hscore = self.height_score()
        return hscore


    def height_score(self):
        result = 0
        tt = self.table.transpose()
        for col in tt:
            height_score = self.col_height_score(col)
            result += height_score
        return result


    def col_height_score(self, col):
        result = 0
        for idx, sn in enumerate(col):
            if sn == 0: continue # empty seat
            st = self.students[sn]
            h = st.height

            for sn2 in col[:idx]:
                if sn2 == 0: continue # empty seat
                if sn2 != sn:
                    front_st = self.students[sn2]
                    front_h = front_st.height
                    diff = (front_h - h) if front_h > h else 0
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

        line = 'score: {}'.format(self.calc_score())
        lines.append(line)

        result = '\n'.join(lines)
        return result


    def __str__(self):
        return str(self.table)


if __name__ == '__main__':
    students = student.student_factory('config.txt')

    for _ in range(3):
        table = SeatTable(students)
        print(table)
        print(repr(table))


