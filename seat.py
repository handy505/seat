#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import random
import collections
import copy

import student

ROW_MAX = 7
COLUMN_MAX = 7


class SeatTable(object):
    def __init__(self, students, row=ROW_MAX, column=COLUMN_MAX):
        tmpstudents = copy.deepcopy(students)

        # 2 dimention list
        self.table = [[(r,c) for c in range(COLUMN_MAX)] for r in range(ROW_MAX)]

        for r in range(0, ROW_MAX):
            for c in range(0, COLUMN_MAX):
                st = random.choice(tmpstudents)
                self.table[r][c] = st
                print('{} {}'.format(c, st))
                tmpstudents.remove(st)
                if not tmpstudents:
                    break
            if not tmpstudents:
                break
        pass

    def score(self):
        pass
    
    def __repr__(self):
        return str(self.table)

    def __str__(self):
        return self.__repr__()


class SeatSheet(object):
    def __init__(self, row=ROW_MAX, column=COLUMN_MAX, students=None):
        self.__table = collections.OrderedDict()
        self.__row = row
        self.__column = column
        self.__students = students
        self.__students_expendables = copy.deepcopy(self.__students) 
        for i in range(0, self.__row):
            for j in range(0, self.__column):
                if self.__students_expendables:
                    rnd = random.randint(0, len(self.__students_expendables)-1)
                    self.__table[(i, j)] = self.__students_expendables[rnd]
                    self.__students_expendables.pop(rnd)
                else:
                    self.__table[(i, j)] = None
        
        self.__score = 0
        self.__hscore = 0
        self.__dscore = 0
        self.__xscore = 0
        self.__variation = True
        
    
    @property
    def row(self):
        return self.__row
        
    @property
    def column(self):
        return self.__column
        
    @property
    def table(self):
        return self.__table
        
    @table.setter
    def table(self, key, val):
        self.__table[key] = val
        self.__variation = True

    def calc_score(self):
        """ weight adjusting """
        DUTY_WEIGHT = 100
        EXCLUSION_WEIGHT = 10
        HEIGHT_WEIGHT = 1
        #BASE_SCORE = 7600 # perfect max score: 9000, 9000 = 7600 + (7*2*100)
        OFFSET_SCORE = 9000 - (DUTY_WEIGHT*14)
        self.__hscore = self.height_score()
        self.__dscore = self.duty_score()
        self.__xscore = self.exclusion_score()
        self.__score = OFFSET_SCORE + (self.__dscore*DUTY_WEIGHT) - (self.__xscore*EXCLUSION_WEIGHT) - (self.__hscore*HEIGHT_WEIGHT)

    @property
    def score(self):
        if self.__variation:
            self.calc_score()
            self.__variation = False
            
        return self.__score
    
    @property
    def hscore(self):
        return self.__hscore
    
    @property
    def dscore(self):
        return self.__dscore
    
    @property
    def xscore(self):
        return self.__xscore
        
    def info(self):
        """ information """
        string = ""
        for i in range(0, self.__row):
            for j in range(0, self.__column):
                st = self.__table[(i, j)].info() if self.__table[(i, j)] else "xxxx" 
                string += "({0}, {1}) {2}\n".format(i, j, st)
        return string
        
    def height_score(self):
        """ height score """
        IGNORE_ERROR = 0
        hscore = 0
        for r, c in self.__table:
            st = self.__table[(r, c)]

            #print("check location:{0}".format((r, c))) # debug
            if st and (r != 0):
                # valid seat
                curHeight = self.__table[(r, c)].height
                for before in range(0, r):
                    if self.__table[(before, c)]:
                        beforeHeight = self.__table[(before, c)].height
                        hscore += (beforeHeight - curHeight) if beforeHeight > (curHeight + IGNORE_ERROR) else 0
                        #print("hscore:{0} at {1} scan {2}".format(hscore, (r, c), (before, c))) # debug
        return hscore

    def duty_score(self):
        col_score = []
        for c in range(0, self.__column):
            rcount = 0
            for r in range(0, self.__row):
                st = self.__table[(r, c)]
                if st:
                    rcount = rcount + (1 if st.duty == True else 0)
            if rcount <=2:
                col_score.append(rcount) 
            else:
                col_score.append(2)
        return sum(col_score)
        
    def __location_valid(self, loc):
        x = loc[0]
        y = loc[1]
        if (0 <= x < self.__row) and (0 <= y < self.__column):
            return True
        else:
            return False
    
    def exclusion_score(self):

        xscore = 0
        for r, c in self.__table:
            st = self.__table[(r, c)]
            #print(r, c, st.info())
            if st.exclusive != "nx":
            
                near = (r-1, c-1)
                if self.__location_valid(near):
                    xscore = xscore + (1 if self.__table[near].exclusive == st.exclusive else 0)
                    #print("--valid ", xscore) # debug
                
                near = (r-1, c)
                if self.__location_valid(near):
                    xscore = xscore + (1 if self.__table[near].exclusive == st.exclusive else 0)
                    #print("-0valid ", xscore) # debug
                
                near = (r-1, c+1)
                if self.__location_valid(near):
                    xscore = xscore + (1 if self.__table[near].exclusive == st.exclusive else 0)
                    #print("-+valid ", xscore) # debug
                
                near = (r, c-1)
                if self.__location_valid(near):
                    xscore = xscore + (1 if self.__table[near].exclusive == st.exclusive else 0)
                    #print("0-valid ", xscore) # debug
                
                near = (r, c+1)
                if self.__location_valid(near):
                    xscore = xscore + (1 if self.__table[near].exclusive == st.exclusive else 0)
                    #print("0+valid ", xscore) # debug
                
                near = (r+1, c-1)
                if self.__location_valid(near):
                    xscore = xscore + (1 if self.__table[near].exclusive == st.exclusive else 0)
                    #print("+-valid ", xscore) # debug
                
                near = (r+1, c)
                if self.__location_valid(near):
                    xscore = xscore + (1 if self.__table[near].exclusive == st.exclusive else 0)
                    #print("+0valid ", xscore) # debug
                
                near = (r+1, c+1)
                if self.__location_valid(near):
                    xscore = xscore + (1 if self.__table[near].exclusive == st.exclusive else 0)
                    #print("++valid ", xscore) # debug
        return xscore


if __name__ == '__main__':
    students = student.student_factory('config.txt')
    t = SeatTable(students)
    print(t)
